(function () {
  var q = document.getElementById("q"), grid = document.getElementById("grid"), empty = document.getElementById("empty"), cat = "";
  function filter() {
    if (!grid) return;
    var t = (q.value || "").trim().toLowerCase(), n = 0;
    grid.querySelectorAll(".card").forEach(function (c) {
      var ok = (!cat || c.dataset.cat === cat) && (!t || c.dataset.t.indexOf(t) > -1);
      c.hidden = !ok; if (ok) n++;
    });
    if (empty) empty.hidden = n > 0;
  }
  document.querySelectorAll(".chip").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".chip").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      cat = b.dataset.c; filter();
    });
  });
  if (q) {
    q.addEventListener("input", function () {
      if (!grid) { if (q.value.length > 1) location.href = "/?q=" + encodeURIComponent(q.value); return; }
      filter();
    });
    var m = location.search.match(/[?&]q=([^&]+)/);
    if (m && grid) { q.value = decodeURIComponent(m[1]); filter(); }
  }
  var stage = document.getElementById("stage"), play = document.getElementById("playBtn"), fs = document.getElementById("fsBtn");
  if (stage && play) {
    play.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = stage.dataset.src; f.title = document.title; f.allow = "autoplay; fullscreen; gamepad"; f.allowFullscreen = true;
      f.setAttribute("scrolling", "no");
      stage.innerHTML = ""; stage.appendChild(f); stage.classList.add("is-on");
    });
    fs.addEventListener("click", function () {
      var el = stage.closest(".play");
      if (document.fullscreenElement) document.exitFullscreen();
      else if (el.requestFullscreen) el.requestFullscreen().catch(function () {});
      else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    });
  }
})();
