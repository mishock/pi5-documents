#!/usr/bin/env node
/** Мониторинг kipu-rc.ru: изменения vs снимок + база из договора → живая сводка на Drive. */
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { fileURLToPath } from "url";
import { google } from "/home/pi/Projects/google-mcp/node_modules/googleapis/build/src/index.js";
import { SocksProxyAgent } from "/home/pi/Projects/google-mcp/node_modules/socks-proxy-agent/dist/index.js";
import {
  getTemporalContext,
  isTemporallyRelevant,
  temporalHeaderLine,
} from "./temporal-filter.mjs";
import { isSpecialtyRelevant, specialtyHeaderLine } from "./specialty-filter.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, "config/site-watch.json"), "utf8"));
const SNAPSHOT = path.join(DATA, "site-snapshot.json");
const CHANGES = path.join(DATA, "site-changes.json");
const LIVE_MD_LOCAL = path.join(DATA, "00_Мониторинг_сайта_КИПУ.md");
const FOLDER_ID = "1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V";
const LIVE_MD_NAME = "00_Мониторинг_сайта_КИПУ.md";
const PENDING = path.join(process.env.HOME, "logs/cursor-work/pending-artem-study.md");
const LOG = path.join(process.env.HOME, "logs/artem-study-drive.log");

function log(msg) {
  const line = `${new Date().toISOString()} site-monitor: ${msg}\n`;
  fs.mkdirSync(path.dirname(LOG), { recursive: true });
  fs.appendFileSync(LOG, line);
  console.log(msg);
}

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&[a-z]+;/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractLinks(html, baseUrl) {
  const links = [];
  const re = /<a[^>]+href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(html))) {
    let href = m[1];
    const text = stripHtml(m[2]).slice(0, 200);
    if (!text || href.startsWith("#") || href.startsWith("javascript:")) continue;
    try {
      href = new URL(href, baseUrl).href;
    } catch {
      continue;
    }
    links.push({ href, text });
  }
  return links;
}

function hashText(s) {
  return crypto.createHash("sha256").update(s).digest("hex").slice(0, 16);
}

function filterByKeywords(items, keywords) {
  const low = keywords.map((k) => k.toLowerCase());
  return items.filter((x) => {
    const blob = `${x.text || ""} ${x.href || ""}`.toLowerCase();
    return low.some((k) => blob.includes(k));
  });
}

