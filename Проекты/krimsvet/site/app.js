const state = {
  step: 1,
  objectType: null,
  tier: null,
  phase: null,
  data: null,
  baseBundle: null,
  selectedBatteryOptionId: null,
  computedBundle: null,
  overrideNote: null,
};

const ruFormatter = new Intl.NumberFormat("ru-RU");
const tierOrder = ["economy", "comfort", "premium"];

const stepTitle = document.getElementById("stepTitle");
const stepOptions = document.getElementById("stepOptions");
const resultCard = document.getElementById("resultCard");
const stepError = document.getElementById("stepError");

const leadForm = document.getElementById("leadForm");
const leadSku = document.getElementById("leadSku");
const leadName = document.getElementById("leadName");
const leadPrice = document.getElementById("leadPrice");
const leadBattery = document.getElementById("leadBattery");
const leadOutput = document.getElementById("leadOutput");
const leadPhone = document.getElementById("leadPhone");
const leadConsent = document.getElementById("leadConsent");
const leadSummary = document.getElementById("leadSummary");
const progressBar = document.getElementById("progressBar");

const objectIcons = {
  apartment: "🏠",
  house: "🏡",
  business: "🏢",
};

const tierIcons = {
  economy: "💡",
  comfort: "⚡",
  premium: "🔋",
};

