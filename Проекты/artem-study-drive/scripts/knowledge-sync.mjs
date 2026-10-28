#!/usr/bin/env node
/** Сборка единого справочника на Drive — база для ответов на любые вопросы об учёбе. */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { google } from "/home/pi/Projects/google-mcp/node_modules/googleapis/build/src/index.js";
import { SocksProxyAgent } from "/home/pi/Projects/google-mcp/node_modules/socks-proxy-agent/dist/index.js";
import { getTemporalContext, isTemporallyRelevant, temporalHeaderLine } from "./temporal-filter.mjs";
import { isSpecialtyRelevant, specialtyHeaderLine } from "./specialty-filter.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const KB = JSON.parse(fs.readFileSync(path.join(ROOT, "config/knowledge-base.json"), "utf8"));
const FOLDER_ID = KB.meta.driveFolderId;
const REF_NAME = KB.driveFiles.masterReference;
const REF_LOCAL = path.join(DATA, REF_NAME);
const LOG = path.join(process.env.HOME, "logs/artem-study-drive.log");

function log(msg) {
  const line = `${new Date().toISOString()} knowledge-sync: ${msg}\n`;
  fs.mkdirSync(path.dirname(LOG), { recursive: true });
  fs.appendFileSync(LOG, line);
  console.log(msg);
}

function readJson(p, fallback = null) {
  if (!fs.existsSync(p)) return fallback;
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return fallback;
  }
}

function readText(p) {
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p, "utf8");
}

function extractSection(md, heading) {
  if (!md) return null;
  const re = new RegExp(`## ${heading}[\\s\\S]*?(?=\\n## |$)`, "i");
  const m = md.match(re);
  return m ? m[0].trim() : null;
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

async function uploadRef(drive, content, fileId) {
  if (fileId) {
    await drive.files.update({ fileId, media: { mimeType: "text/markdown", body: content } });
    return fileId;
  }
  const res = await drive.files.create({
    requestBody: { name: REF_NAME, parents: [FOLDER_ID], mimeType: "text/markdown" },
    media: { mimeType: "text/markdown", body: content },
    fields: "id",
  });
  return res.data.id;
}

function buildReference(ctx, tctx) {
  const now = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  const s = KB.student;
  const p = KB.payment;
  const c = KB.contract;
  const r = p.requisites;

  return `# Справочник КИПУ — ${s.fullName}

> **Единая база для ответов** на вопросы об учёбе, успеваемости, оплате, аккредитации и т.д.  
> **Обновлено:** ${now} (MSK) · ${specialtyHeaderLine()}  
> ${temporalHeaderLine(tctx)}  
> **Анализ:** раз в неделю + по запросу  
> **Папка Drive:** https://drive.google.com/drive/folders/${FOLDER_ID}

---

## Быстрые ответы

| Тема | Актуально |
|------|-----------|
| Специальность | **${s.specialtyCode}** «${s.specialtyName}» |
| Подразделение | ${s.unit} · ${s.form} · курс ${s.course}${s.group ? ` · группа **${s.group}**` : " · _группа не указана_"} |
| Стоимость года | **${p.yearCostActual}** (в договоре №${c.no}: ${c.yearCostInContract}) |
| За семестр | **${p.semesterCost}** |
| Сроки оплаты | ${p.dates.join(" и ")} |
| Договор | № ${c.no} от ${c.date} · ${c.totalCost} за ${c.duration} |
| Л/с | \`${r.personalAccount}\` |
| Счёт / БИК | \`${r.account}\` / \`${r.bik}\` |
| ЭИОС | ${KB.institution.eios} |
| Куратор | ${KB.contacts.curator.name} · ${KB.contacts.curator.phone} |
| Успеваемость | ${ctx.academicStatus} |
| Изменения на сайте | ${ctx.siteChanges} |

---

## 1. Студент и учёба

| | |
|--|--|
| ФИО | ${s.fullName} (${s.shortName}) |
| Учреждение | ${KB.institution.short} |
| Адрес | ${KB.institution.address} |
| Сайт | ${KB.institution.site} |
| Раздел ЦСПО | ${KB.institution.cspoStudent} |
| ЭИОС | ${KB.institution.eios} _(логин студента)_ |

Подробности: \`${KB.driveFiles.summary}\`

---

## 2. Оплата и реквизиты

> ⚠️ **Источник истины — только загруженные файлы на Drive** (договор, чеки, реквизиты). Ниже — справочно из сводки; при расхождении верны **файлы**.

| Параметр | Значение |
|----------|----------|
| Стоимость (актуальная) | **${p.yearCostActual}** / год · **${p.semesterCost}** / семестр |
| В договоре №${c.no} | ${c.yearCostInContract} |
| График | ${p.dates.join(", ")} |
| Оплачено | ${p.firstPaymentDone} |
| Л/с | \`${r.personalAccount}\` |
| Счёт | \`${r.account}\` |
| БИК | \`${r.bik}\` |

Страница стоимости: https://kipu-rc.ru/sveden/paid_edu/

---

## 3. Договор

> ⚠️ **Читать файл на Drive** — \`${c.driveFile}\`. Ответы только из загруженного договора.

| | |
|--|--|
| № / дата | **${c.no}** от **${c.date}** |
| Сумма за срок | ${c.totalCost} · ${c.duration} |
| Файл | \`${c.driveFile}\` |
| Примечание | ${c.note} |

---

## 4. Успеваемость и аттестация

**Статус:** ${ctx.academicStatus}

Файл: \`${KB.driveFiles.academic}\`

${ctx.academicExcerpt || ""}

Аттестация ЦСПО: ${KB.institution.cspoStudent}

---

## 5. Расписание

- https://kipu-rc.ru/student/2015-09-02-07-28-16
- ${KB.institution.cspoStudent}

${ctx.scheduleNote}

---

## 6. Аккредитация и лицензия

| | |
|--|--|
| Основные сведения | ${KB.accreditation.licensePage} |
| Документы | ${KB.accreditation.documentsPage} |
| Лицензия | ${KB.accreditation.licenseRegistry} |
| Аккредитация | ${KB.accreditation.accreditationRegistry} |

${KB.accreditation.note}

---

## 7. Контакты

| | |
|--|--|
| Куратор | **${KB.contacts.curator.name}** · ${KB.contacts.curator.phone} · ${KB.contacts.curator.hours} |
| Email родителя | ${KB.contacts.parentEmail} |

---

## 8. Компенсация и вычет

- ${KB.support.compensation393}
- ${KB.support.taxDeduction}

---

## 9. Файлы на Drive (${ctx.driveFileCount})

Проверка: **${ctx.driveLastCheck || "—"}**

${ctx.driveFileList || "_—_"}

---

## 10. Журнал изменений на сайте

${ctx.siteJournal || "_Изменений нет._"}

Полный мониторинг: \`${KB.driveFiles.siteMonitor}\`

---

## 11. Автомониторинг

| Что | Когда |
|-----|-------|
| Drive + сайт + успеваемость + справочник | **Понедельник 09:00 MSK** (раз в неделю) |

Темы: ${KB.monitorTopics.join(" · ")}

Email: ${KB.contacts.parentEmail} — негативные списки, важные изменения.

---

## 12. Правило для агента

> **${KB.agentPolicy?.documentsPrimary || "Договоры и документы — только файлы на Drive."}**  
> **${KB.agentPolicy?.siteFor || "Сайт — успеваемость и изменения."}**  
> **${KB.agentPolicy?.temporal || "Только текущий учебный год и будущее."}**  
> **${KB.agentPolicy?.specialty || "Только 09.02.07."}**

Порядок чтения: ${(KB.agentPolicy?.readOrder || []).map((f) => `\`${f}\``).join(" → ")}