async function fetchPage(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": "artem-study-monitor/1.0 (Pi5; family use)" },
    redirect: "follow",
    signal: AbortSignal.timeout(45000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${url}`);
  const html = await res.text();
  const text = stripHtml(html);
  const links = extractLinks(html, url);
  return { html, text: text.slice(0, 12000), links, fetchedAt: new Date().toISOString() };
}

function loadSnapshot() {
  if (!fs.existsSync(SNAPSHOT)) return { pages: {}, liveDocDriveId: null };
  return JSON.parse(fs.readFileSync(SNAPSHOT, "utf8"));
}

function saveSnapshot(s) {
  fs.mkdirSync(DATA, { recursive: true });
  fs.writeFileSync(SNAPSHOT, JSON.stringify(s, null, 2));
}

async function getDrive() {
  const proxy = process.env.GOOGLE_MCP_PROXY || "socks5h://127.0.0.1:10808";
  google.options({ agent: new SocksProxyAgent(proxy) });
  const creds = JSON.parse(fs.readFileSync("/home/pi/.config/google-mcp/credentials.json")).installed;
  const token = JSON.parse(fs.readFileSync("/home/pi/.local/share/google-mcp/tokens.json"));
  const oauth2 = new google.auth.OAuth2(creds.client_id, creds.client_secret);
  oauth2.setCredentials(token.default || token);
  return google.drive({ version: "v3", auth: oauth2 });
}

async function findLiveDocOnDrive(drive) {
  const q = `'${FOLDER_ID}' in parents and name = '${LIVE_MD_NAME}' and trashed = false`;
  const res = await drive.files.list({ q, fields: "files(id,name)", pageSize: 5 });
  return res.data.files?.[0]?.id || null;
}

async function uploadLiveDoc(drive, content, fileId) {
  if (fileId) {
    await drive.files.update({
      fileId,
      media: { mimeType: "text/markdown", body: content },
    });
    return fileId;
  }
  const res = await drive.files.create({
    requestBody: { name: LIVE_MD_NAME, parents: [FOLDER_ID], mimeType: "text/markdown" },
    media: { mimeType: "text/markdown", body: content },
    fields: "id",
  });
  return res.data.id;
}

function buildLiveMarkdown(checkResult, snapshot, tctx) {
  const now = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  const b = CONFIG.contractBaseline;
  let md = `# Мониторинг сайта КИПУ — живая сводка

> **Студент:** ${CONFIG.student} · ${CONFIG.specialty}  
> **Сайт:** ${CONFIG.site} · **ЭИОС:** https://st.kipu-rc.ru/user  
> ${specialtyHeaderLine()}  
> ${temporalHeaderLine(tctx)}  
> **Автопроверка:** раз в неделю (понедельник 09:00) + по запросу  
> **Последняя проверка:** ${now} (MSK)

---

## База из договора (для сравнения)

| Параметр | Значение в договоре |
|----------|---------------------|
| Договор | № ${b.contractNo} от ${b.contractDate} |
| Стоимость (старый договор) | ${b.yearCostOld} / год |
| Стоимость (актуальная) | ${b.yearCostNew} / год, ${b.semesterCost} / семестр |
| График оплаты | ${b.paymentDates} |
| Сайт для объявлений | ${b.siteUrl} |
| Л/с (реквизиты 2026) | ${b.personalAccount || "—"} |
| Счёт / БИК | ${b.bankAccount || "—"} / ${b.bik || "—"} |

> Если на сайте появится **другая сумма, приказ, срок или правило** — фиксируется ниже.

---

## Статус последней проверки

`;

  if (checkResult.changes.length === 0) {
    md += `**Изменений не обнаружено** — все отслеживаемые страницы совпадают с прошлым снимком.\n\n`;
  } else {
    md += `**⚠️ Обнаружены изменения:** ${checkResult.changes.length} страниц(а)\n\n`;
    for (const ch of checkResult.changes) {
      md += `### ${ch.title}\n`;
      md += `- URL: ${ch.url}\n`;
      if (ch.newLinks?.length) {
        md += `- **Новые/изменённые ссылки:**\n`;
        for (const l of ch.newLinks.slice(0, 15)) {
          md += `  - [${l.text}](${l.href})\n`;
        }
      }
      if (ch.textChanged) md += `- **Текст страницы изменился** (хеш ${ch.oldHash} → ${ch.newHash})\n`;
      md += `\n`;
    }
  }

  md += `---\n\n## Журнал изменений\n\n`;
  const journal = [...(snapshot.journal || []), ...checkResult.journalEntries].slice(-30);
  if (journal.length === 0) {
    md += `_Пока записей нет — базовый снимок создан ${now}._\n\n`;
  } else {
    for (const e of journal.reverse()) {
      md += `### ${e.date}\n${e.summary}\n\n`;
    }
  }

  md += `---\n\n## Отслеживаемые страницы\n\n`;
  md += `| Раздел | URL | Проверено |\n|--------|-----|----------|\n`;
  for (const p of CONFIG.pages) {
    const ps = checkResult.pageStatus[p.id];
    md += `| ${p.title} | ${p.url} | ${ps?.checkedAt?.slice(0, 16).replace("T", " ") || "—"} |\n`;
  }

  md += `\n---\n\n## Полезные ссылки (не мониторятся автоматически)\n\n`;
  md += `- [Платные услуги / стоимость](https://kipu-rc.ru/sveden/paid_edu/)\n`;
  md += `- [Расписание ${tctx.academicLabel}](https://kipu-rc.ru/student/2015-09-02-07-28-16)\n`;
  md += `- [Документы вуза](https://kipu-rc.ru/sveden/document/)\n`;
  md += `- [ЭИОС — личный кабинет](https://st.kipu-rc.ru/user) _(нужен логин студента)_\n`;
  md += `\n*Файл обновляется автоматически скриптом \`artem-study-drive/scripts/site-monitor.mjs\`*\n`;

  return { md, journal };
}