function money(value) {
  return `${ruFormatter.format(value)} ₽`;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function round1(value) {
  return Math.round(value * 10) / 10;
}

function bundleBySku(sku) {
  return state.data.bundles.find((b) => b.sku === sku);
}

function getInverter(id) {
  return state.data.components.inverters.find((i) => i.id === id);
}

function getBattery(id) {
  return state.data.components.batteries.find((b) => b.id === id);
}

function formatBatteryLabel(battery, qty) {
  const base = `LiFePO4 ${battery.voltage} V / ${battery.capacity_ah} А·ч`;
  return qty > 1 ? `${qty}× ${base}` : base;
}

function formatHours(usableKwh, loadW) {
  const hours = Math.round((usableKwh * 1000) / loadW);
  return `${hours} ч при ${loadW} Вт`;
}

function calcLoadCurrent(loadW, voltage) {
  return Math.round((loadW / voltage) * 10) / 10;
}

function calcMaxDischargeCurrent(battery, qty, inverter) {
  const cRate = 0.5;
  return Math.round(battery.capacity_ah * qty * cRate);
}

function computeBundleConfig(baseBundle, batteryOption) {
  const inverter = getInverter(baseBundle.inverter_id);
  const battery = getBattery(batteryOption.battery_id);
  const invQty = baseBundle.inverter_qty || 1;
  const batQty = batteryOption.qty;

  const powerKw = inverter.power_kw * invQty;
  const powerPeakKw = inverter.power_peak_kw * invQty;
  const usableKwh = round1(battery.usable_kwh * batQty);
  const totalAh = battery.capacity_ah * batQty;
  const loadW = baseBundle.reference_load_w;
  const loadCurrentA = calcLoadCurrent(loadW, battery.voltage);
  const maxDischargeA = calcMaxDischargeCurrent(battery, batQty, inverter);

  return {
    sku: baseBundle.sku,
    name: baseBundle.name,
    group: baseBundle.group,
    tier: baseBundle.tier,
    phases: baseBundle.phases,
    works: baseBundle.works,
    not_for: baseBundle.not_for,
    power_kw: powerKw,
    power_peak_kw: powerPeakKw,
    usable_kwh: usableKwh,
    capacity_ah: totalAh,
    battery_voltage: battery.voltage,
    battery_label: formatBatteryLabel(battery, batQty),
    battery_option_id: batteryOption.id,
    hours_hint: formatHours(usableKwh, loadW),
    load_current_a: loadCurrentA,
    max_discharge_a: maxDischargeA,
    reference_load_w: loadW,
    price_rub: batteryOption.price_rub,
  };
}

function defaultBatteryOption(bundle) {
  return bundle.battery_options.find((o) => o.default) || bundle.battery_options[0];
}

function batteryOptionById(bundle, optionId) {
  return bundle.battery_options.find((o) => o.id === optionId);
}

function needsPhaseStep() {
  return state.objectType === "business" && state.tier === "premium";
}

function progressVisualStep() {
  if (state.step <= 1) return 1;
  if (state.step === 2) return 2;
  if (state.step === 3 && needsPhaseStep()) return 2;
  if (state.step === 3) return 3;
  if (state.step === 4 && needsPhaseStep()) return 3;
  if (state.step >= 4) return 4;
  return 1;
}

function updateProgress() {
  if (!progressBar) return;
  const steps = progressBar.querySelectorAll(".progress-step");
  const visualStep = progressVisualStep();
  steps.forEach((el, i) => {
    const n = i + 1;
    el.classList.toggle("active", n === visualStep);
    el.classList.toggle("done", n < visualStep);
  });
}

function renderStep1() {
  stepTitle.textContent = "Где нужен резерв?";
  const options = state.data.steps.object_types
    .map(
      (item) => `
      <button class="option-card" data-object-type="${item.id}">
        <span class="opt-icon">${objectIcons[item.id] || "⚡"}</span>
        <strong>${item.label}</strong>
      </button>
    `
    )
    .join("");
  stepOptions.innerHTML = options;
  updateProgress();
}

function renderStep2() {
  stepTitle.textContent = "Какой уровень подойдёт?";
  const tiers = state.data.steps.tiers[state.objectType];
  const options = tiers
    .map(
      (item) => `
      <button class="option-card" data-tier="${item.id}">
        <span class="opt-icon">${tierIcons[item.id] || "⚡"}</span>
        <strong>${item.label}</strong>
        <p>${item.hint}</p>
        <p class="price">от ${money(item.price_from)}</p>
      </button>
    `
    )
    .join("");
  stepOptions.innerHTML = options;
  updateProgress();
}

function renderStepPhase() {
  stepTitle.textContent = "Сколько фаз в объекте?";
  stepOptions.innerHTML = `
    <button class="option-card" data-phase="1ph">
      <span class="opt-icon">1️⃣</span>
      <strong>Одна фаза</strong>
      <p>Максимум для одной фазы</p>
    </button>
    <button class="option-card" data-phase="3ph">
      <span class="opt-icon">3️⃣</span>
      <strong>Три фазы</strong>
      <p>Трёхфазная система</p>
    </button>
  `;
  updateProgress();
}

function renderStepBattery() {
  const bundle = state.baseBundle;
  const options = bundle.battery_options
    .map((opt) => {
      const preview = computeBundleConfig(bundle, opt);
      return `
        <button class="option-card battery-card" data-battery-option="${opt.id}">
          <span class="opt-icon">🔋</span>
          <strong>${escapeHtml(preview.battery_label)}</strong>
          <p>${preview.usable_kwh} кВт·ч · ~${escapeHtml(preview.hours_hint)}</p>
          <p class="battery-specs">Ток нагрузки ~${preview.load_current_a} А · разряд до ${preview.max_discharge_a} А</p>
          <p class="price">${money(opt.price_rub)}</p>
        </button>
      `;
    })
    .join("");

  const inv = getInverter(bundle.inverter_id);
  const invQty = bundle.inverter_qty || 1;
  const invPower = inv.power_kw * invQty;

  stepTitle.textContent = "Выберите ёмкость АКБ";
  stepOptions.innerHTML = `
    <p class="step-hint">Инвертор: <strong>${invPower} кВт</strong> — мощность не меняется. Меняется ёмкость, ампер-часы и автономность.</p>
    ${options}
  `;
  updateProgress();
}

function neighborLinks(bundle) {
  const sameGroup = state.data.bundles
    .filter((b) => b.group === bundle.group)
    .sort((a, b) => tierOrder.indexOf(a.tier) - tierOrder.indexOf(b.tier));

  const idx = sameGroup.findIndex((b) => b.sku === bundle.sku);
  const cheaper = idx > 0 ? sameGroup[idx - 1] : null;
  const stronger = idx >= 0 && idx < sameGroup.length - 1 ? sameGroup[idx + 1] : null;

  return { cheaper, stronger };
}

function fillLead(bundle) {
  leadSku.value = bundle.sku;
  leadName.value = `${bundle.name} · ${bundle.battery_label}`;
  leadPrice.value = money(bundle.price_rub);
  if (leadBattery) {
    leadBattery.value = `${bundle.battery_label}; ${bundle.usable_kwh} кВт·ч; ${bundle.capacity_ah} А·ч`;
  }
  if (leadSummary) {
    leadSummary.textContent = `${bundle.name} · ${bundle.battery_label} — ${money(bundle.price_rub)}`;
    leadSummary.classList.add("filled");
  }
}

function resultPhoto(bundle) {
  if (bundle.group === "apartment") {
    return {
      src: "/pic/card-entry-must.jpg",
      alt: "Комплект квартира: инвертор MUST и АКБ LiFePO4",
    };
  }
  if (bundle.group === "house") {
    return {
      src: "/pic/card-hit-deye.jpg",
      alt: "Комплект дом: инвертор DEYE и АКБ LiFePO4",
    };
  }
  return {
    src: "/pic/card-hit-deye.jpg",
    alt: "Комплект резервного питания: инвертор и АКБ LiFePO4",
  };
}

function renderResult() {
  const bundle = state.computedBundle;
  const { cheaper, stronger } = neighborLinks(state.baseBundle);
  const photo = resultPhoto(bundle);
  const worksTags = bundle.works.map((w) => `<span class="tag tag-ok">${escapeHtml(w)}</span>`).join("");
  const notTags = bundle.not_for.length
    ? bundle.not_for.map((w) => `<span class="tag tag-no">${escapeHtml(w)}</span>`).join("")
    : '<span class="tag tag-ok">без ограничений</span>';
  const note = state.overrideNote
    ? `<p class="result-note">${escapeHtml(state.overrideNote)}</p>`
    : "";

  resultCard.innerHTML = `
    <article class="result">
      <img class="result-photo" src="${photo.src}" width="1024" height="768" alt="${escapeHtml(photo.alt)}" decoding="async">
      <div class="result-header">
        <h3>${escapeHtml(bundle.name)}</h3>
        <div class="result-price">${money(bundle.price_rub)}</div>
      </div>
      <div class="result-body">
        ${note}
        <div class="result-grid">
          <div class="result-item">
            <span class="label">Мощность инвертора</span>
            ${bundle.power_kw} кВт / ${bundle.power_peak_kw} кВт пик
          </div>
          <div class="result-item">
            <span class="label">Ёмкость</span>
            ${bundle.usable_kwh} кВт·ч
          </div>
          <div class="result-item">
            <span class="label">АКБ</span>
            ${escapeHtml(bundle.battery_label)}
          </div>
          <div class="result-item">
            <span class="label">Ампер-часы</span>
            ${bundle.capacity_ah} А·ч при ${bundle.battery_voltage} V
          </div>
          <div class="result-item">
            <span class="label">Ток нагрузки</span>
            ~${bundle.load_current_a} А при ${bundle.reference_load_w} Вт
          </div>
          <div class="result-item">
            <span class="label">Автономность</span>
            ~${escapeHtml(bundle.hours_hint)}
          </div>
        </div>
        <div class="result-item">
          <span class="label">Работает</span>
          <div class="result-tags">${worksTags}</div>
        </div>
        <div class="result-item" style="margin-top:10px">
          <span class="label">Не тянет постоянно</span>
          <div class="result-tags">${notTags}</div>
        </div>
        <div class="result-links">
          ${cheaper ? `<a href="#" data-switch-sku="${cheaper.sku}">← Дешевле: ${escapeHtml(cheaper.name)}</a>` : ""}
          ${stronger ? `<a href="#" data-switch-sku="${stronger.sku}">Мощнее: ${escapeHtml(stronger.name)} →</a>` : ""}
          <a href="#" data-change-battery>↺ Изменить АКБ</a>
        </div>
      </div>
      <div class="result-actions">
        <a class="btn btn-accent" href="#leadForm" onclick="document.querySelector('.section-lead').scrollIntoView({behavior:'smooth'});return false;">Оставить заявку</a>
        <a class="btn btn-ghost" href="tel:+78003331404" style="color:var(--text);border-color:var(--line)">Позвонить</a>
      </div>
    </article>
  `;

  fillLead(bundle);
  updateProgress();

  resultCard.querySelectorAll("[data-switch-sku]").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const sku = link.dataset.switchSku;
      state.baseBundle = bundleBySku(sku);
      state.overrideNote = null;
      const defOpt = defaultBatteryOption(state.baseBundle);
      state.selectedBatteryOptionId = defOpt.id;
      state.computedBundle = computeBundleConfig(state.baseBundle, defOpt);
      if (state.baseBundle.battery_options.length > 1) {
        state.step = needsPhaseStep() ? 4 : 3;
        render();
      } else {
        state.step = needsPhaseStep() ? 5 : 4;
        render();
      }
      document.getElementById("calculator").scrollIntoView({ behavior: "smooth" });
    });
  });

  const changeBattery = resultCard.querySelector("[data-change-battery]");
  if (changeBattery) {
    changeBattery.addEventListener("click", (e) => {
      e.preventDefault();
      state.step = needsPhaseStep() ? 4 : 3;
      render();
    });
  }
}

