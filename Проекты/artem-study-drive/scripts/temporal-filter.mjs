/** Фильтр актуальности: только текущий учебный год и будущее (MSK). */
const TZ = "Europe/Moscow";

export function getMskNow() {
  return new Date(new Date().toLocaleString("en-US", { timeZone: TZ }));
}

export function getTemporalContext(now = getMskNow()) {
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const academicStartYear = month >= 9 ? year : year - 1;
  const academicEndYear = academicStartYear + 1;

  return {
    now,
    year,
    month,
    academicStartYear,
    academicEndYear,
    academicLabel: `${academicStartYear}/${academicEndYear}`,
    minYear: academicStartYear,
    maxYear: year + 1,
    humanDate: now.toLocaleDateString("ru-RU", { timeZone: TZ }),
  };
}

export function extractYears(blob) {
  const years = new Set();
  for (const m of String(blob).matchAll(/\b(20\d{2})\b/g)) {
    years.add(parseInt(m[1], 10));
  }
  for (const m of String(blob).matchAll(/\/(20\d{2})\//g)) {
    years.add(parseInt(m[1], 10));
  }
  return [...years];
}

/** Без года в тексте/URL — считаем актуальным (общие страницы). */
export function isTimelessReference(url, title) {
  const blob = `${url} ${title}`.toLowerCase();
  return /polojenie|poloj\/|положение|лиценз|аккредит|reestr|common\/|sveden\/document/.test(blob);
}

/**
 * Актуально, если относится к текущему учебному году или будущему.
 * Прошлые годы (до academicStartYear) — отбрасываем.
 */
export function isTemporallyRelevant(url, title, text = "", ctx = getTemporalContext()) {
  const blob = `${url} ${title} ${text.slice(0, 3000)}`;

  const range = blob.match(/(20\d{2})\s*[-–/]\s*(20\d{2})/);
  if (range) {
    const start = parseInt(range[1], 10);
    return start >= ctx.academicStartYear && start <= ctx.academicEndYear + 1;
  }

  const years = extractYears(blob);
  if (years.length === 0) return true;

  const maxY = Math.max(...years);
  if (maxY < ctx.academicStartYear) return false;

  return true;
}

export function filterEntries(entries, getFields, ctx = getTemporalContext()) {
  return entries.filter((e) => {
    const { url = "", title = "", text = "" } = getFields(e);
    if (isTimelessReference(url, title)) return true;
    return isTemporallyRelevant(url, title, text, ctx);
  });
}

export function purgeStaleDocuments(documents, ctx = getTemporalContext()) {
  const kept = {};
  let removed = 0;
  for (const [url, doc] of Object.entries(documents || {})) {
    if (isTimelessReference(url, doc.title || "")) {
      kept[url] = doc;
      continue;
    }
    if (isTemporallyRelevant(url, doc.title || "", "", ctx)) {
      kept[url] = doc;
    } else {
      removed++;
    }
  }
  return { documents: kept, removed };
}

export function temporalHeaderLine(ctx = getTemporalContext()) {
  return `Учебный год **${ctx.academicLabel}** · актуально на **${ctx.humanDate}** · прошлые годы не учитываются`;
}
