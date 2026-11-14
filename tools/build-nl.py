#!/usr/bin/env python3
"""Build the Dutch page (nl/index.html) from the English index.html.

Run from the repository root after changing index.html:

    python3 tools/build-nl.py

Every English text below must still exist in index.html; if one was
changed or removed, the script stops and names it, so the translation
never silently falls out of date.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "nl" / "index.html"

# (English, Dutch) — exact substrings of index.html, applied in order.
T = [
    # --- head ---
    ('<html lang="en" class="no-js">', '<html lang="nl" class="no-js">'),
    ('<title>Nexasporte · Websites for Sports Clubs &amp; Academies in Belgium</title>',
     '<title>Nexasporte · Websites voor sportclubs en academies in België</title>'),
    ('content="Websites for sports clubs and academies in Antwerp and across Belgium: fixtures, live results, standings, news and sponsors. Fast, mobile-friendly, professional."',
     'content="Websites voor sportclubs en academies in Antwerpen en heel België: kalender, live uitslagen, klassementen, nieuws en sponsors. Snel, mobielvriendelijk en professioneel."'),
    ('<link rel="canonical" href="https://nexasporte.com/" />',
     '<link rel="canonical" href="https://nexasporte.com/nl/" />'),
    ('<meta property="og:url" content="https://nexasporte.com/" />',
     '<meta property="og:url" content="https://nexasporte.com/nl/" />\n  <meta property="og:locale" content="nl_BE" />'),
    ('<meta property="og:title" content="Nexasporte · Your Club. Online. Professional." />',
     '<meta property="og:title" content="Nexasporte · Jouw club. Online. Professioneel." />'),
    ('"description": "Websites for sports clubs and academies in Antwerp and across Belgium."',
     '"description": "Websites voor sportclubs en academies in Antwerpen en heel België."'),

    # --- header ---
    ('<a href="#home" class="active">Home</a>', '<a href="#home" class="active">Home</a>'),
    ('<a href="#features">Features</a>\n        <a href="#pricing">Pricing</a>\n        <a href="#about">About</a>\n        <a href="#contact">Contact</a>\n        <a href="#contact" class="btn btn-outline nav-cta-mobile">Get Started',
     '<a href="#features">Functies</a>\n        <a href="#pricing">Prijzen</a>\n        <a href="#about">Over ons</a>\n        <a href="#contact">Contact</a>\n        <a href="#contact" class="btn btn-outline nav-cta-mobile">Start nu'),
    ('class="btn btn-outline nav-cta">Get Started', 'class="btn btn-outline nav-cta">Start nu'),
    ('aria-label="Open menu"', 'aria-label="Menu openen"'),

    # --- hero ---
    ('<span class="dot"></span> For Local Sports Teams', '<span class="dot"></span> Voor lokale sportclubs'),
    ('<h1>Your Club.<br />Online. <span class="accent">Professional.</span></h1>',
     '<h1>Jouw club.<br />Online. <span class="accent">Professioneel.</span></h1>'),
    ('<p class="lead">Modern websites for local sports teams<br class="br-desktop" /> and academies – powered by Nexasporte.</p>',
     '<p class="lead">Moderne websites voor lokale sportclubs<br class="br-desktop" /> en academies – powered by Nexasporte.</p>'),
    ('class="btn btn-primary btn-lg">Get Your Club Website', 'class="btn btn-primary btn-lg">Vraag je clubwebsite aan'),
    ('aria-label="Proud digital sponsor of FC Vezhdanisht – visit the club website (opens in a new tab)"',
     'aria-label="Trotse digitale sponsor van FC Vezhdanisht – bezoek de clubwebsite (opent in een nieuw tabblad)"'),
    ('<small>Proud digital sponsor of</small>', '<small>Trotse digitale sponsor van</small>'),
    ('<strong>Fast &amp; Reliable</strong><small>Hosting &amp; security included</small>',
     '<strong>Snel &amp; betrouwbaar</strong><small>Hosting &amp; beveiliging inbegrepen</small>'),
    ('<strong>Live Results &amp; Standings</strong><small>Updated in seconds</small>',
     '<strong>Live uitslagen &amp; klassement</strong><small>In enkele seconden bijgewerkt</small>'),
    ('<strong>Mobile Friendly</strong><small>Looks great on every screen</small>',
     '<strong>Mobielvriendelijk</strong><small>Ziet er goed uit op elk scherm</small>'),
    ('<strong>Boost Your Club’s Presence</strong><small>More fans, more sponsors</small>',
     '<strong>Meer zichtbaarheid voor je club</strong><small>Meer fans, meer sponsors</small>'),
    ('aria-label="Scroll down"', 'aria-label="Naar beneden scrollen"'),

    # --- features ---
    ('<p class="eyebrow">Features</p>', '<p class="eyebrow">Functies</p>'),
    ('<h2>Everything your club needs, <span class="accent">in one place.</span></h2>',
     '<h2>Alles wat je club nodig heeft, <span class="accent">op één plek.</span></h2>'),
    ('From the first-team squad to the youngest academy players — give your fans, parents and sponsors a home online.',
     'Van de eerste ploeg tot de jongste jeugdspelers — geef je fans, ouders en sponsors een thuis online.'),
    ('<h3>Teams &amp; Player Profiles</h3>\n            <p>Squads for every age group with photos, positions, numbers and stats.</p>',
     '<h3>Ploegen &amp; spelersprofielen</h3>\n            <p>Ploegen voor elke leeftijdscategorie met foto’s, posities, rugnummers en statistieken.</p>'),
    ('<h3>Fixtures &amp; Live Results</h3>\n            <p>Upcoming matches, live scores and full-time results updated in seconds.</p>',
     '<h3>Kalender &amp; live uitslagen</h3>\n            <p>Komende wedstrijden, live scores en eindstanden, in enkele seconden bijgewerkt.</p>'),
    ('<h3>League Standings</h3>\n            <p>Clear, always up-to-date tables for every competition you play in.</p>',
     '<h3>Klassementen</h3>\n            <p>Overzichtelijke, altijd actuele rangschikkingen voor elke competitie waarin je speelt.</p>'),
    ('<h3>News &amp; Photo Gallery</h3>\n            <p>Share match reports, announcements and photos from every game day.</p>',
     '<h3>Nieuws &amp; fotogalerij</h3>\n            <p>Deel wedstrijdverslagen, aankondigingen en foto’s van elke speeldag.</p>'),
    ('<h3>Sponsors Showcase</h3>\n            <p>Give your sponsors the visibility they deserve — and attract new ones.</p>',
     '<h3>Sponsors in de kijker</h3>\n            <p>Geef je sponsors de zichtbaarheid die ze verdienen — en trek nieuwe aan.</p>'),
    ('<h3>Online Registrations</h3>\n            <p>Let new players and parents sign up for trials and academies online.</p>',
     '<h3>Online inschrijvingen</h3>\n            <p>Laat nieuwe spelers en ouders zich online inschrijven voor proeftrainingen en academies.</p>'),

    # --- our work ---
    ('<p class="eyebrow">Our work</p>', '<p class="eyebrow">Ons werk</p>'),
    ('<h2>See what your club <span class="accent">gets.</span></h2>',
     '<h2>Ontdek wat je club <span class="accent">krijgt.</span></h2>'),
    ('A clean, branded website in your club colours — built to look great on every phone and easy to update after every match.',
     'Een strakke website in je clubkleuren — gemaakt om er op elke smartphone goed uit te zien en eenvoudig bij te werken na elke wedstrijd.'),
    ('<li>Your crest, colours and domain name</li>', '<li>Je clublogo, kleuren en domeinnaam</li>'),
    ('<li>Simple admin panel — no technical skills needed</li>', '<li>Eenvoudig beheer — geen technische kennis nodig</li>'),
    ('<li>Fast hosting, SSL security and backups included</li>', '<li>Snelle hosting, SSL-beveiliging en back-ups inbegrepen</li>'),
    ('<li>Google-friendly so fans can find you</li>', '<li>Google-vriendelijk, zodat fans je vinden</li>'),
    ('class="btn btn-primary">Request a Free Demo', 'class="btn btn-primary">Vraag een gratis demo aan'),
    ('aria-label="FC Vezhdanisht website, made by Nexasporte (opens in a new tab)"',
     'aria-label="Website van FC Vezhdanisht, gemaakt door Nexasporte (opent in een nieuw tabblad)"'),
    ('alt="Homepage of the FC Vezhdanisht website: next match, countdown and fixtures"',
     'alt="Homepagina van de website van FC Vezhdanisht: volgende wedstrijd, aftelklok en kalender"'),
    ('<span class="browser-tag">Live client site · Visit ↗</span>', '<span class="browser-tag">Live klantensite · Bekijk ↗</span>'),

    # --- how it works ---
    ('<p class="eyebrow">How it works</p>', '<p class="eyebrow">Hoe het werkt</p>'),
    ('<h2>From kick-off to online <span class="accent">in 3 steps.</span></h2>',
     '<h2>Van aftrap tot online <span class="accent">in 3 stappen.</span></h2>'),
    ('<h3>Tell us about your club</h3>\n            <p>Send us your logo, colours, teams and the content you want to show.</p>',
     '<h3>Vertel ons over je club</h3>\n            <p>Stuur ons je logo, kleuren, ploegen en de inhoud die je wilt tonen.</p>'),
    ('<h3>We design &amp; build</h3>\n            <p>We create a professional website tailored to your club and your sport.</p>',
     '<h3>Wij ontwerpen &amp; bouwen</h3>\n            <p>We maken een professionele website op maat van je club en je sport.</p>'),
    ('<h3>Go live &amp; score</h3>\n            <p>Launch on your own domain and update results and news in seconds.</p>',
     '<h3>Online gaan &amp; scoren</h3>\n            <p>Lanceer op je eigen domein en werk uitslagen en nieuws in enkele seconden bij.</p>'),

    # --- pricing ---
    ('<p class="eyebrow">Pricing</p>', '<p class="eyebrow">Prijzen</p>'),
    ('<h2>Two simple ways <span class="accent">to get online.</span></h2>',
     '<h2>Twee eenvoudige manieren <span class="accent">om online te gaan.</span></h2>'),
    ('Same professional website, same care. Pick what suits your club’s budget.',
     'Dezelfde professionele website, dezelfde zorg. Kies wat past bij het budget van je club.'),
    ('<h3>Direct Buy</h3>', '<h3>Eenmalige aankoop</h3>'),
    ('<p class="plan-desc">Pay once for your website, then a small yearly fee.</p>',
     '<p class="plan-desc">Betaal één keer voor je website, daarna een kleine jaarlijkse bijdrage.</p>'),
    ('<span class="per">one-off</span>', '<span class="per">eenmalig</span>'),
    ('<span class="free-badge">1st year free</span> After that <strong>€80 / year</strong> for hosting, domain, security &amp; updates. Cancel anytime.',
     '<span class="free-badge">1e jaar gratis</span> Daarna <strong>€80 / jaar</strong> voor hosting, domein, beveiliging &amp; updates. Altijd opzegbaar.'),
    ('<li>Your website, built and launched</li>\n              <li>You own the full code — take it to any developer, anytime</li>\n              <li>Lowest cost over the years</li>',
     '<li>Je website, gebouwd en gelanceerd</li>\n              <li>De volledige code is van jou — neem ze mee naar elke ontwikkelaar, wanneer je wilt</li>\n              <li>Laagste kost op lange termijn</li>'),
    ('data-plan="Direct Buy">Choose Direct Buy', 'data-plan="Direct Buy">Kies eenmalige aankoop'),
    ('<span class="plan-tag">No upfront cost</span>', '<span class="plan-tag">Geen opstartkosten</span>'),
    ('<h3>Monthly Plan</h3>', '<h3>Maandabonnement</h3>'),
    ('<p class="plan-desc">Start today without a big investment.</p>',
     '<p class="plan-desc">Start vandaag zonder grote investering.</p>'),
    ('<span class="per">/ month</span>', '<span class="per">/ maand</span>'),
    ('<strong>€0</strong> to get started · domain, hosting, security &amp; updates included',
     '<strong>€0</strong> opstartkosten · domein, hosting, beveiliging &amp; updates inbegrepen'),
    ('<li>Your website, built and launched</li>\n              <li>Everything included, one monthly price</li>\n              <li>Cancel anytime, no commitment</li>\n              <li><strong>Off-season?</strong> After 6 active months, pause your site for free for up to 6 months.</li>',
     '<li>Je website, gebouwd en gelanceerd</li>\n              <li>Alles inbegrepen, één maandprijs</li>\n              <li>Altijd opzegbaar, geen verplichtingen</li>\n              <li><strong>Buiten het seizoen?</strong> Na 6 actieve maanden kun je je site tot 6 maanden gratis pauzeren.</li>'),
    ('<span class="extra-label">Optional</span>', '<span class="extra-label">Optioneel</span>'),
    ('After 6 paid months you can buy your website outright for <strong>€150</strong> and continue at €80 / year. Paused months don’t count towards the 6.',
     'Na 6 betaalde maanden kun je je website volledig overkopen voor <strong>€150</strong> en verdergaan aan €80 / jaar. Gepauzeerde maanden tellen niet mee.'),
    ('data-plan="Monthly Plan">Choose Monthly Plan', 'data-plan="Monthly Plan">Kies maandabonnement'),
    ('<p class="includes-title">Every website includes</p>', '<p class="includes-title">Elke website bevat</p>'),
    ('<li>Your crest, colours &amp; own domain</li>', '<li>Je clublogo, kleuren &amp; eigen domein</li>'),
    ('<li>Fixtures, results &amp; standings</li>', '<li>Kalender, uitslagen &amp; klassement</li>'),
    ('<li>Teams, news &amp; sponsors</li>', '<li>Ploegen, nieuws &amp; sponsors</li>'),
    ('<li>Mobile-friendly &amp; Google-ready</li>', '<li>Mobielvriendelijk &amp; klaar voor Google</li>'),
    ('<span><strong>Cancel anytime</strong>No contracts. Stop the €80 / year plan whenever you like: you get your full code to host it yourself or with another developer. On the Monthly Plan, the site goes offline when you cancel unless you buy it out.</span>',
     '<span><strong>Altijd opzegbaar</strong>Geen contracten. Stop het jaarplan van €80 wanneer je wilt: je krijgt je volledige code om de site zelf of bij een andere ontwikkelaar te hosten. Bij het maandabonnement gaat de site offline wanneer je opzegt, tenzij je hem overkoopt.</span>'),
    ('<span><strong>Your domain belongs to your club</strong>We manage it for you. Leaving? We transfer it to you for €12, hand over your code and delete our copy.</span>',
     '<span><strong>Je domein is van je club</strong>Wij beheren het voor je. Vertrek je? Dan dragen we het voor €12 aan je over, geven we je de code en verwijderen we onze kopie.</span>'),
    ('<p class="price-note">All prices incl. VAT.</p>', '<p class="price-note">Alle prijzen incl. btw.</p>'),
    ('<span><strong>See it before you pay</strong>We build a free demo of your website first and shape it to your wishes. You only pay when you’re happy with it.</span>',
     '<span><strong>Eerst zien, dan betalen</strong>We maken eerst een gratis demo van je website en passen die aan jouw wensen aan. Je betaalt pas als je tevreden bent.</span>'),
    ('<option>Direct Buy</option>', '<option value="Direct Buy">Eenmalige aankoop</option>'),
    ('<option>Monthly Plan</option>', '<option value="Monthly Plan">Maandabonnement</option>'),

    # --- about ---
    ('<p class="eyebrow">About</p>', '<p class="eyebrow">Over ons</p>'),
    ('Nexasporte was created with one goal: to give every local club and academy the same professional online presence as the big teams — without the big budget.',
     'Nexasporte is ontstaan met één doel: elke lokale club en academie dezelfde professionele online uitstraling geven als de grote ploegen — zonder het grote budget.'),
    ('We combine modern web technology with a real love for sport. Football, basketball, volleyball, tennis, martial arts — whatever you play, we build a website that makes your club proud.',
     'We combineren moderne webtechnologie met een echte passie voor sport. Voetbal, basketbal, volleybal, tennis, vechtsport — welke sport je ook speelt, wij bouwen een website waar je club trots op is.'),
    ('<strong>Built for sport</strong><span>Features designed around clubs, not generic templates.</span>',
     '<strong>Gemaakt voor sport</strong><span>Functies ontworpen rond clubs, geen standaard sjablonen.</span>'),
    ('<strong>Personal support</strong><span>A real person helps you every step of the way.</span>',
     '<strong>Persoonlijke ondersteuning</strong><span>Een echt persoon helpt je bij elke stap.</span>'),

    # --- CTA ---
    ('<h2>Ready to take your club <span class="accent">online?</span></h2>',
     '<h2>Klaar om je club <span class="accent">online te brengen?</span></h2>'),

    # --- contact ---
    ('<h2>Let’s build your <span class="accent">club website.</span></h2>',
     '<h2>Laten we je <span class="accent">clubwebsite bouwen.</span></h2>'),
    ('Tell us a little about your club and we’ll get back to you within 24 hours with ideas and a free demo.',
     'Vertel ons iets over je club en we nemen binnen 24 uur contact met je op met ideeën en een gratis demo.'),
    ('<span>Antwerp, Belgium</span>', '<span>Antwerpen, België</span>'),
    ('<label>Your name', '<label>Je naam'),
    ('<label>Club / Academy', '<label>Club / academie'),
    ('<label>Email', '<label>E-mail'),
    ('<label>Phone', '<label>Telefoon'),
    ('<option>Football</option>', '<option value="Football">Voetbal</option>'),
    ('<option>Basketball</option>', '<option value="Basketball">Basketbal</option>'),
    ('<option>Volleyball</option>', '<option value="Volleyball">Volleybal</option>'),
    ('<option>Handball</option>', '<option value="Handball">Handbal</option>'),
    ('<option>Martial Arts</option>', '<option value="Martial Arts">Vechtsport</option>'),
    ('<option>Other</option>', '<option value="Other">Andere</option>'),
    ('<label>Plan', '<label>Pakket'),
    ('<option>Not sure yet</option>', '<option value="Not sure yet">Nog niet zeker</option>'),
    ('<label>Message', '<label>Bericht'),
    ('placeholder="Tell us about your club…"', 'placeholder="Vertel ons over je club…"'),
    ('class="btn btn-primary btn-block">Send Message', 'class="btn btn-primary btn-block">Verstuur bericht'),
    ('We only use your details to reply to you. No cookies, no tracking.',
     'We gebruiken je gegevens alleen om je te antwoorden. Geen cookies, geen tracking.'),
    ('<a href="privacy.html">Privacy Policy</a></p>', '<a href="privacy.html">Privacybeleid (EN)</a></p>'),

    # --- footer ---
    ('<a href="#features">Features</a>\n        <a href="#pricing">Pricing</a>\n        <a href="#about">About</a>\n        <a href="#contact">Contact</a>\n        <a href="privacy.html">Privacy Policy</a>',
     '<a href="#features">Functies</a>\n        <a href="#pricing">Prijzen</a>\n        <a href="#about">Over ons</a>\n        <a href="#contact">Contact</a>\n        <a href="privacy.html">Privacybeleid</a>'),
    ('<span>Proud digital sponsor of <strong>FC Vezhdanisht</strong></span>',
     '<span>Trotse digitale sponsor van <strong>FC Vezhdanisht</strong></span>'),
]

# Language switch: EN page points to nl/, NL page points back to the root.
SWITCH_EN = '<a href="./" lang="en" aria-current="true">EN</a><a href="nl/" lang="nl" hreflang="nl">NL</a>'
SWITCH_NL = '<a href="../" lang="en" hreflang="en">EN</a><a href="./" lang="nl" aria-current="true">NL</a>'


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    missing = []
    for en, nl in T:
        if en not in html:
            missing.append(en)
            continue
        html = html.replace(en, nl)
    if missing:
        print("These English texts were not found in index.html (update tools/build-nl.py):", file=sys.stderr)
        for m in missing:
            print("  - " + m[:110].replace("\n", "\\n"), file=sys.stderr)
        return 1

    if SWITCH_EN not in html:
        print("Language switch not found in index.html", file=sys.stderr)
        return 1
    html = html.replace(SWITCH_EN, SWITCH_NL)

    # The NL page lives one folder down: point local files one level up.
    html = re.sub(r'(\s(?:src|href|data-src-(?:lg|md|sm))=")(?!https?:|mailto:|#|\.\./|\./)([^"]+")', r'\1../\2', html)
    html = re.sub(r'(srcset=")([^"]+)(")',
                  lambda m: m.group(1) + ", ".join("../" + p.strip() for p in m.group(2).split(",")) + m.group(3), html)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(T)} texts translated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
