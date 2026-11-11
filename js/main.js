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
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

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

  /* ---------- Footer year ---------- */
  document.getElementById("year").textContent = new Date().getFullYear();

  doc.classList.remove("no-js");
})();