async function main() {
  const tctx = getTemporalContext();
  const snapshot = loadSnapshot();
  const checkResult = { changes: [], journalEntries: [], pageStatus: {} };
  const newPages = { ...snapshot.pages };
  const yearKw = [String(tctx.year), String(tctx.year + 1), String(tctx.academicStartYear), String(tctx.academicEndYear)];

  for (const page of CONFIG.pages) {
    log(`fetch ${page.id}`);
    let data;
    try {
      data = await fetchPage(page.url);
    } catch (e) {
      log(`ERR ${page.id}: ${e.message}`);
      checkResult.pageStatus[page.id] = { error: e.message };
      continue;
    }

    const textHash = hashText(data.text);
    const keywords = [...page.keywords, ...yearKw];
    let relevantLinks = filterByKeywords(data.links, keywords).filter(
      (l) => isTemporallyRelevant(l.href, l.text, "") && isSpecialtyRelevant(l.href, l.text, "")
    );
    const linkKey = (l) => `${l.href}|${l.text}`;
    const prev = snapshot.pages?.[page.id];

    checkResult.pageStatus[page.id] = {
      checkedAt: data.fetchedAt,
      textHash,
      relevantLinkCount: relevantLinks.length,
    };

    newPages[page.id] = {
      title: page.title,
      url: page.url,
      checkedAt: data.fetchedAt,
      textHash,
      relevantLinks,
      topText: data.text.slice(0, 800),
    };

    if (!prev) {
      log(`baseline ${page.id}`);
      continue;
    }

    const prevKeys = new Set((prev.relevantLinks || []).map(linkKey));
    const newLinks = relevantLinks.filter((l) => !prevKeys.has(linkKey(l.href + "|" + l.text)));
    const textChanged = prev.textHash !== textHash;

    if (newLinks.length || textChanged) {
      checkResult.changes.push({
        id: page.id,
        title: page.title,
        url: page.url,
        newLinks,
        textChanged,
        oldHash: prev.textHash,
        newHash: textHash,
      });
      const summary = [
        `**${page.title}** (${page.url}):`,
        newLinks.length ? `новые ссылки: ${newLinks.map((l) => l.text).slice(0, 5).join("; ")}` : null,
        textChanged ? "изменился текст страницы" : null,
      ]
        .filter(Boolean)
        .join(" ");
      checkResult.journalEntries.push({
        date: new Date().toISOString().slice(0, 10),
        summary,
      });
    }
  }

  snapshot.pages = newPages;
  snapshot.lastCheck = new Date().toISOString();

  const { md, journal } = buildLiveMarkdown(checkResult, snapshot, tctx);
  snapshot.journal = journal;
  saveSnapshot(snapshot);
  fs.writeFileSync(LIVE_MD_LOCAL, md);

  // Upload to Drive
  const drive = await getDrive();
  let driveId = snapshot.liveDocDriveId || (await findLiveDocOnDrive(drive));
  driveId = await uploadLiveDoc(drive, md, driveId);
  snapshot.liveDocDriveId = driveId;
  saveSnapshot(snapshot);

  if (checkResult.changes.length) {
    const lines = [
      `- [pending] artem-study — изменения на kipu-rc.ru (${checkResult.changes.length} стр.)`,
      ...checkResult.changes.map((c) => `  - ${c.title}: ${c.newLinks?.length || 0} новых ссылок, textΔ=${c.textChanged}`),
      `- Смотреть: ${LIVE_MD_NAME} на Drive`,
    ];
    fs.mkdirSync(path.dirname(PENDING), { recursive: true });
    fs.appendFileSync(PENDING, `\n## ${new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" })}\n${lines.join("\n")}\n`);
  }

  fs.writeFileSync(
    CHANGES,
    JSON.stringify({ checkedAt: snapshot.lastCheck, changes: checkResult.changes, driveId }, null, 2)
  );

  console.log(JSON.stringify({ ok: true, changes: checkResult.changes.length, driveId }, null, 2));
}

main().catch((e) => {
  log(`FATAL ${e.message}`);
  process.exit(1);
});
