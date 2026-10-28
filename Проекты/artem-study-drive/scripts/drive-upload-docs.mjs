#!/usr/bin/env node
/** Разовая загрузка/обновление markdown и переименование PDF на Drive. */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { google } from "/home/pi/Projects/google-mcp/node_modules/googleapis/build/src/index.js";
import { SocksProxyAgent } from "/home/pi/Projects/google-mcp/node_modules/socks-proxy-agent/dist/index.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const FOLDER_ID = "1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V";

const RENAMES = {
  "1AnSU0tb6usqe7278SOMoyIVs0QVZQl60": "01_Допсоглашение_№209_реквизиты_договор65_2025-12-01.pdf",
  "1FbKwubDZhpaQ9aUCsvq_EUW7nmBKvZkZ": "01_Допсоглашение_№68-с_стоимость_128700₽_договор65_2026-05-22.pdf",
};

const UPDATES = [
  { id: "1vILqQJyOIdDirbmqu05PY_A3C9RJwoQK", local: "00_Сводка_учёба_Артём.md" },
];

const CREATES = [{ local: "08_Чеклист_налоговый_вычет.md" }];

async function getDrive() {
  const proxy = process.env.GOOGLE_MCP_PROXY || "socks5h://127.0.0.1:10808";
  google.options({ agent: new SocksProxyAgent(proxy) });
  const creds = JSON.parse(fs.readFileSync("/home/pi/.config/google-mcp/credentials.json")).installed;
  const token = JSON.parse(fs.readFileSync("/home/pi/.local/share/google-mcp/tokens.json"));
  const oauth2 = new google.auth.OAuth2(creds.client_id, creds.client_secret);
  oauth2.setCredentials(token.default || token);
  return google.drive({ version: "v3", auth: oauth2 });
}

async function main() {
  const drive = await getDrive();
  const results = { renamed: [], updated: [], created: [] };

  for (const [fileId, name] of Object.entries(RENAMES)) {
    await drive.files.update({ fileId, requestBody: { name } });
    results.renamed.push({ fileId, name });
    console.log(`renamed ${fileId} → ${name}`);
  }

  for (const { id, local } of UPDATES) {
    const body = fs.readFileSync(path.join(DATA, local), "utf8");
    await drive.files.update({ fileId: id, media: { mimeType: "text/markdown", body } });
    results.updated.push({ id, local });
    console.log(`updated ${local} → ${id}`);
  }

  for (const { local } of CREATES) {
    const body = fs.readFileSync(path.join(DATA, local), "utf8");
    const res = await drive.files.create({
      requestBody: { name: local, parents: [FOLDER_ID], mimeType: "text/markdown" },
      media: { mimeType: "text/markdown", body },
      fields: "id",
    });
    results.created.push({ local, id: res.data.id });
    console.log(`created ${local} → ${res.data.id}`);
  }

  console.log(JSON.stringify(results, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
