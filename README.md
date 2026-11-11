# Nexasporte

**Intelligent & Sport Solutions** — modern websites for local sports teams and academies.

This is the Nexasporte company website: a fast, static, mobile-friendly landing page.

## Structure

```
index.html          Main page (Home, Features, Demo, How it works, Pricing, About, Contact)
css/style.css       All styles (colours are in the :root variables at the top)
js/main.js          Mobile menu, scroll effects, contact form
assets/img/         Web-ready images (logo, stadium photo in 3 sizes, favicon, social preview)
assets/source/      Full-resolution originals (not used by the page directly)
```

## Run locally

Just open `index.html` in a browser, or start a small local server:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000

## Things to customise

- **Email address** — `CONTACT_EMAIL` at the top of `js/main.js` (the contact form opens the visitor's email app with the message filled in).
- **Prices** — in the `#pricing` section of `index.html`.
- **Brand colour** — `--green` in `css/style.css`.

## Deploy

It's a static site, so it works on GitHub Pages, Netlify, Vercel or Cloudflare Pages with no build step.
For GitHub Pages: *Settings → Pages → Deploy from branch → `main` / root*.

## Credits

Photos from [Unsplash](https://unsplash.com):

- Football stadium — Mario Klassen ([photo](https://unsplash.com/photos/70YxSTWa2Zw))
- Basketball — Markus Spiske ([photo](https://unsplash.com/photos/0It4NhP_9kQ))
- Pickleball — Hoi Pham ([photo](https://unsplash.com/photos/79UPJtBsSAg))
- Handball — Krystof Zajicek ([photo](https://unsplash.com/photos/xu1A9u0P4Fc))

## Hero slideshow

The hero background rotates through the photos with a crossfade and a slow zoom-out.
To add another sport: put web-ready versions in `assets/img/` (`<name>-3200.webp`, `-2400`, `-1600`)
and copy one of the `<div class="hero-slide ...">` lines in `index.html` with the new file names.
Timing is set by `SHOW_MS` in `js/main.js`.