function resolveBaseBundle() {
  state.overrideNote = null;
  let sku = state.data.lookup[state.objectType][state.tier];
  if (state.objectType === "business" && state.tier === "premium") {
    const override = state.data.business_premium_override[state.phase];
    sku = override.sku;
    state.overrideNote = override.note;
  }
  state.baseBundle = bundleBySku(sku);
}

function applyBatteryAndGoResult(optionId) {
  const option = batteryOptionById(state.baseBundle, optionId);
  state.selectedBatteryOptionId = optionId;
  state.computedBundle = computeBundleConfig(state.baseBundle, option);
  state.step = needsPhaseStep() ? 5 : 4;
  render();
}

function goToBatteryStep() {
  resolveBaseBundle();
  const defOpt = defaultBatteryOption(state.baseBundle);
  if (state.baseBundle.battery_options.length === 1) {
    applyBatteryAndGoResult(defOpt.id);
    return;
  }
  state.selectedBatteryOptionId = defOpt.id;
  state.step = needsPhaseStep() ? 4 : 3;
  render();
}

function render() {
  stepError.textContent = "";
  resultCard.innerHTML = "";

  if (state.step === 1) {
    renderStep1();
    return;
  }
  if (state.step === 2) {
    renderStep2();
    return;
  }
  if (state.step === 3 && needsPhaseStep()) {
    renderStepPhase();
    return;
  }
  if ((state.step === 3 && !needsPhaseStep()) || (state.step === 4 && needsPhaseStep())) {
    renderStepBattery();
    return;
  }
  if ((state.step === 4 && !needsPhaseStep()) || (state.step === 5 && needsPhaseStep())) {
    stepTitle.textContent = "Ваш комплект";
    stepOptions.innerHTML = `
      <button class="option-card restart" id="restartBtn">
        <strong>↺ Подобрать заново</strong>
      </button>
    `;
    renderResult();
  }
}

