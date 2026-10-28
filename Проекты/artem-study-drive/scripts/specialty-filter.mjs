/** Фильтр по специальности студента — только 09.02.07, не все программы подряд. */
export const SPECIALTY = {
  code: "09.02.07",
  shortCode: "09.02.07",
  name: "Информационные системы и программирование",
  namePatterns: [
    "09.02.07",
    "09.02. 07",
    "информационн систем и программ",
    "информационные системы и программирование",
    "информ систем и програм",
  ],
  /** Другие коды СПО 09.02.XX — не наша специальность */
  otherCodeRe: /09\.02\.(?!07)\d{2}/gi,
  /** ИПК, БТСТ, вуз — не ЦСПО Артёма */
  excludeUnitPatterns: [
    "ipk.kipu",
    "/ipk/",
    "бтст",
    "btst",
    "bakalavriat",
    "magistratur",
    "aspirantur",
    "бакалавр",
    "магистр",
    "специалитет",
    "инженерно-педагогический колледж",
  ],
  /** Общие для всех (оплата, лицензия, реквизиты) — без привязки к спец. */
  institutionWidePatterns: [
    "paid_edu",
    "sveden/paid",
    "sveden/common",
    "sveden/document",
    "sveden/grants",
    "studentu-tsspo",
    "/cspo/",
    "стоимост",
    "реквизит",
    "лиценз",
    "аккредит",
    "компенсац",
    "налогов",
    "вычет",
  ],
  /** Расписание аттестации ЦСПО — общий файл, но только раздел ЦСПО */
  cspoSharedPatterns: ["rasp_zima", "raspisanie-promezhutochn", "аттестац"],
};

export function mentionsOurSpecialty(blob) {
  const low = String(blob).toLowerCase();
  return SPECIALTY.namePatterns.some((p) => low.includes(p.toLowerCase()));
}

export function mentionsOtherSpecialty(blob) {
  SPECIALTY.otherCodeRe.lastIndex = 0;
  return SPECIALTY.otherCodeRe.test(String(blob));
}

export function isExcludedUnit(url, title, text = "") {
  const low = `${url} ${title} ${text}`.toLowerCase();
  return SPECIALTY.excludeUnitPatterns.some((p) => low.includes(p.toLowerCase()));
}

export function isInstitutionWide(url, title, text = "") {
  if (isExcludedUnit(url, title, text)) return false;
  const low = `${url} ${title} ${text}`.toLowerCase();
  return SPECIALTY.institutionWidePatterns.some((p) => low.includes(p.toLowerCase()));
}

export function isCspoSharedSchedule(url, title, text = "") {
  const low = `${url} ${title} ${text}`.toLowerCase();
  return SPECIALTY.cspoSharedPatterns.some((p) => low.includes(p.toLowerCase()));
}

/**
 * @param {{ studentFound?: boolean, group?: string|null }} opts
 */
export function isSpecialtyRelevant(url, title, text = "", opts = {}) {
  const { studentFound = false, group = null } = opts;
  const blob = `${url} ${title} ${text.slice(0, 12000)}`;
  const low = blob.toLowerCase();

  if (studentFound) return true;
  if (isExcludedUnit(url, title, text)) return false;
  if (isInstitutionWide(url, title, text)) return true;
  if (isCspoSharedSchedule(url, title, text)) return true;
  if (mentionsOurSpecialty(blob)) return true;
  if (mentionsOtherSpecialty(blob)) return false;
  if (group && low.includes(String(group).toLowerCase())) return true;
  return false;
}

export function specialtyHeaderLine() {
  return `Только специальность **${SPECIALTY.code}** «${SPECIALTY.name}» — другие программы не учитываются`;
}

export function purgeOtherSpecialtyDocuments(documents, opts = {}) {
  const kept = {};
  let removed = 0;
  for (const [url, doc] of Object.entries(documents || {})) {
    if (
      isSpecialtyRelevant(url, doc.title || "", "", {
        studentFound: doc.studentFound,
        group: opts.group ?? null,
      })
    ) {
      kept[url] = doc;
    } else {
      removed++;
    }
  }
  return { documents: kept, removed };
}
