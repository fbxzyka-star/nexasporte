// Nexasporte — site interactions
(function () {
  "use strict";

  // Where contact-form messages are sent (opens the visitor's email app).
  var CONTACT_EMAIL = "info@nexasporte.com";

  var doc = document.documentElement;
  var header = document.querySelector(".site-header");
  var toggle = document.getElementById("nav-toggle");
  var navLinks = document.getElementById("nav-links");

  /* ---------- Header background on scroll ---------- */
  function onScroll() {
    header.classList.toggle("scrolled", window.scrollY > 20);
    document.body.classList.toggle("past-hero", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Smooth slide from the hero to the next section ----------
     A small scroll / swipe / arrow key inside the hero glides the page
     to the Features section (and back up to the top). Only active when
     the whole hero fits on screen, so nothing in it can be skipped. */
  var hero = document.getElementById("home");
  var nextSection = hero.nextElementSibling;
  var scrollDown = document.getElementById("scroll-down");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var animating = false;
  var locked = false;
  var lastInput = 0;

  function headerOffset() {
    return header.offsetHeight - 8;
  }
  function nextTop() {
    return Math.max(0, nextSection.offsetTop - headerOffset());
  }
  var heroStrip = hero.querySelector(".hero-strip");
  function heroFits() {
    // all hero content (down to the feature strip) is visible on screen
    return heroStrip.getBoundingClientRect().bottom + window.scrollY <= window.innerHeight + 4;
  }
  function menuOpen() {
    return document.body.classList.contains("nav-open");
  }
  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
  function jumpTo(y) {
    try { window.scrollTo({ top: y, behavior: "instant" }); }
    catch (e) { window.scrollTo(0, y); }
  }

  function glideTo(target) {
    if (reduceMotion.matches) { jumpTo(target); return; }
    var start = window.scrollY;
    var distance = target - start;
    if (Math.abs(distance) < 2) return;
    var duration = Math.min(1100, Math.max(650, Math.abs(distance) * 0.9));
    var t0 = null;
    animating = locked = true;
    doc.style.scrollBehavior = "auto";

    function step(now) {
      if (t0 === null) t0 = now;
      var p = Math.min(1, (now - t0) / duration);
      jumpTo(start + distance * easeInOutCubic(p));
      if (p < 1) {
        requestAnimationFrame(step);
      } else {
        animating = false;
        doc.style.scrollBehavior = "";
        releaseLock();
      }
    }
    requestAnimationFrame(step);
  }

  // Keep swallowing trackpad / touch momentum until it has died down,
  // so the page doesn't keep drifting after the glide.
  function releaseLock() {
    if (animating) return;
    if (performance.now() - lastInput > 220) locked = false;
    else setTimeout(releaseLock, 120);
  }

  // Which way (if any) a scroll gesture at the current position should glide.
  function glideTarget(down) {
    if (menuOpen() || !heroFits()) return null;
    var y = window.scrollY;
    var stop = nextTop();
    if (down && y < stop - 2) return stop;
    if (!down && y > 0 && y <= stop + 2) return 0;
    return null;
  }

  function handleIntent(down, e) {
    lastInput = performance.now();
    if (locked) { if (e.cancelable) e.preventDefault(); return; }
    var target = glideTarget(down);
    if (target === null) return;
    if (e.cancelable) e.preventDefault();
    glideTo(target);
  }

  window.addEventListener("wheel", function (e) {
    if (e.ctrlKey || Math.abs(e.deltaY) < Math.abs(e.deltaX)) return; // pinch-zoom / sideways
    if (Math.abs(e.deltaY) < 1) return;
    handleIntent(e.deltaY > 0, e);
  }, { passive: false });

  var touchY = null;
  window.addEventListener("touchstart", function (e) {
    touchY = e.touches.length === 1 ? e.touches[0].clientY : null;
  }, { passive: true });
  window.addEventListener("touchmove", function (e) {
    if (locked) { lastInput = performance.now(); if (e.cancelable) e.preventDefault(); return; }
    if (touchY === null) return;
    var dy = touchY - e.touches[0].clientY;
    if (dy === 0) return;
    var target = glideTarget(dy > 0);
    if (target === null) return;             // normal native scrolling
    if (e.cancelable) e.preventDefault();    // hold the page still until the swipe is clear
    if (Math.abs(dy) < 8) return;
    lastInput = performance.now();
    touchY = null;
    glideTo(target);
  }, { passive: false });

  window.addEventListener("keydown", function (e) {
    var t = e.target;
    if (t.closest && t.closest("input, textarea, select, button, [contenteditable]")) return;
    var down = e.key === "ArrowDown" || e.key === "PageDown" || (e.key === " " && !e.shiftKey);
    var up = e.key === "ArrowUp" || e.key === "PageUp" || (e.key === " " && e.shiftKey);
    if (!down && !up) return;
    handleIntent(down, e);
  });

  scrollDown.addEventListener("click", function (e) {
    e.preventDefault();
    glideTo(nextTop());
  });

  /* ---------- Mobile menu ---------- */
  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  toggle.addEventListener("click", function () {
    setMenu(!document.body.classList.contains("nav-open"));
  });
  navLinks.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });

  /* ---------- Active nav link while scrolling ---------- */
  var links = Array.prototype.slice.call(navLinks.querySelectorAll("a:not(.btn)"));
  var sectionIds = links.map(function (a) { return a.getAttribute("href").slice(1); });
  var sections = sectionIds
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  function setActive(id) {
    links.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("href") === "#" + id);
    });
  }

  function updateActive() {
    var mark = window.scrollY + window.innerHeight * 0.35;
    var current = sections[0].id;
    sections.forEach(function (s) {
      if (s.offsetTop <= mark) current = s.id;
    });
    // Treat sections between nav items (demo, how) as part of the previous nav item
    setActive(current);
  }
  updateActive();
  window.addEventListener("scroll", updateActive, { passive: true });
  window.addEventListener("resize", updateActive);

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    revealEls.forEach(function (el, i) {
      // small stagger for items inside grids
      var parent = el.parentElement;
      var siblings = parent ? parent.querySelectorAll(":scope > .reveal") : [];
      var idx = Array.prototype.indexOf.call(siblings, el);
      if (idx > 0) el.style.transitionDelay = Math.min(idx * 80, 320) + "ms";
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Pricing buttons pre-select the plan ---------- */
  var planSelect = document.getElementById("plan-select");
  document.querySelectorAll("[data-plan]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      planSelect.value = btn.getAttribute("data-plan");
    });
  });

  /* ---------- Contact form → email ---------- */
  document.querySelectorAll(".js-email").forEach(function (a) {
    a.href = "mailto:" + CONTACT_EMAIL;
    a.textContent = CONTACT_EMAIL;
  });

  var form = document.getElementById("contact-form");
  var note = document.getElementById("form-note");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var invalid = [];
    form.querySelectorAll("[required]").forEach(function (field) {
      var ok = field.value.trim() !== "" && (field.type !== "email" || /^\S+@\S+\.\S+$/.test(field.value));
      field.classList.toggle("invalid", !ok);
      if (!ok) invalid.push(field);
    });

    if (invalid.length) {
      note.textContent = "Please fill in your name, club and a valid email.";
      note.classList.add("error");
      invalid[0].focus();
      return;
    }

    var d = new FormData(form);
    var subject = "New club website request — " + d.get("club");
    var body = [
      "Name: " + d.get("name"),
      "Club / Academy: " + d.get("club"),
      "Email: " + d.get("email"),
      "Phone: " + (d.get("phone") || "-"),
      "Sport: " + d.get("sport"),
      "Plan: " + d.get("plan"),
      "",
      d.get("message") || ""
    ].join("\n");

    window.location.href = "mailto:" + CONTACT_EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);

    note.classList.remove("error");
    note.textContent = "Opening your email app… Thank you!";
  });

  form.addEventListener("input", function (e) {
    if (e.target.classList.contains("invalid")) e.target.classList.remove("invalid");
  });

  /* ---------- Hero background slideshow ----------
     The first photo is in the CSS and shows immediately. The others are
     downloaded in the background after the page has loaded (in the size
     that suits the screen) and join the rotation once they are ready. */
  (function heroSlideshow() {
    var slides = Array.prototype.slice.call(document.querySelectorAll(".hero-slide"));
    if (slides.length < 2 || reduceMotion.matches) return;

    var SHOW_MS = 4000;          // a new photo every 4 seconds
    var FADE_MS = 1200;          // must match the CSS opacity transition
    var current = 0;
    var timer = null;
    var heroVisible = true;

    slides[0].ready = true;

    function pickSrc(el) {
      if (window.matchMedia("(max-width: 640px)").matches) return el.getAttribute("data-src-sm");
      if (window.matchMedia("(max-width: 1400px)").matches) return el.getAttribute("data-src-md");
      return el.getAttribute("data-src-lg");
    }

    function loadSlide(el) {
      return new Promise(function (resolve) {
        var src = pickSrc(el);
        var img = new Image();
        img.onload = function () {
          var show = function () {
            el.style.backgroundImage = 'url("' + src + '")';
            el.ready = true;
            resolve();
          };
          if (img.decode) img.decode().then(show, show); else show();
        };
        img.onerror = function () { resolve(); };
        img.src = src;
      });
    }

    function nextReady() {
      for (var i = 1; i < slides.length; i++) {
        var idx = (current + i) % slides.length;
        if (slides[idx].ready) return idx;
      }
      return -1;
    }

    function advance() {
      var next = nextReady();
      if (next === -1) return;
      var prev = slides[current];
      var incoming = slides[next];

      prev.classList.remove("is-active");
      prev.classList.add("is-leaving");
      // restart the zoom on the incoming photo
      incoming.classList.remove("is-leaving");
      void incoming.offsetWidth;
      incoming.classList.add("is-active");
      setTimeout(function () { prev.classList.remove("is-leaving"); }, FADE_MS + 50);
      current = next;
    }

    function schedule() {
      clearTimeout(timer);
      if (document.hidden || !heroVisible) return;
      timer = setTimeout(function () { advance(); schedule(); }, SHOW_MS);
    }

    // pause while the tab is hidden or the hero is scrolled out of view
    document.addEventListener("visibilitychange", schedule);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        heroVisible = entries[0].isIntersecting;
        schedule();
      }).observe(hero);
    }

    function start() {
      // load the remaining photos one after another so they don't compete
      slides.slice(1).reduce(function (p, el) {
        return p.then(function () { return loadSlide(el); });
      }, Promise.resolve());
      schedule();
    }
    if (document.readyState === "complete") start();
    else window.addEventListener("load", start);
  })();

  /* ---------- Tagline: spread letters evenly to the wordmark width ---------- */
  var taglines = document.querySelectorAll(".brand-tagline");
  function fitTaglines() {
    taglines.forEach(function (el) {
      var inner = el.firstElementChild;
      var target = el.parentElement.clientWidth;
      if (!target) return;
      el.style.letterSpacing = "0px";
      var natural = inner.getBoundingClientRect().width;
      var chars = inner.textContent.length;
      var ls = Math.max(0, (target - natural) / (chars - 1));
      el.style.letterSpacing = ls + "px";
      inner.style.marginRight = -ls + "px"; // no trailing gap after the last letter
    });
  }
  fitTaglines();
  window.addEventListener("resize", fitTaglines);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitTaglines);

  /* ---------- Footer year ---------- */
  document.getElementById("year").textContent = new Date().getFullYear();

  doc.classList.remove("no-js");
})();