stepOptions.addEventListener("click", (event) => {
  const target = event.target.closest("button");
  if (!target) return;

  if (target.dataset.objectType) {
    state.objectType = target.dataset.objectType;
    state.step = 2;
    render();
    return;
  }

  if (target.dataset.tier) {
    state.tier = target.dataset.tier;
    if (needsPhaseStep()) {
      state.step = 3;
      render();
      return;
    }
    goToBatteryStep();
    return;
  }

  if (target.dataset.phase) {
    state.phase = target.dataset.phase;
    goToBatteryStep();
    return;
  }

  if (target.dataset.batteryOption) {
    applyBatteryAndGoResult(target.dataset.batteryOption);
    return;
  }

  if (target.id === "restartBtn") {
    state.step = 1;
    state.objectType = null;
    state.tier = null;
    state.phase = null;
    state.baseBundle = null;
    state.selectedBatteryOptionId = null;
    state.computedBundle = null;
    state.overrideNote = null;
    leadOutput.textContent = "";
    if (leadSummary) {
      leadSummary.textContent = "Сначала подберите комплект в калькуляторе";
      leadSummary.classList.remove("filled");
    }
    render();
  }
});

if (leadPhone) leadPhone.addEventListener("input", () => {
  let digits = leadPhone.value.replace(/\D/g, "");
  if (digits.startsWith("8")) digits = `7${digits.slice(1)}`;
  if (!digits.startsWith("7")) digits = `7${digits}`;
  digits = digits.slice(0, 11);

  const p = digits.padEnd(11, "_").split("");
  leadPhone.value = `+${p[0]} (${p[1]}${p[2]}${p[3]}) ${p[4]}${p[5]}${p[6]}-${p[7]}${p[8]}-${p[9]}${p[10]}`.replace(/_/g, "");
});

