#!/usr/bin/env node
/**
 * Месячный монитор госаккредитации КИПУ по специальности 09.02.07.
 * Источник: страница sveden/common + PDF выписки реестра аккредитации.
 * При изменении статуса / PDF / ссылок — письмо на mishock24@gmail.com.
 *
 * Обновлено: 2026-11-19
 */
import crypto from "crypto";
import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CONFIG_PATH = path.join(ROOT, "config/accreditation-watch.json");
const SNAPSHOT_PATH = path.join(ROOT, "data/accreditation-snapshot.json");
const STATUS_MD_PATH = path.join(ROOT, "data/00_Аккредитация_09.02.07.md");
const LOG_PATH = path.join(process.env.HOME || "/home/pi", "logs/artem-accreditation.log");

const UA =
  "Mozilla/5.0 (compatible; ArtemStudyAccreditation/1.0; +https://kipu-rc.ru/)";

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
    fs.appendFileSync(LOG_PATH, line + "\n");
  } catch {
    /* ignore */
  }
}

function loadJson(p, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return fallback;
  }
}

function saveJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + "\n");
}

async function sleep(ms) {
  await new Promise((r) => setTimeout(r, ms));
}

async function fetchBuffer(url, timeoutMs = 45000, attempts = 4) {
  let lastErr;
  for (let i = 1; i <= attempts; i++) {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const res = await fetch(url, {
        signal: ctrl.signal,
        headers: { "User-Agent": UA, Accept: "*/*" },
        redirect: "follow",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status} ${url}`);
      const ab = await res.arrayBuffer();
      return Buffer.from(ab);
    } catch (err) {
      lastErr = err;
      log(`fetch retry ${i}/${attempts}: ${url} — ${err?.message || err}`);
      if (i < attempts) await sleep(1500 * i);
    } finally {
      clearTimeout(t);
    }
  }
  throw lastErr;
}

async function fetchText(url) {
  const buf = await fetchBuffer(url);
  return buf.toString("utf8");
}

function sha256(buf) {
  return crypto.createHash("sha256").update(buf).digest("hex");
}

function extractAccredLinks(html, baseUrl) {
  const links = [];
  const re = /<a[^>]+href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(html))) {
    const href = m[1].trim();
    const text = m[2].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
    const blob = `${href} ${text}`.toLowerCase();
    if (!/аккредит|лиценз|reestr|реестр|выписк|vipiska|obrnadzor|isga/i.test(blob)) {
      continue;
    }
    let abs = href;
    try {
      abs = new URL(href, baseUrl).href;
    } catch {
      /* keep */
    }
    links.push({ text, href: abs });
  }
  return links;
}

function pdfToText(buf) {
  const tmp = path.join(
    "/tmp",
    `kipu-accred-${process.pid}-${Date.now()}.pdf`
  );
  fs.writeFileSync(tmp, buf);
  try {
    const r = spawnSync("pdftotext", ["-layout", tmp, "-"], {
      encoding: "utf8",
      maxBuffer: 8 * 1024 * 1024,
    });
    if (r.status !== 0) {
      throw new Error(r.stderr || "pdftotext failed");
    }
    return r.stdout || "";
  } finally {
    try {
      fs.unlinkSync(tmp);
    } catch {
      /* ignore */
    }
  }
}

function findSpecialtyStatus(text, code) {
  const lines = text.split(/\r?\n/);
  const present = text.includes(code);
  let status = null;
  let context = [];
  if (!present) {
    return { present: false, status: null, context: [] };
  }
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].includes(code)) continue;
    const window = lines.slice(Math.max(0, i - 1), Math.min(lines.length, i + 5));
    context = window.map((l) => l.trim()).filter(Boolean);
    const joined = window.join(" ");
    const sm = joined.match(
      /(Действующ\w*|Приостановлен\w*|Не действующ\w*|прекращен\w*)/i
    );
    if (sm) status = sm[1];
    break;
  }
  return { present: true, status, context };
}

function extractAsOf(text) {
  const m = text.match(/по состоянию на[^\n]*?(\d{1,2}[./]\d{1,2}[./]\d{2,4})/i);
  return m ? m[1] : null;
}

function sendEmail(cfg, subject, body) {
  const script = cfg.emailFromScript;
  if (!fs.existsSync(script)) {
    log(`email skip: нет ${script}`);
    return false;
  }
  const r = spawnSync(script, [subject, body, cfg.emailTo], {
    encoding: "utf8",
  });
  if (r.status !== 0) {
    log(`email ERR: ${r.stderr || r.stdout}`);
    return false;
  }
  log(`email sent → ${cfg.emailTo}: ${subject}`);
  return true;
}

function summarize(snap) {
  const code = snap.specialtyCode;
  const ac = snap.accredPdf || {};
  const lic = snap.licensePdf || {};
  if (ac.specialtyPresent) {
    return `${code}: в выписке госаккредитации НАЙДЕНА (статус: ${
      ac.specialtyStatus || "не указан"
    })`;
  }
  if (lic.specialtyPresent) {
    return `${code}: лицензия есть, госаккредитация в выписке НЕ найдена`;
  }
  return `${code}: в выписке госаккредитации и лицензии код не найден`;
}

function diffSnapshots(prev, next) {
  const changes = [];
  if (!prev) return changes;
  if (prev.summary !== next.summary) {
    changes.push(`Сводка: было «${prev.summary}» → стало «${next.summary}»`);
  }
  const pAc = prev.accredPdf || {};
  const nAc = next.accredPdf || {};
  if (Boolean(pAc.specialtyPresent) !== Boolean(nAc.specialtyPresent)) {
    changes.push(
      `09.02.07 в выписке аккредитации: ${pAc.specialtyPresent} → ${nAc.specialtyPresent}`
    );
  }
  if ((pAc.specialtyStatus || null) !== (nAc.specialtyStatus || null)) {
    changes.push(
      `Статус в выписке: ${pAc.specialtyStatus || "—"} → ${
        nAc.specialtyStatus || "—"
      }`
    );
  }
  if (pAc.sha256 && nAc.sha256 && pAc.sha256 !== nAc.sha256) {
    changes.push(`PDF выписки аккредитации изменился (sha256)`);
  }
  if ((pAc.asOf || null) !== (nAc.asOf || null)) {
    changes.push(`Дата «по состоянию на»: ${pAc.asOf || "—"} → ${nAc.asOf || "—"}`);
  }
  const pLic = prev.licensePdf || {};
  const nLic = next.licensePdf || {};
  if (Boolean(pLic.specialtyPresent) !== Boolean(nLic.specialtyPresent)) {
    changes.push(
      `09.02.07 в выписке лицензии: ${pLic.specialtyPresent} → ${nLic.specialtyPresent}`
    );
  }
  if (pLic.sha256 && nLic.sha256 && pLic.sha256 !== nLic.sha256) {
    changes.push(`PDF выписки лицензии изменился (sha256)`);
  }
  if ((prev.page || {}).hash !== (next.page || {}).hash) {
    changes.push(`Страница sveden/common изменилась (текст/ссылки по лицензии/аккредитации)`);
  }
  const prevHrefs = new Set(((prev.page || {}).links || []).map((l) => l.href));
  const nextLinks = (next.page || {}).links || [];
  for (const l of nextLinks) {
    if (!prevHrefs.has(l.href)) {
      changes.push(`Новая ссылка: ${l.text || l.href}`);
    }
  }
  return changes;
}

function writeStatusMd(snap, changes) {
  const now = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  const ac = snap.accredPdf || {};
  const lic = snap.licensePdf || {};
  let md = `# Аккредитация 09.02.07 — КИПУ / ЦСПО

> **Обновлено:** ${now} (MSK)  
> Специальность: **${snap.specialtyCode}** «${snap.specialtyName}»  
> Автопроверка: **раз в месяц** (1-е число) + по запросу

## Текущий статус

**${snap.summary}**

| Источник | Результат |
|----------|-----------|
| Выписка госаккредитации | ${ac.specialtyPresent ? `найдена (${ac.specialtyStatus || "статус н/д"})` : "код **не найден**"} |
| Выписка лицензии | ${lic.specialtyPresent ? "код есть (обучение разрешено)" : "код не найден"} |
| PDF аккредитации «по состоянию на» | ${ac.asOf || "—"} |
| Страница | ${snap.page?.url || "—"} |

## Ссылки

- [Основные сведения (лицензия, аккредитация)](${snap.page?.url || "https://kipu-rc.ru/sveden/common/"})
- [Выписка из реестра аккредитации (PDF)](${ac.url || ""})
- [Выписка из реестра лицензий (PDF)](${lic.url || ""})
- [Реестр Рособрнадзора](${snap.registryUrl || ""})

## Контекст из PDF аккредитации

\`\`\`
${(ac.context || []).join("\n") || "(код 09.02.07 в выписке отсутствует)"}
\`\`\`

## Последние изменения этой проверки

${
  changes.length
    ? changes.map((c) => `- ${c}`).join("\n")
    : "- без изменений относительно предыдущего снимка"
}

*Скрипт: \`scripts/accreditation-monitor.mjs\`*
`;
  fs.writeFileSync(STATUS_MD_PATH, md);
}

async function main() {
  const cfg = loadJson(CONFIG_PATH);
  if (!cfg) {
    log("ERR: нет config/accreditation-watch.json");
    process.exit(1);
  }
  const forceEmail = process.argv.includes("--force-email");
  const notifyBaseline = process.argv.includes("--notify-baseline");

  log("старт проверки аккредитации 09.02.07");

  const pageHtml = await fetchText(cfg.commonPageUrl);
  const links = extractAccredLinks(pageHtml, cfg.commonPageUrl);
  // Хеш только по релевантным ссылкам (полный HTML страницы нестабилен).
  const stableLinks = links
    .map((l) => ({
      href: l.href,
      text: (l.text || "").replace(/\s+/g, " ").trim(),
    }))
    .sort((a, b) => a.href.localeCompare(b.href) || a.text.localeCompare(b.text));
  const pageHash = sha256(Buffer.from(JSON.stringify(stableLinks)));

  const accredBuf = await fetchBuffer(cfg.accredPdfUrl);
  const accredText = pdfToText(accredBuf);
  const accredHit = findSpecialtyStatus(accredText, cfg.specialtyCode);

  const licenseBuf = await fetchBuffer(cfg.licensePdfUrl);
  const licenseText = pdfToText(licenseBuf);
  const licenseHit = findSpecialtyStatus(licenseText, cfg.specialtyCode);

  const next = {
    checkedAt: new Date().toISOString(),
    checkedAtMsk: new Date().toLocaleString("ru-RU", {
      timeZone: "Europe/Moscow",
    }),
    specialtyCode: cfg.specialtyCode,
    specialtyName: cfg.specialtyName,
    registryUrl: cfg.registryUrl,
    page: {
      url: cfg.commonPageUrl,
      hash: pageHash,
      links,
    },
    accredPdf: {
      url: cfg.accredPdfUrl,
      sha256: sha256(accredBuf),
      bytes: accredBuf.length,
      asOf: extractAsOf(accredText),
      specialtyPresent: accredHit.present,
      specialtyStatus: accredHit.status,
      context: accredHit.context,
    },
    licensePdf: {
      url: cfg.licensePdfUrl,
      sha256: sha256(licenseBuf),
      bytes: licenseBuf.length,
      specialtyPresent: licenseHit.present,
      specialtyStatus: licenseHit.status,
      context: licenseHit.context,
    },
  };
  next.summary = summarize(next);

  const prev = loadJson(SNAPSHOT_PATH);
  const isBaseline = !prev;
  const changes = diffSnapshots(prev, next);

  writeStatusMd(next, changes);
  saveJson(SNAPSHOT_PATH, next);

  log(next.summary);
  if (isBaseline) {
    log("базовый снимок сохранён");
  } else if (changes.length) {
    log(`изменений: ${changes.length}`);
    changes.forEach((c) => log(`  - ${c}`));
  } else {
    log("без изменений");
  }

  const shouldEmail =
    forceEmail ||
    (isBaseline && notifyBaseline) ||
    (!isBaseline && changes.length > 0);

  if (shouldEmail) {
    const subject = isBaseline
      ? "КИПУ — мониторинг аккредитации 09.02.07 включён"
      : next.accredPdf.specialtyPresent
        ? "✓ КИПУ — аккредитация 09.02.07: изменение (код в выписке)"
        : "КИПУ — аккредитация 09.02.07: изменение на сайте";
    const body = [
      `Специальность: ${cfg.specialtyCode} «${cfg.specialtyName}»`,
      `Проверка: ${next.checkedAtMsk} (MSK)`,
      "",
      `Статус: ${next.summary}`,
      "",
      isBaseline
        ? "Это первое письмо: месячный контроль включён. Дальше письмо придёт только при изменении."
        : "Изменения:",
      ...(isBaseline ? [] : changes.map((c) => `• ${c}`)),
      "",
      `Страница: ${cfg.commonPageUrl}`,
      `PDF аккредитации: ${cfg.accredPdfUrl}`,
      `PDF лицензии: ${cfg.licensePdfUrl}`,
      "",
      `Локальная сводка: ${STATUS_MD_PATH}`,
    ].join("\n");
    sendEmail(cfg, subject, body);
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        baseline: isBaseline,
        changed: changes.length > 0,
        summary: next.summary,
        emailed: shouldEmail,
        changes,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  log(`FATAL: ${err?.stack || err}`);
  process.exit(1);
});
