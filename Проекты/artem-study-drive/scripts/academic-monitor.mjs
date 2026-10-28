#!/usr/bin/env node
/** Мониторинг успеваемости: списки допуска / неуспевающих на kipu-rc.ru → Drive + email. */
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { google } from "/home/pi/Projects/google-mcp/node_modules/googleapis/build/src/index.js";
import { SocksProxyAgent } from "/home/pi/Projects/google-mcp/node_modules/socks-proxy-agent/dist/index.js";
import {
  getTemporalContext,
  isTemporallyRelevant,
  purgeStaleDocuments,
  temporalHeaderLine,
} from "./temporal-filter.mjs";
import {
  isSpecialtyRelevant,
  mentionsOurSpecialty,
  purgeOtherSpecialtyDocuments,
  specialtyHeaderLine,
} from "./specialty-filter.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const TMP = path.join(DATA, "tmp");
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, "config/academic-track.json"), "utf8"));
const SNAPSHOT = path.join(DATA, "academic-snapshot.json");
const LIVE_MD_LOCAL = path.join(DATA, "00_Успеваемость_Артём.md");
const FOLDER_ID = "1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V";
const LIVE_MD_NAME = "00_Успеваемость_Артём.md";
const PENDING = path.join(process.env.HOME, "logs/cursor-work/pending-artem-study.md");
const LOG = path.join(process.env.HOME, "logs/artem-study-drive.log");

function log(msg) {
  const line = `${new Date().toISOString()} academic-monitor: ${msg}\n`;
  fs.mkdirSync(path.dirname(LOG), { recursive: true });
  fs.appendFileSync(LOG, line);
  console.log(msg);
}

function hashText(s) {
  return crypto.createHash("sha256").update(s).digest("hex").slice(0, 16);
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
    const text = stripHtml(m[2]).slice(0, 300);
    if (!text || href.startsWith("#") || href.startsWith("javascript:") || href.startsWith("mailto:")) continue;
    try {
      href = new URL(href, baseUrl).href;
    } catch {
      continue;
    }
    links.push({ href, text });
  }
  return links;
}

function matchesKeywords(blob, keywords) {
  const low = blob.toLowerCase();
  return keywords.some((k) => low.includes(k.toLowerCase()));
}

function isExcluded(url, title) {
  const blob = `${url} ${title}`.toLowerCase();
  for (const p of CONFIG.excludeUrlPatterns || []) {
    if (blob.includes(p.toLowerCase())) return true;
  }
  for (const p of CONFIG.excludeTitlePatterns || []) {
    if (title.toLowerCase().includes(p.toLowerCase())) return true;
  }
  return false;
}

function isStrongPerformanceList(title, text) {
  return matchesKeywords(`${title}\n${text.slice(0, 8000)}`, CONFIG.strongListKeywords || []);
}

function classifyDocument(title, text) {
  const blob = `${title} ${text.slice(0, 4000)}`.toLowerCase();
  if (!isStrongPerformanceList(title, text)) return "neutral";
  let negative = 0;
  let positive = 0;
  for (const kw of CONFIG.listKeywords.negative) if (blob.includes(kw)) negative++;
  for (const kw of CONFIG.listKeywords.positive) if (blob.includes(kw)) positive++;
  if (negative > positive && negative > 0) return "negative";
  if (positive > 0) return "positive";
  return "neutral";
}

function findStudentMentions(text) {
  const lines = text.split(/\r?\n/);
  const mentions = [];
  const seen = new Set();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const p of CONFIG.namePatterns) {
      if (!line.toLowerCase().includes(p.toLowerCase())) continue;
      const key = `${i}:${line.trim()}`;
      if (seen.has(key)) continue;
      seen.add(key);
      mentions.push({
        line: line.trim(),
        context: lines.slice(Math.max(0, i - 2), Math.min(lines.length, i + 4)).join("\n").trim(),
      });
    }
  }
  return mentions;
}

function isRelevantDocument(title, text, studentFound) {
  if (isExcluded("", title)) return false;
  if (
    !isSpecialtyRelevant("", title, text, {
      studentFound,
      group: CONFIG.group,
    })
  ) {
    return false;
  }
  if (studentFound) return true;
  if (!isStrongPerformanceList(title, text)) return false;
  const blob = `${title}\n${text.slice(0, 6000)}`.toLowerCase();
  if (blob.includes(CONFIG.specialtyCode.toLowerCase())) return true;
  if (CONFIG.group && CONFIG.groupPatterns.length) {
    if (CONFIG.groupPatterns.some((p) => blob.includes(p.toLowerCase()))) return true;
  }
  if (/акadem zadolzhen|акademическ задолжен|неуспевающ|допущен к аттестации/i.test(blob)) {
    return mentionsOurSpecialty(blob) || CONFIG.group;
  }
  return false;
}

