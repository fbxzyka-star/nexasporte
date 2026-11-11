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

Stadium photo by Mario Klassen on [Unsplash](https://unsplash.com/photos/70YxSTWa2Zw).
