// The site's only script. It remembers the theme you pick (Auto, Light or Dark) in this
// browser's local storage, so the next page opens the same way. No cookie, nothing sent anywhere.
// Loaded right after the theme radios, before the page paints, so there's no flash.
(function () {
  try {
    var r = document.getElementById("t-" + localStorage.getItem("theme"));
    if (r) r.checked = true;
  } catch (e) {}
  document.addEventListener("change", function (e) {
    if (e.target.name !== "theme") return;
    try { localStorage.setItem("theme", e.target.id.slice(2)); } catch (e) {}
  });
})();