if (leadForm) leadForm.addEventListener("submit", (event) => {
  event.preventDefault();
  leadOutput.className = "output";

  if (!state.computedBundle) {
    stepError.textContent = "Сначала выберите комплект через калькулятор.";
    return;
  }

  if (!leadConsent.checked) {
    leadOutput.classList.add("fail");
    leadOutput.textContent = "Подтвердите согласие на обработку персональных данных.";
    return;
  }

  const digits = leadPhone.value.replace(/\D/g, "");
  if (digits.length < 11) {
    leadOutput.classList.add("fail");
    leadOutput.textContent = "Введите корректный телефон в формате +7.";
    return;
  }

  const formData = new FormData(leadForm);
  const payload = Object.fromEntries(formData.entries());
  payload.phone = `+${digits}`;
  payload.landing = "krimsvet.ru";
  payload.created_at = new Date().toISOString();

  leadOutput.textContent = "Отправляем заявку...";

  fetch("/lead.php", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then(async (response) => {
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        throw new Error(data.error || "Не удалось отправить заявку");
      }
      leadOutput.classList.add("success");
      leadOutput.textContent = "Заявка отправлена. Мы свяжемся с вами в ближайшее время.";
      leadForm.reset();
      document.getElementById("leadCity").value = "Симферополь";
      fillLead(state.computedBundle);
    })
    .catch((error) => {
      leadOutput.classList.add("fail");
      leadOutput.textContent = `Ошибка отправки: ${error.message}`;
    });
});


const OBJECT_ALIASES = {
  apartment: "apartment",
  kvartira: "apartment",
  flat: "apartment",
  house: "house",
  dom: "house",
  business: "business",
  biznes: "business",
};

function applyObjectFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const raw = (params.get("object") || params.get("type") || document.body.dataset.object || "").toLowerCase().trim();
  if (!raw) return false;
  const objectType = OBJECT_ALIASES[raw] || OBJECT_ALIASES[raw.replace(/[^a-z]/g, "")] || raw;
  if (!objectType || !["apartment", "house", "business"].includes(objectType)) return false;
  const exists = (state.data.steps.object_types || []).some((x) => x.id === objectType);
  if (!exists) return false;
  state.objectType = objectType;
  state.tier = null;
  state.phase = null;
  state.baseBundle = null;
  state.selectedBatteryOptionId = null;
  state.computedBundle = null;
  state.overrideNote = null;
  state.step = 2;
  return true;
}

async function loadBundles() {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("/bundles.json?v=20261111a", { signal: controller.signal });
    if (!response.ok) throw new Error(`bundles.json HTTP ${response.status}`);
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

async function init() {
  try {
    if (stepError) stepError.textContent = "Загрузка комплектов…";
    state.data = await loadBundles();
    if (stepError) stepError.textContent = "";
    applyObjectFromQuery();
    render();
  } catch (error) {
    const msg = error && error.message ? error.message : String(error);
    if (stepTitle) stepTitle.textContent = "Не удалось загрузить калькулятор";
    if (stepOptions) {
      stepOptions.innerHTML = `
        <button class="option-card restart" id="retryBundlesBtn" type="button">
          <strong>↻ Обновить и попробовать снова</strong>
          <p>${msg}</p>
        </button>`;
      const btn = document.getElementById("retryBundlesBtn");
      if (btn) btn.addEventListener("click", () => init());
    }
    if (stepError) stepError.textContent = `Ошибка загрузки: ${msg}`;
  }
}

init();