function isAllowedHost(url) {
  try {
    const host = new URL(url).hostname;
    if (host.includes(CONFIG.crawl.hostPattern)) return true;
    for (const h of CONFIG.crawl.extraHosts || []) {
      if (host.includes(h)) return true;
    }
    return false;
  } catch {
    return false;
  }
}

async function fetchUrl(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": "artem-study-academic/1.0 (Pi5; family use)" },
    redirect: "follow",
    signal: AbortSignal.timeout(60000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const contentType = res.headers.get("content-type") || "";
  const buf = Buffer.from(await res.arrayBuffer());
  return { contentType, buf };
}

function extractPdfText(buf) {
  fs.mkdirSync(TMP, { recursive: true });
  const pdfPath = path.join(TMP, `_${Date.now()}_${Math.random().toString(36).slice(2)}.pdf`);
  fs.writeFileSync(pdfPath, buf);
  const out = spawnSync("pdftotext", ["-layout", pdfPath, "-"], {
    encoding: "utf8",
    maxBuffer: 12 * 1024 * 1024,
  });
  try {
    fs.unlinkSync(pdfPath);
  } catch {
    /* ignore */
  }
  if (out.error) throw out.error;
  return (out.stdout || "").trim();
}

async function fetchDocument(url, linkText = "") {
  const { contentType, buf } = await fetchUrl(url);
  const isPdf = contentType.includes("pdf") || /\.pdf($|\?)/i.test(url);
  let text = "";
  let title = linkText || url.split("/").pop() || url;

  if (isPdf) {
    text = extractPdfText(buf);
  } else if (contentType.includes("html") || !contentType) {
    const html = buf.toString("utf8");
    text = stripHtml(html);
    const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
    if (titleMatch) title = stripHtml(titleMatch[1]) || title;
  } else {
    return null;
  }

  return { url, title, text, contentHash: hashText(text), fetchedAt: new Date().toISOString() };
}

function loadSnapshot() {
  if (!fs.existsSync(SNAPSHOT)) {
    return { documents: {}, emailedAlerts: [], liveDocDriveId: null, journal: [], baselineEstablished: false };
  }
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

function sendEmail(subject, body) {
  const script = CONFIG.emailFromScript;
  if (!fs.existsSync(script)) {
    log(`email skip: no ${script}`);
    return false;
  }
  const r = spawnSync(script, [subject, body, CONFIG.emailTo], { encoding: "utf8" });
  if (r.status !== 0) {
    log(`email ERR: ${r.stderr || r.stdout}`);
    return false;
  }
  log(`email sent: ${subject}`);
  return true;
}

function buildLiveMarkdown(snapshot, runResult, tctx) {
  const now = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  const groupLine = CONFIG.group
    ? `**Группа:** ${CONFIG.group}`
    : "**Группа:** _не указана — только специальность 09.02.07_";

  let md = `# Успеваемость — Шпак Артём Михайлович

> **КИПУ · 09.02.07 «Информационные системы и программирование»** · колледж/ЦСПО  
> ${groupLine} · **Курс:** ${CONFIG.course ?? "—"}  
> ${specialtyHeaderLine()}  
> ${temporalHeaderLine(tctx)}  
> **ЭИОС (оценки):** https://st.kipu-rc.ru/user _(нужен логин студента)_  
> **Автопроверка:** раз в неделю (понедельник 09:00) + по запросу  
> **Последняя проверка:** ${now} (MSK)

---

## Текущий статус

`;

  const docs = Object.values(snapshot.documents || {}).filter(
    (d) =>
      !isExcluded(d.url, d.title) &&
      isTemporallyRelevant(d.url, d.title, "", tctx) &&
      isSpecialtyRelevant(d.url, d.title, "", {
        studentFound: d.studentFound,
        group: CONFIG.group,
      })
  );
  const attestationDocs = docs.filter((d) =>
    /аттестац|rasp_zima|promежut/i.test(`${d.title} ${d.url}`)
  );
  const withStudent = docs.filter((d) => d.studentFound);
  const negative = withStudent.filter((d) => d.classification === "negative");
  const positive = withStudent.filter((d) => d.classification === "positive");

  if (negative.length) {
    md += `### ⚠️ Внимание — найден в «проблемных» списках\n\n`;
    for (const d of negative) {
      md += `- **[${d.title}](${d.url})** — проверено ${d.lastChecked?.slice(0, 10) || "—"}\n`;
      for (const m of d.mentions || []) {
        md += `  - \`${m.line.slice(0, 120)}\`\n`;
      }
    }
    md += `\n`;
  } else if (withStudent.length === 0) {
    md += `**ФИО в опубликованных списках пока не найдено** — это нормально, если колледж ещё не выкладывал списки по вашему курсу/группе.\n\n`;
  } else {
    md += `**В списках неуспевающих / с задолженностью не числится** (по данным сайта на дату проверки).\n\n`;
  }

  if (positive.length) {
    md += `### ✓ Допуск / положительные списки\n\n`;
    for (const d of positive) {
      md += `- [${d.title}](${d.url})\n`;
      for (const m of d.mentions || []) {
        md += `  - \`${m.line.slice(0, 120)}\`\n`;
      }
    }
    md += `\n`;
  }

  if (attestationDocs.length) {
    md += `### 📅 Расписание промежуточной аттестации (ЦСПО)\n\n`;
    for (const d of attestationDocs) {
      md += `- [${d.title}](${d.url})\n`;
    }
    md += `\n> Полный раздел: https://kipu-rc.ru/studentu-tsspo\n\n`;
  }

  const watchDocs = docs.filter((d) => !d.studentFound && d.relevant && d.classification !== "neutral");
  if (watchDocs.length) {
    md += `### 👀 Новые списки по направлению (ФИО не найдено — проверить вручную)\n\n`;
    for (const d of watchDocs.slice(0, 15)) {
      md += `- [${d.title}](${d.url}) — _${d.classification}_\n`;
    }
    md += `\n`;
  }

  md += `---\n\n## Проверенные документы\n\n`;
  if (docs.length === 0) {
    md += `_Пока нет сохранённых документов — первый проход создаёт базу._\n\n`;
  } else {
    md += `| Документ | Тип | ФИО | Обновлено |\n|----------|-----|-----|----------|\n`;
    for (const d of docs.sort((a, b) => (b.lastChecked || "").localeCompare(a.lastChecked || "")).slice(0, 40)) {
      const icon = d.classification === "negative" ? "⚠️" : d.classification === "positive" ? "✓" : "·";
      const name = d.studentFound ? "**да**" : "—";
      md += `| [${d.title.slice(0, 60)}](${d.url}) | ${icon} ${d.classification} | ${name} | ${d.lastChecked?.slice(0, 10) || "—"} |\n`;
    }
    md += `\n`;
  }

  md += `---\n\n## Журнал\n\n`;
  const journal = [...(snapshot.journal || [])].slice(-25).reverse();
  if (journal.length === 0) {
    md += `_Записей пока нет._\n\n`;
  } else {
    for (const e of journal) {
      md += `- **${e.date}** — ${e.summary}\n`;
    }
    md += `\n`;
  }

  md += `---\n\n## Как это работает\n\n`;
  md += `1. Скрипт ищет на **kipu-rc.ru** страницы и PDF со словами «допущен», «неуспевающ», «аттестация», «09.02.07».\n`;
  md += `2. Ищет **Шпак Артём** в тексте; при попадании в негативный список — **письмо на ${CONFIG.emailTo}**.\n`;
  md += `3. Когда станет известен **номер группы** — добавить в \`config/academic-track.json\` для точной фильтрации.\n`;
  md += `4. Оценки по предметам — только через **ЭИОС** (логин студента).\n`;
  md += `5. **Прошлые учебные годы не учитываются** — только ${tctx.academicLabel} и будущее.\n`;
  md += `6. **Только специальность 09.02.07** — другие программы КИПУ не мониторятся.\n\n`;
  md += `*Обновляется \`artem-study-drive/scripts/academic-monitor.mjs\`*\n`;

  if (runResult?.errors?.length) {
    md += `\n---\n\n<details><summary>Ошибки последнего прогона (${runResult.errors.length})</summary>\n\n`;
    for (const e of runResult.errors.slice(0, 10)) {
      md += `- ${e}\n`;
    }
    md += `\n</details>\n`;
  }

  return md;
}

async function discoverCandidateUrls() {
  const seen = new Set();
  const candidates = [];
  const queue = CONFIG.seedUrls.map((url) => ({ url, depth: 0, text: "" }));

  for (const url of CONFIG.policyDocs || []) {
    queue.push({ url, depth: 0, text: "Положение об успеваемости" });
  }

  while (queue.length && candidates.length < CONFIG.crawl.maxPages) {
    const item = queue.shift();
    if (!item || seen.has(item.url)) continue;
    seen.add(item.url);

    if (!isAllowedHost(item.url) || isExcluded(item.url, item.text)) continue;
    if (!isTemporallyRelevant(item.url, item.text, "")) continue;
    if (!isSpecialtyRelevant(item.url, item.text, "", { group: CONFIG.group })) continue;

    const blob = `${item.text} ${item.url}`;
    const isPdf = /\.pdf($|\?)/i.test(item.url);
    const interesting =
      isPdf ||
      matchesKeywords(blob, CONFIG.linkKeywords) ||
      matchesKeywords(blob, CONFIG.strongListKeywords || []);

    if (interesting) {
      candidates.push({ url: item.url, title: item.text || item.url.split("/").pop() });
    }

    if (item.depth >= CONFIG.crawl.maxDepth || isPdf) continue;

    try {
      const { contentType, buf } = await fetchUrl(item.url);
      if (!contentType.includes("html") && !contentType.includes("text/html")) continue;
      const html = buf.toString("utf8");
      const links = extractLinks(html, item.url);
      for (const l of links) {
        if (!isAllowedHost(l.href) || isExcluded(l.href, l.text)) continue;
        if (!isTemporallyRelevant(l.href, l.text, "")) continue;
        if (!isSpecialtyRelevant(l.href, l.text, "", { group: CONFIG.group })) continue;
        if (
          matchesKeywords(`${l.text} ${l.href}`, CONFIG.linkKeywords) ||
          matchesKeywords(`${l.text} ${l.href}`, CONFIG.strongListKeywords || [])
        ) {
          queue.push({ url: l.href, depth: item.depth + 1, text: l.text });
        }
      }
    } catch (e) {
      log(`crawl skip ${item.url}: ${e.message}`);
    }
  }

  return candidates;
}

function appendPending(lines) {
  fs.mkdirSync(path.dirname(PENDING), { recursive: true });
  const ts = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  fs.appendFileSync(PENDING, `\n## ${ts}\n${lines.join("\n")}\n`);
}

async function main() {
  const tctx = getTemporalContext();
  const snapshot = loadSnapshot();
  snapshot.documents = snapshot.documents || {};
  snapshot.emailedAlerts = snapshot.emailedAlerts || [];
  snapshot.journal = snapshot.journal || [];

  const purged = purgeStaleDocuments(snapshot.documents, tctx);
  snapshot.documents = purged.documents;
  if (purged.removed) log(`purged stale docs: ${purged.removed}`);

  const specPurged = purgeOtherSpecialtyDocuments(snapshot.documents, { group: CONFIG.group });
  snapshot.documents = specPurged.documents;
  if (specPurged.removed) log(`purged other specialty: ${specPurged.removed}`);

  const runResult = { scanned: 0, alerts: [], errors: [], newDocs: 0 };
  const candidates = await discoverCandidateUrls();
  log(`candidates: ${candidates.length}`);

  for (const cand of candidates) {
    if (runResult.scanned >= CONFIG.crawl.maxPages) break;

    let doc;
    try {
      doc = await fetchDocument(cand.url, cand.title);
    } catch (e) {
      runResult.errors.push(`${cand.url}: ${e.message}`);
      continue;
    }
    if (!doc || doc.text.length < 20) continue;
    if (isExcluded(doc.url, doc.title)) continue;
    if (!isTemporallyRelevant(doc.url, doc.title, doc.text, tctx)) {
      log(`skip stale: ${doc.title.slice(0, 60)}`);
      continue;
    }
    if (!isSpecialtyRelevant(doc.url, doc.title, doc.text, { group: CONFIG.group })) {
      log(`skip other specialty: ${doc.title.slice(0, 60)}`);
      continue;
    }

    runResult.scanned++;
    const mentions = findStudentMentions(doc.text);
    const studentFound = mentions.length > 0;
    const relevant = isRelevantDocument(doc.title, doc.text, studentFound);
    if (!relevant && !matchesKeywords(`${doc.title} ${doc.text.slice(0, 500)}`, CONFIG.linkKeywords)) {
      continue;
    }

    const classification = classifyDocument(doc.title, doc.text);
    const prev = snapshot.documents[doc.url];
    const contentChanged = !prev || prev.contentHash !== doc.contentHash;
    const newlyFoundStudent = studentFound && (!prev || !prev.studentFound);
    const newlyNegative = studentFound && classification === "negative" && contentChanged;

    snapshot.documents[doc.url] = {
      url: doc.url,
      title: doc.title,
      contentHash: doc.contentHash,
      classification,
      studentFound,
      mentions,
      relevant,
      firstSeen: prev?.firstSeen || doc.fetchedAt,
      lastChecked: doc.fetchedAt,
    };

    if (!prev) runResult.newDocs++;

    const journalBits = [];
    if (newlyFoundStudent) journalBits.push(`ФИО найдено: ${doc.title}`);
    if (newlyNegative) journalBits.push(`⚠️ негативный список: ${doc.title}`);
    if (contentChanged && prev) journalBits.push(`обновлён: ${doc.title}`);
    if (journalBits.length) {
      snapshot.journal.push({
        date: new Date().toISOString().slice(0, 10),
        summary: journalBits.join("; "),
      });
    }

    const alertKey = (type) => `${doc.url}|${doc.contentHash}|${type}`;

    if (newlyNegative && !snapshot.emailedAlerts.includes(alertKey("negative"))) {
      const body = [
        `Артём Шпак найден в списке с признаками неуспеваемости / недопуска.`,
        ``,
        `Документ: ${doc.title}`,
        `URL: ${doc.url}`,
        ``,
        `Фрагменты:`,
        ...mentions.map((m) => m.context),
        ``,
        `Полная сводка: Google Drive → Учёба Артём → ${LIVE_MD_NAME}`,
      ].join("\n");
      if (sendEmail("⚠️ КИПУ — Артём в списке неуспевающих", body)) {
        snapshot.emailedAlerts.push(alertKey("negative"));
        runResult.alerts.push("negative");
      }
    } else if (newlyFoundStudent && classification === "positive" && !snapshot.emailedAlerts.includes(alertKey("positive"))) {
      const body = [
        `Артём Шпак найден в списке допущенных / положительном списке.`,
        ``,
        `Документ: ${doc.title}`,
        `URL: ${doc.url}`,
        ...mentions.map((m) => m.line),
      ].join("\n");
      if (sendEmail("✓ КИПУ — Артём в списке допущенных", body)) {
        snapshot.emailedAlerts.push(alertKey("positive"));
        runResult.alerts.push("positive");
      }
    } else if (
      snapshot.baselineEstablished &&
      !studentFound &&
      relevant &&
      classification !== "neutral" &&
      !prev &&
      !snapshot.emailedAlerts.includes(alertKey("watch"))
    ) {
      const body = [
        `На сайте КИПУ появился новый список по успеваемости/аттестации (09.02.07 / ЦСПО).`,
        `ФИО Шпак Артём в документе не найдено — проверьте вручную (возможно, другая группа).`,
        ``,
        `Документ: ${doc.title}`,
        `URL: ${doc.url}`,
        `Тип: ${classification}`,
      ].join("\n");
      if (sendEmail("👀 КИПУ — новый список успеваемости", body)) {
        snapshot.emailedAlerts.push(alertKey("watch"));
        runResult.alerts.push("watch");
      }
    }
  }

  snapshot.lastCheck = new Date().toISOString();
  snapshot.baselineEstablished = true;
  snapshot.journal = snapshot.journal.slice(-50);

  const md = buildLiveMarkdown(snapshot, runResult, tctx);
  fs.writeFileSync(LIVE_MD_LOCAL, md);

  const drive = await getDrive();
  let driveId = snapshot.liveDocDriveId || (await findLiveDocOnDrive(drive));
  driveId = await uploadLiveDoc(drive, md, driveId);
  snapshot.liveDocDriveId = driveId;
  saveSnapshot(snapshot);

  if (runResult.alerts.length || runResult.newDocs > 0) {
    appendPending([
      `- [pending] artem-study — успеваемость: проверено ${runResult.scanned}, новых док. ${runResult.newDocs}, алертов ${runResult.alerts.length}`,
      ...runResult.alerts.map((a) => `  - email: ${a}`),
      `- Сводка: ${LIVE_MD_NAME}`,
    ]);
  }

  log(`done: scanned=${runResult.scanned} newDocs=${runResult.newDocs} alerts=${runResult.alerts.length}`);
  console.log(JSON.stringify({ ok: true, ...runResult, driveId }, null, 2));
}

main().catch((e) => {
  log(`FATAL ${e.message}`);
  process.exit(1);
});
