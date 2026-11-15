/* Цели Яндекс.Метрики krimsvet.ru. Обновлено: 2026-11-15 */
(function () {
  var COUNTER_ID = 114159186;

  function reachGoal(name, params) {
    try {
      if (typeof window.ym === "function") {
        if (params) window.ym(COUNTER_ID, "reachGoal", name, params);
        else window.ym(COUNTER_ID, "reachGoal", name);
      }
    } catch (err) {
      /* ignore */
    }
  }

  window.krimsvetReachGoal = reachGoal;

  document.addEventListener(
    "click",
    function (event) {
      var link = event.target && event.target.closest ? event.target.closest("a[href^='tel:']") : null;
      if (!link) return;
      reachGoal("phone_click", { phone: (link.getAttribute("href") || "").replace(/^tel:/i, "") });
    },
    true
  );
})();
