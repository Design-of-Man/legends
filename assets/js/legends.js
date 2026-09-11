/* ============================================================================
   LEGENDS RADIO 100.3 — front-end behaviour
   Persistent live player (real WLML stream) · client-side "On Air Now" engine
   computed in the station's Eastern time · scroll reveals · counters · nav ·
   marquees · forms. Zero dependencies. Reduced-motion aware.
   Data (schedule/stream) is injected by build.py as window.LEGENDS_*.
   ========================================================================== */
(function () {
  "use strict";
  var RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var SCHEDULE = window.LEGENDS_SCHEDULE || {};
  var STREAM = window.LEGENDS_STREAM || "";
  var POPOUT = window.LEGENDS_POPOUT || "https://legendsradio.com/listen-live/";

  /* ---------------------------------------------------------------- header */
  var header = $(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 24); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ------------------------------------------------------------- mobile nav */
  var toggle = $(".nav-toggle"), links = $(".nav-links");
  function closeNav() {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", "false");
    links.classList.remove("open");
    document.body.classList.remove("nav-open");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      links.classList.toggle("open", !open);
      document.body.classList.toggle("nav-open", !open);
    });
    $$(".nav-links a").forEach(function (a) { a.addEventListener("click", closeNav); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeNav(); });
  }

  /* ================================================================ PLAYER */
  var audio = $("#legends-audio");
  var player = $(".player");
  var playBtns = $$("[data-play]");           // hero button + player button share control
  var volInput = $(".player-vol input");
  var vinyls = $$(".vinyl");
  var eqs = $$(".eq");
  var state = { playing: false, loading: false };

  function setEq(on) { eqs.forEach(function (e) { e.classList.toggle("playing", on); }); }
  function setVinyl(on) { vinyls.forEach(function (v) { v.classList.toggle("spinning", on); }); }
  function reflectUI() {
    if (player) player.classList.toggle("playing", state.playing);
    if (player) player.classList.toggle("loading", state.loading);
    playBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String(state.playing));
      b.classList.toggle("playing", state.playing);
      var lbl = b.querySelector("[data-play-label]");
      if (lbl) lbl.textContent = state.playing ? "Pause" : (b.dataset.playLabelText || "Listen Live");
    });
    setEq(state.playing); setVinyl(state.playing);
  }

  function play() {
    if (!audio) return;
    state.loading = true; reflectUI();
    // (re)attach the live source each play so we always reconnect to the live edge
    if (!audio.src) audio.src = STREAM;
    var p = audio.play();
    if (p && p.catch) p.catch(function () { onError(); });
  }
  function pause() { if (audio) { audio.pause(); try { audio.removeAttribute("src"); audio.load(); } catch (e) {} } }
  function toggle_() { state.playing ? pause() : play(); }

  function onError() {
    state.playing = false; state.loading = false; reflectUI();
    if (player) {
      var meta = $(".player-meta .p-host", player);
      if (meta) meta.innerHTML = 'Stream unavailable — <a href="' + POPOUT + '" target="_blank" rel="noopener" style="color:var(--gold);text-decoration:underline">open the pop-out player</a>';
    }
  }

  if (audio) {
    audio.addEventListener("playing", function () { state.playing = true; state.loading = false; reflectUI(); });
    audio.addEventListener("pause", function () { state.playing = false; state.loading = false; reflectUI(); });
    audio.addEventListener("waiting", function () { state.loading = true; reflectUI(); });
    audio.addEventListener("error", onError);
    audio.addEventListener("stalled", function () { /* keep trying */ });
    // volume
    var savedVol = parseFloat(localStorage.getItem("legends_vol"));
    audio.volume = isNaN(savedVol) ? 0.85 : savedVol;
    if (volInput) {
      volInput.value = String(Math.round(audio.volume * 100));
      volInput.addEventListener("input", function () {
        audio.volume = Math.min(1, Math.max(0, volInput.value / 100));
        localStorage.setItem("legends_vol", String(audio.volume));
      });
    }
  }
  playBtns.forEach(function (b) { b.addEventListener("click", toggle_); });

  // keyboard: space toggles when not typing in a field
  document.addEventListener("keydown", function (e) {
    if (e.code === "Space" && !/^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); toggle_();
    }
  });

  /* ===================================================== ON AIR NOW engine */
  // Current time in the station's timezone (America/New_York), tz-safe anywhere.
  function nowET() {
    var parts;
    try {
      parts = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/New_York", weekday: "short", hour: "2-digit",
        minute: "2-digit", hour12: false
      }).formatToParts(new Date());
    } catch (e) { var d = new Date(); return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }; }
    var map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, o = {};
    parts.forEach(function (p) { o[p.type] = p.value; });
    var h = parseInt(o.hour, 10); if (h === 24) h = 0;
    return { day: map[o.weekday], min: h * 60 + parseInt(o.minute, 10) };
  }
  function toMin(hhmm) { var a = hhmm.split(":"); return parseInt(a[0], 10) * 60 + parseInt(a[1], 10); }
  function fmt(hhmm) {
    var m = toMin(hhmm), h = Math.floor(m / 60), mm = m % 60;
    var ap = h >= 12 ? "PM" : "AM", h12 = h % 12; if (h12 === 0) h12 = 12;
    return h12 + (mm ? ":" + (mm < 10 ? "0" + mm : mm) : "") + " " + ap;
  }

  function currentSlot() {
    var t = nowET(), day = SCHEDULE[t.day] || [], i;
    for (i = 0; i < day.length; i++) {
      var s = toMin(day[i].start), e = toMin(day[i].end);
      if (e <= s) e = 1440; // safety
      if (t.min >= s && t.min < e) {
        return { slot: day[i], day: t.day, idx: i, now: t.min, start: s, end: e };
      }
    }
    return null;
  }
  function nextSlot(cur) {
    if (!cur) return null;
    var day = SCHEDULE[cur.day] || [];
    if (cur.idx + 1 < day.length) return day[cur.idx + 1];
    var nd = (cur.day + 1) % 7, nday = SCHEDULE[nd] || [];
    return nday[0] || null;
  }

  function paintNowPlaying() {
    var cur = currentSlot();
    var nxt = nextSlot(cur);
    var showName = cur ? cur.slot.show : "Nonstop Legends";
    var hostName = cur ? (cur.slot.host || "The Great American Songbook") : "The Great American Songbook";
    var timeStr = cur ? (fmt(cur.slot.start) + " – " + fmt(cur.slot.end) + " ET") : "";

    // hero now-playing card
    var hc = $("#np-show"); if (hc) hc.textContent = showName;
    var hh = $("#np-host"); if (hh) hh.textContent = hostName;
    var ht = $("#np-time"); if (ht) ht.textContent = timeStr;
    var hn = $("#np-next"); if (hn && nxt) hn.innerHTML = "Up next · <b>" + nxt.show + "</b> at " + fmt(nxt.start);

    // sticky player meta
    var ps = $(".player .p-show"); if (ps) ps.textContent = showName;
    var ph = $(".player .p-host");
    if (ph && ph.querySelector("a") === null) ph.textContent = hostName + (cur && !state.playing ? " · " + timeStr : "");

    // Media Session (lock-screen / OS media controls)
    if ("mediaSession" in navigator) {
      try {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: showName, artist: hostName,
          album: "Legends Radio 100.3 FM",
          artwork: [{ src: (window.LEGENDS_ARTWORK || ""), sizes: "512x512", type: "image/png" }]
        });
      } catch (e) {}
    }

    // schedule grid live highlight + progress
    $$(".sched-row").forEach(function (row) { row.classList.remove("live"); var b = $(".s-progress", row); if (b) b.style.width = "0"; });
    if (cur) {
      var sel = '.sched-row[data-day="' + cur.day + '"][data-idx="' + cur.idx + '"]';
      var row = $(sel);
      if (row) {
        row.classList.add("live");
        var pct = ((cur.now - cur.start) / (cur.end - cur.start)) * 100;
        var bar = $(".s-progress", row); if (bar) bar.style.width = Math.max(2, Math.min(100, pct)) + "%";
      }
    }
  }
  if (Object.keys(SCHEDULE).length) { paintNowPlaying(); setInterval(paintNowPlaying, 30000); }

  /* --------------------------------------------------------- schedule tabs */
  var tabs = $$(".sched-tabs button");
  if (tabs.length) {
    function showDay(day) {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", String(t.dataset.day === day)); });
      $$("[data-sched-day]").forEach(function (panel) {
        panel.hidden = panel.dataset.schedDay !== day;
      });
    }
    tabs.forEach(function (t) { t.addEventListener("click", function () { showDay(t.dataset.day); }); });
    // default to today (ET)
    showDay(String(nowET().day));
  }

  /* ------------------------------------------------------------- marquees */
  $$(".marquee-track").forEach(function (track) {
    var html = track.innerHTML; track.innerHTML = html + html; // duplicate for seamless -50% loop
  });

  /* ----------------------------------------------------- reveal on scroll */
  var reveals = $$(".reveal");
  if (RM || !("IntersectionObserver" in window)) {
    reveals.forEach(function (r) { r.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (r) { io.observe(r); });
  }

  /* ------------------------------------------------------------- counters */
  function runCounter(el) {
    var target = parseFloat(el.dataset.count) || 0;
    var suffix = el.dataset.suffix || "";
    var dur = 1400, t0 = null;
    if (RM) { el.textContent = format(target) + ""; wrapSuffix(el, suffix); return; }
    function format(n) { return Math.round(n).toLocaleString("en-US"); }
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(target * eased);
      if (p < 1) requestAnimationFrame(step); else { el.textContent = format(target); wrapSuffix(el, suffix); }
    }
    requestAnimationFrame(step);
  }
  function wrapSuffix(el, suffix) { if (suffix) { var s = document.createElement("span"); s.className = "suffix"; s.textContent = suffix; el.appendChild(s); } }
  var counters = $$("[data-count]");
  if (counters.length) {
    if (RM || !("IntersectionObserver" in window)) { counters.forEach(runCounter); }
    else {
      var co = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { runCounter(e.target); co.unobserve(e.target); } });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { co.observe(c); });
    }
  }

  /* ---------------------------------------------------------------- forms */
  $$("form[data-endpoint]").forEach(function (form) {
    var status = $(".form-status", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = $("[type=submit]", form); var orig = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      var data = new FormData(form);
      fetch(form.dataset.endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error("bad"); return r.json().catch(function () { return {}; }); })
        .then(function () {
          if (status) { status.className = "form-status ok"; status.textContent = form.dataset.success || "Thank you — we’ll be in touch shortly."; }
          form.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.innerHTML = 'Something went wrong. Please call us at <a href="tel:+15614696700" style="color:inherit;text-decoration:underline">(561) 469-6700</a>.'; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = orig; } });
    });
  });

  /* ------------------------------------------- brass scroll-progress rail */
  var rail = $("#scroll-rail");
  if (rail && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var railTick = false;
    var drawRail = function () {
      var d = document.documentElement;
      var max = d.scrollHeight - d.clientHeight;
      rail.style.width = (max > 0 ? (d.scrollTop / max) * 100 : 0) + "%";
      railTick = false;
    };
    addEventListener("scroll", function () {
      if (!railTick) { railTick = true; requestAnimationFrame(drawRail); }
    }, { passive: true });
    addEventListener("resize", drawRail, { passive: true });
    drawRail();
  }


  /* ==================================================================== */
  /*  LIVE NOW PLAYING — track + album art                                */
  /*                                                                      */
  /*  Both feeds come from SecureNetSystems, the station's own streaming   */
  /*  vendor, and both send Access-Control-Allow-Origin, so the browser    */
  /*  reads them directly. WLML.xml is the current item and goes blank     */
  /*  during ad breaks and talk, so we fall back to the head of the        */
  /*  history feed. Cover art is absent on roughly 40% of tracks — the     */
  /*  spinning vinyl is the designed fallback, never a broken image.       */
  /* ==================================================================== */
  var NP_URL = window.LEGENDS_NOWPLAYING || "";
  var HIST_URL = window.LEGENDS_HISTORY || "";

  function xmlText(node, tag) {
    var el = node.getElementsByTagName(tag)[0];
    return el && el.textContent ? el.textContent.trim() : "";
  }
  function parseSongs(text) {
    var doc;
    try { doc = new DOMParser().parseFromString(text, "text/xml"); } catch (e) { return []; }
    if (!doc || doc.getElementsByTagName("parsererror").length) return [];
    var nodes = doc.getElementsByTagName("song");
    if (!nodes.length) nodes = doc.getElementsByTagName("playlist");
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      var t = xmlText(nodes[i], "title"), a = xmlText(nodes[i], "artist");
      if (!t && !a) continue;                       // blank = ad break or talk
      out.push({
        title: t, artist: a,
        album: xmlText(nodes[i], "album"),
        cover: xmlText(nodes[i], "cover"),
        at: xmlText(nodes[i], "programStartTS")
      });
    }
    return out;
  }
  function getXML(url) {
    if (!url || !window.fetch) return Promise.reject();
    return fetch(url, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    });
  }

  /* Paint one art slot: real cover when we have it, vinyl when we don't. */
  function paintArt(scope, song) {
    $$("[data-art]", scope || document).forEach(function (slot) {
      var img = $("[data-art-img]", slot), fb = $("[data-art-fallback]", slot);
      if (!img || !fb) return;
      if (song && song.cover) {
        if (img.getAttribute("src") !== song.cover) {
          img.onerror = function () { img.hidden = true; fb.hidden = false; slot.classList.remove("has-art"); };
          img.setAttribute("src", song.cover);
        }
        img.alt = song.album ? (song.album + " — " + song.artist) : song.artist;
        img.hidden = false; fb.hidden = true; slot.classList.add("has-art");
      } else {
        img.hidden = true; img.removeAttribute("src"); fb.hidden = false;
        slot.classList.remove("has-art");
      }
    });
  }

  var curSong = null;
  function paintTrack(song) {
    curSong = song;
    paintArt(document, song);
    $$("[data-track]").forEach(function (row) {
      var t = $("[data-track-title]", row), a = $("[data-track-artist]", row);
      if (song) {
        if (t) t.textContent = song.title;
        if (a) a.textContent = song.artist ? " · " + song.artist : "";
        row.hidden = false;
      } else { row.hidden = true; }
    });
    if (song && "mediaSession" in navigator) {
      try {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: song.title, artist: song.artist,
          album: song.album || "Legends Radio 100.3 FM",
          artwork: [{ src: song.cover || (window.LEGENDS_ARTWORK || ""), sizes: "512x512" }]
        });
      } catch (e) {}
    }
  }

  var playedList = $("[data-played]");
  function renderPlayed(songs) {
    if (!playedList) return;
    var limit = parseInt(playedList.dataset.playedLimit || "12", 10);
    var rows = songs.slice(0, limit);
    if (!rows.length) return;
    playedList.innerHTML = rows.map(function (s, i) {
      var art = s.cover
        ? '<img class="pl-art" src="' + s.cover + '" alt="" width="56" height="56" loading="lazy">'
        : '<span class="pl-art pl-art-none" aria-hidden="true"></span>';
      var when = (s.at || "").split(" ").slice(3).join(" ").slice(0, 5);
      return '<li class="played-row' + (i === 0 ? " is-current" : "") + '">' + art +
        '<span class="pl-meta"><b>' + esc(s.title) + '</b><span>' + esc(s.artist) + '</span></span>' +
        (when ? '<time class="pl-when">' + esc(when) + '</time>' : "") + '</li>';
    }).join("");
  }
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }

  function refreshNowPlaying() {
    if (document.hidden) return;
    getXML(NP_URL).then(function (txt) {
      var cur = parseSongs(txt)[0];
      if (cur) { paintTrack(cur); return null; }
      return getXML(HIST_URL).then(function (h) { paintTrack(parseSongs(h)[0] || null); return null; });
    }).catch(function () { /* leave the show card as-is; never surface a stack trace */ });

    if (playedList) {
      getXML(HIST_URL).then(function (h) {
        var songs = parseSongs(h);
        renderPlayed(songs);
        if (!curSong && songs[0]) paintTrack(songs[0]);
      }).catch(function () {
        var e = $("[data-played-empty]");
        if (e) e.textContent = "The playlist is taking a breath — tune to 100.3 FM to hear what's on.";
      });
    }
  }
  if (NP_URL) {
    refreshNowPlaying();
    setInterval(refreshNowPlaying, 30000);
    document.addEventListener("visibilitychange", function () { if (!document.hidden) refreshNowPlaying(); });
  }

  /* ==================================================================== */
  /*  EPISODE PLAYER                                                      */
  /*  Only one thing plays at a time: starting an episode stops the live   */
  /*  stream, and starting the live stream stops the episode.             */
  /* ==================================================================== */
  var epAudio = null, epCurrent = null;
  function epStopAll() {
    if (epAudio) { epAudio.pause(); }
    $$("[data-episode]").forEach(function (li) {
      li.classList.remove("playing"); li.classList.remove("loading");
    });
  }
  function mmss(s) {
    if (!isFinite(s) || s < 0) return "0:00";
    var m = Math.floor(s / 60), r = Math.floor(s % 60);
    return m + ":" + (r < 10 ? "0" : "") + r;
  }
  $$("[data-episode]").forEach(function (li) {
    var btn = $("[data-ep-play]", li), rail = $("[data-ep-rail]", li),
        fill = $("[data-ep-fill]", li), now = $("[data-ep-now]", li), dur = $("[data-ep-dur]", li);
    function ensure() {
      if (!epAudio) {
        epAudio = new Audio();
        epAudio.preload = "metadata";
        epAudio.addEventListener("timeupdate", function () {
          if (!epCurrent) return;
          var f = $("[data-ep-fill]", epCurrent), n = $("[data-ep-now]", epCurrent);
          var pct = epAudio.duration ? (epAudio.currentTime / epAudio.duration) * 100 : 0;
          if (f) f.style.width = pct + "%";
          if (n) n.textContent = mmss(epAudio.currentTime);
        });
        epAudio.addEventListener("loadedmetadata", function () {
          if (!epCurrent) return;
          var d = $("[data-ep-dur]", epCurrent);
          if (d) d.textContent = mmss(epAudio.duration);
        });
        epAudio.addEventListener("playing", function () {
          if (!epCurrent) return;
          epCurrent.classList.remove("loading");
          epCurrent.classList.add("playing");
        });
        epAudio.addEventListener("waiting", function () {
          if (epCurrent) epCurrent.classList.add("loading");
        });
        epAudio.addEventListener("ended", function () { epStopAll(); epCurrent = null; });
        epAudio.addEventListener("error", function () {
          var failed = epCurrent;
          epStopAll();
          if (failed) failed.classList.add("ep-error");
        });
      }
    }
    if (btn) btn.addEventListener("click", function () {
      ensure();
      var isMe = epCurrent === li && !epAudio.paused;
      epStopAll();
      if (isMe) { epCurrent = null; return; }
      pause();                                   // hand the floor over from the live stream
      if (epCurrent !== li) { epAudio.src = li.dataset.src; epCurrent = li; }
      li.classList.remove("ep-error");
      li.classList.add("loading");          // 'playing' is set by the audio element itself
      var pr = epAudio.play();
      if (pr && pr.catch) pr.catch(function () { epStopAll(); li.classList.add("ep-error"); });
    });
    if (rail) rail.addEventListener("click", function (e) {
      if (epCurrent !== li || !epAudio || !epAudio.duration) return;
      var r = rail.getBoundingClientRect();
      epAudio.currentTime = ((e.clientX - r.left) / r.width) * epAudio.duration;
    });
    if (dur) dur.textContent = "––";
  });
  // The live stream reclaims the floor whenever it starts.
  if (audio) audio.addEventListener("playing", function () { if (epAudio) { epAudio.pause(); epStopAll(); } });

  /* -------- SoundCloud: widget only once the visitor asks for it -------- */
  $$("[data-sc-load]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.closest(".episode"); if (!li || li.dataset.loaded) return;
      pause();
      var f = document.createElement("iframe");
      f.src = btn.dataset.scUrl + "&auto_play=true";
      f.title = btn.getAttribute("aria-label") || "SoundCloud player";
      f.width = "100%"; f.height = "120"; f.frameBorder = "0";
      f.allow = "autoplay"; f.loading = "lazy";
      f.className = "ep-embed";
      li.appendChild(f); li.dataset.loaded = "1"; li.classList.add("loaded");
      btn.setAttribute("aria-expanded", "true");
    });
  });

  /* -------- YouTube: facade until pressed, then the real embed --------- */
  $$("[data-video]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var card = btn.parentNode, id = btn.dataset.video;
      pause();
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = btn.getAttribute("aria-label") || "Video";
      f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true; f.className = "vid-frame"; f.loading = "lazy";
      card.replaceChild(f, btn);
    });
  });

  /* ==================================================================== */
  /*  EVENTS — the page keeps itself current                              */
  /*  The server-rendered list is the floor; this reconciles it against    */
  /*  the station's own calendar while the page is open.                   */
  /* ==================================================================== */
  var evStatus = $("[data-ev-status]"), evList = $("[data-ev-list]");
  function evClean(txt) {
    return (txt || "").replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .replace(/^[A-Z][a-z]+ \d{1,2}:\s*/, "")
      .split("Optional Reserved Seats")[0]
      .split("All concerts begin")[0]
      .trim().slice(0, 200);
  }
  function evRender(list) {
    var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    var DOW = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
    var FULL = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    var seen = null, html_ = "";
    list.forEach(function (e, i) {
      var d = new Date(e.start.replace(" ", "T"));
      if (isNaN(d)) return;
      var m = FULL[d.getMonth()] + " " + d.getFullYear();
      if (m !== seen) { seen = m; html_ += '<li class="ev-month"><span>' + esc(m) + '</span></li>'; }
      var hr = d.getHours(), ap = hr >= 12 ? "PM" : "AM", h12 = hr % 12 || 12;
      var mins = d.getMinutes();
      var time = e.all_day ? "All day" : h12 + ":" + (mins < 10 ? "0" : "") + mins + " " + ap;
      html_ += '<li class="ev reveal in reveal-d' + (i % 4) + '" data-ev-start="' + esc(e.start) + '">' +
        '<time class="ev-date" datetime="' + d.toISOString() + '">' +
          '<span class="ev-mon">' + MON[d.getMonth()] + '</span>' +
          '<span class="ev-day">' + d.getDate() + '</span>' +
          '<span class="ev-dow">' + DOW[d.getDay()] + '</span></time>' +
        '<div class="ev-body"><h3 class="ev-title"><a href="' + esc(e.url) + '" target="_blank" rel="noopener">' +
          esc(e.title) + '</a></h3>' +
        '<p class="ev-meta">' + esc(time) + '<span class="ev-dot">·</span>' + esc(e.venue || "Venue TBA") + '</p>' +
        '<p class="ev-where">' + esc(e.address || "") + '</p></div>' +
        '<span class="ev-cost">' + esc(e.cost || "Free") + '</span></li>';
    });
    if (!html_) html_ = '<li class="ev-empty">No dates on the calendar right now — new concerts are announced on the air first.</li>';
    evList.innerHTML = html_;
  }
  function evCountdown() {
    var box = $("[data-ev-countdown]"); if (!box) return;
    var first = $(".ev[data-ev-start]", evList || document);
    if (!first) { box.hidden = true; return; }
    var when = new Date(first.dataset.evStart.replace(" ", "T"));
    var title = $(".ev-title", first);
    var nm = $("[data-cd-name]", box), ck = $("[data-cd-clock]", box);
    function tick() {
      var ms = when - new Date();
      if (isNaN(ms) || ms <= 0) { box.hidden = true; return; }
      var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), mi = Math.floor(ms % 36e5 / 6e4);
      ck.textContent = (d ? d + (d === 1 ? " day " : " days ") : "") + h + "h " + mi + "m";
      box.hidden = false;
    }
    if (nm && title) nm.textContent = title.textContent;
    tick(); setInterval(tick, 60000);
  }
  if (evList && evStatus && window.fetch) {
    var endpoint = evStatus.dataset.evEndpoint;
    var statusText = $("[data-ev-status-text]", evStatus);
    fetch(endpoint, { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var list = (d.events || []).map(function (e) {
          var v = e.venue || {};
          return {
            start: e.start_date, all_day: !!e.all_day, url: e.url,
            title: (e.title || "").replace(/&#(\d+);/g, function (_, n) { return String.fromCharCode(n); })
                     .replace(/&amp;/g, "&").replace(/&#8217;/g, "’"),
            cost: (e.cost || "").trim(),
            venue: v.venue || "",
            address: [v.address, v.city, v.state, v.zip].filter(Boolean).join(" "),
            blurb: evClean(e.description || e.excerpt)
          };
        }).filter(function (e) { return e.start; })
          .sort(function (a, b) { return a.start < b.start ? -1 : 1; });
        evRender(list);
        evStatus.classList.add("is-live");
        if (statusText) statusText.textContent = "Live from the station calendar · updated just now";
        evCountdown();
      })
      .catch(function () {
        evStatus.classList.add("is-cached");
        if (statusText) statusText.textContent = "Showing the last saved schedule — the live calendar didn't answer";
        evCountdown();
      });
  } else if (evList) { evCountdown(); }

  /* ---------------- show page: is this programme on right now? --------- */
  var showLive = $("[data-show-live]");
  if (showLive && Object.keys(SCHEDULE).length) {
    var showHero = showLive.closest("[data-show]");
    var wanted = showHero ? (showHero.dataset.show || "").toLowerCase() : "";
    var checkLive = function () {
      var cur = currentSlot();
      var on = !!(cur && wanted && (cur.slot.show || "").toLowerCase().indexOf(wanted.slice(0, 18)) > -1);
      showLive.hidden = !on;
    };
    checkLive(); setInterval(checkLive, 30000);
  }

  /* --------------------------------------------------- footer year + boot */
  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
  reflectUI();
})();