*Зафиксировано: ${KB.agentPolicy?.recordedAt || "—"} · ${KB.agentPolicy?.requestedBy || "родитель"}*

---

*Собирается: artem-study-drive/scripts/knowledge-sync.mjs*
`;
}

async function main() {
  const tctx = getTemporalContext();
  const siteSnap = readJson(path.join(DATA, "site-snapshot.json"), {});
  const academicSnap = readJson(path.join(DATA, "academic-snapshot.json"), {});
  const lastCheck = readJson(path.join(DATA, "last-check.json"), {});
  const manifest = readJson(path.join(DATA, "manifest.json"), { files: {} });
  const siteChanges = readJson(path.join(DATA, "site-changes.json"), {});
  const academicMd = readText(path.join(DATA, "00_Успеваемость_Артём.md"));

  const academicDocs = Object.values(academicSnap.documents || {}).filter(
    (d) =>
      isTemporallyRelevant(d.url, d.title || "", "", tctx) &&
      isSpecialtyRelevant(d.url, d.title || "", "", {
        studentFound: d.studentFound,
        group: KB.student.group,
      })
  );
  const studentInNegative = academicDocs.some((d) => d.studentFound && d.classification === "negative");
  const studentInPositive = academicDocs.some((d) => d.studentFound && d.classification === "positive");
  let academicStatus = "ФИО в списках **не найдено**";
  if (studentInNegative) academicStatus = "⚠️ **в проблемном списке**";
  else if (studentInPositive) academicStatus = "✓ в списке допущенных";

  const changesCount = siteChanges.changes?.length ?? 0;
  const siteChangesText = changesCount > 0 ? `**${changesCount} изменений**` : "нет";

  const journal = (siteSnap.journal || []).slice(-8).reverse();
  const siteJournal = journal.length ? journal.map((e) => `- **${e.date}** — ${e.summary}`).join("\n") : null;

  const driveFiles = Object.values(manifest.files || {});

  const ctx = {
    academicStatus,
    academicExcerpt: extractSection(academicMd, "Текущий статус"),
    siteChanges: siteChangesText,
    siteJournal,
    driveFileCount: driveFiles.length,
    driveFileList: driveFiles.slice(0, 25).map((f) => `- \`${f.name}\``).join("\n") || null,
    driveLastCheck: lastCheck.checkedAt
      ? new Date(lastCheck.checkedAt).toLocaleString("ru-RU", { timeZone: "Europe/Moscow" })
      : null,
    scheduleNote: siteSnap.pages?.schedule
      ? `_Расписание проверено: ${siteSnap.pages.schedule.checkedAt?.slice(0, 10) || "—"}_`
      : "",
  };

  const md = buildReference(ctx, tctx);
  fs.mkdirSync(DATA, { recursive: true });
  fs.writeFileSync(REF_LOCAL, md);

  const statePath = path.join(DATA, "knowledge-sync-state.json");
  const state = readJson(statePath, {});
  const drive = await getDrive();
  const driveId = await uploadRef(drive, md, state.driveId || null);
  fs.writeFileSync(statePath, JSON.stringify({ driveId, syncedAt: new Date().toISOString() }, null, 2));

  log(`synced → ${driveId}`);
  console.log(JSON.stringify({ ok: true, driveId }, null, 2));
}

main().catch((e) => {
  log(`FATAL ${e.message}`);
  process.exit(1);
});
