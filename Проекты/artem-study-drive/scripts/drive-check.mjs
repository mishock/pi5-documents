#!/usr/bin/env node
/** Проверка папки «Учёба Артём» на Drive: новые файлы, подготовка аудио к транскрипции. */
import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { google } from "/home/pi/Projects/google-mcp/node_modules/googleapis/build/src/index.js";
import { SocksProxyAgent } from "/home/pi/Projects/google-mcp/node_modules/socks-proxy-agent/dist/index.js";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const MANIFEST = path.join(DATA, "manifest.json");
const REPORT = path.join(DATA, "last-check.json");
const PENDING = path.join(process.env.HOME, "logs/cursor-work/pending-artem-study.md");
const LOG = path.join(process.env.HOME, "logs/artem-study-drive.log");

export const FOLDER_ID = "1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V";
const PROXY = process.env.GOOGLE_MCP_PROXY || "socks5h://127.0.0.1:10808";
const TOKEN_PATH = "/home/pi/.local/share/google-mcp/tokens.json";
const CREDS_PATH = "/home/pi/.config/google-mcp/credentials.json";
const WHISPER_PY = "/home/pi/Documents/Проекты/ai_assistant/venv/bin/python3";
const AUDIO_RE = /\.(m4a|mp3|wav|ogg|aac|flac)$/i;

function log(msg) {
  const line = `${new Date().toISOString()} ${msg}\n`;
  fs.mkdirSync(path.dirname(LOG), { recursive: true });
  fs.appendFileSync(LOG, line);
  console.log(msg);
}

function loadManifest() {
  if (!fs.existsSync(MANIFEST)) return { files: {} };
  return JSON.parse(fs.readFileSync(MANIFEST, "utf8"));
}

function saveManifest(m) {
  fs.mkdirSync(DATA, { recursive: true });
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2));
}

async function getDrive() {
  google.options({ agent: new SocksProxyAgent(PROXY) });
  const creds = JSON.parse(fs.readFileSync(CREDS_PATH, "utf8")).installed;
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH, "utf8"));
  const oauth2 = new google.auth.OAuth2(creds.client_id, creds.client_secret);
  oauth2.setCredentials(token.default || token);
  return google.drive({ version: "v3", auth: oauth2 });
}

async function listAllFiles(drive) {
  const out = [];
  let pageToken;
  do {
    const res = await drive.files.list({
      pageSize: 100,
      pageToken,
      q: `'${FOLDER_ID}' in parents and trashed = false`,
      fields: "nextPageToken, files(id, name, mimeType, modifiedTime, size)",
      orderBy: "modifiedTime desc",
    });
    out.push(...(res.data.files || []));
    pageToken = res.data.nextPageToken;
  } while (pageToken);
  return out;
}

async function downloadFile(drive, fileId, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const res = await drive.files.get({ fileId, alt: "media" }, { responseType: "arraybuffer" });
  fs.writeFileSync(dest, Buffer.from(res.data));
}

function transcribeAudio(src, destTxt) {
  if (fs.existsSync(destTxt) && fs.statSync(destTxt).mtimeMs >= fs.statSync(src).mtimeMs) {
    return { skipped: true };
  }
  const wav = src.replace(/\.[^.]+$/, ".wav");
  spawnSync("ffmpeg", ["-y", "-i", src, "-ar", "16000", "-ac", "1", wav], {
    stdio: "ignore",
  });
  const code = spawnSync(
    WHISPER_PY,
    [
      "-c",
      `import os; os.environ.setdefault('HF_HUB_OFFLINE','1'); from pathlib import Path; from whisper_client import transcribe; print(transcribe(Path('${wav}')))`,
    ],
    {
      cwd: "/home/pi/Documents/Проекты/ai_assistant",
      env: {
        ...process.env,
        WHISPER_MODEL: process.env.WHISPER_MODEL || "small",
        WHISPER_VAD_FILTER: "0",
      },
      encoding: "utf8",
    }
  );
  if (code.status !== 0) {
    return { error: code.stderr || "whisper failed" };
  }
  fs.mkdirSync(path.dirname(destTxt), { recursive: true });
  fs.writeFileSync(destTxt, code.stdout.trim());
  return { ok: true };
}

function appendPending(lines) {
  fs.mkdirSync(path.dirname(PENDING), { recursive: true });
  const ts = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  fs.appendFileSync(PENDING, `\n## ${ts}\n${lines.join("\n")}\n`);
}

async function main() {
  const drive = await getDrive();
  const remote = await listAllFiles(drive);
  const manifest = loadManifest();
  const prev = manifest.files || {};
  const now = {};
  const added = [];
  const changed = [];

  for (const f of remote) {
    now[f.id] = {
      name: f.name,
      mimeType: f.mimeType,
      modifiedTime: f.modifiedTime,
      size: f.size,
    };
    if (!prev[f.id]) added.push(f);
    else if (prev[f.id].modifiedTime !== f.modifiedTime) changed.push(f);
  }

  const transcripts = [];
  for (const f of [...added, ...changed]) {
    if (!AUDIO_RE.test(f.name)) continue;
    const local = path.join(DATA, "downloads", `${f.id}_${f.name}`);
    const txt = path.join(DATA, "transcripts", `${f.id}.txt`);
    try {
      await downloadFile(drive, f.id, local);
      const tr = transcribeAudio(local, txt);
      if (tr.ok) transcripts.push({ name: f.name, path: txt });
      log(`audio ${f.name}: ${tr.ok ? "transcribed" : tr.skipped ? "skip" : tr.error}`);
    } catch (e) {
      log(`audio ${f.name} ERR: ${e.message}`);
    }
  }

  const report = {
    checkedAt: new Date().toISOString(),
    folderId: FOLDER_ID,
    total: remote.length,
    added: added.map((f) => ({ id: f.id, name: f.name, modifiedTime: f.modifiedTime })),
    changed: changed.map((f) => ({ id: f.id, name: f.name, modifiedTime: f.modifiedTime })),
    transcripts,
  };
  fs.mkdirSync(DATA, { recursive: true });
  fs.writeFileSync(REPORT, JSON.stringify(report, null, 2));
  manifest.files = now;
  manifest.lastCheck = report.checkedAt;
  saveManifest(manifest);

  if (added.length || changed.length) {
    const lines = [
      `- [pending] artem-study — новые/изменённые файлы на Drive (${added.length} новых, ${changed.length} измен.)`,
      ...added.map((f) => `  - NEW: ${f.name}`),
      ...changed.map((f) => `  - CHG: ${f.name}`),
      ...transcripts.map((t) => `  - AUDIO→txt: ${t.name}`),
      "- Действие агента: прочитать файлы, обновить сводку на Drive",
    ];
    appendPending(lines);
    log(`NEW ${added.length} CHG ${changed.length} → ${PENDING}`);
  } else {
    log("no changes");
  }

  console.log(JSON.stringify({ ok: true, added: added.length, changed: changed.length }, null, 2));
}

main().catch((e) => {
  log(`FATAL ${e.message}`);
  process.exit(1);
});
