"""Skapar undersidorna Tjänster, Priser, FAQ och Kontakt från startsidan (site/index.html).
Körs av build-site.sh. Innehållet ändras alltså bara i sabimedia.html – sidorna följer med."""
import html as H, json, re

src = open("site/index.html", encoding="utf-8").read()

def one(text, old, new):
    if text.count(old) != 1:
        raise SystemExit(f"build-pages: hittade {text.count(old)} av: {old[:80]}")
    return text.replace(old, new)

def section(sid):
    m = re.search(r'  <section class="section[^"]*" id="%s".*?\n  </section>\n' % sid, src, re.S)
    if not m: raise SystemExit("build-pages: sektionen saknas: " + sid)
    return m.group(0)

def next_step(h, p, btns):
    links = "".join(f'<a class="btn {c}" href="{u}">{t}</a>' for c, u, t in btns)
    return f'''  <section class="section next-step" style="padding-top:0">
    <div class="wrap"><div class="next-box"><div><h2>{h}</h2><p>{p}</p></div><div class="next-btns">{links}</div></div></div>
  </section>
'''

def cookie_munch():
    """Exemplet och omdömet från startsidan, samlade i en egen sektion."""
    stage = re.search(r'        <div class="stage">.*?\n        </div>\n', src, re.S)
    review = re.search(r'        <figure class="review".*?</figure>\n', src, re.S)
    if not stage or not review: raise SystemExit("build-pages: Cookie Munch-exemplet saknas")
    review = re.sub(r'\s*<a class="review-link".*?</a>', "", review.group(0))
    return f'''  <section class="section" id="cookie-munch" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Exempel</span>
        <h2>Så blev det för <em class="hl">Cookie Munch.</em></h2>
        <p class="lead">En webbshop vi har byggt åt ett bageri i Borås, med betalning via Swish och en egen adminsida.</p>
      </div>
      <div class="case-grid">
{stage.group(0).replace("<img ", '<img loading="lazy" ')}{review}      </div>
      <div class="case-btns"><a class="btn btn-accent" href="/kundcase-cookie-munch">Läs hela kundcaset →</a><a class="btn btn-line" href="https://cookiemunch.se" target="_blank" rel="noopener">Besök cookiemunch.se ↗</a></div>
    </div>
  </section>
'''

PAGES = {
    "tjanster": dict(
        menu="Tjänster", title="Tjänster – det här ingår i din hemsida · Sabimedia",
        desc="Egen adminpanel, produkter och varukorg, betalning, beställningar via mejl och en design som är din. Se vad som ingår och hur vi jobbar, steg för steg.",
        eyebrow="Tjänster", parts=["ingar", "sa-funkar-det", "agande"],
        after=next_step("Vad kostar det?", "Tre paket med fast pris. Jämför dem eller fråga oss vad som passar dig.",
                        [("btn-accent", "/priser", "Se priserna →"), ("btn-line", "/kontakt", "Kontakta oss")])),
    "priser": dict(
        menu="Priser", title="Priser och paket – hemsida från 1 200 kr · Sabimedia",
        desc="Jämför paketen Start, Business och Custom. Fast engångspris från 1 200 kr exkl. moms och inga månadsavgifter till oss.",
        eyebrow="Priser", parts=["priser"],
        after=next_step("Osäker på vilket paket som passar?", "Boka ett kostnadsfritt samtal så går vi igenom vad du behöver.",
                        [("btn-accent", "/boka", "Boka samtal →"), ("btn-line", "/faq", "Vanliga frågor")])),
    "faq": dict(
        menu="FAQ", title="Vanliga frågor om hemsidor · Sabimedia",
        desc="Svar på vanliga frågor om pris, tid, ägande, publicering och support när Sabimedia bygger din hemsida.",
        eyebrow="Vanliga frågor", parts=["fragor"], after=""),
    "kontakt": dict(
        menu="Kontakt", title="Kontakt – skicka en förfrågan · Sabimedia",
        desc="Berätta om ditt företag och välj en tid för ett kostnadsfritt samtal. Sabimedia svarar inom 24 timmar.",
        eyebrow="Kontakt", parts=["kontakt"], after=""),
}

CSS = """/* Undersidor skapade av scripts/build-pages.py */
.section-head h1{font-size:clamp(2.2rem,5vw,3.8rem)}
.contact h1{font-size:clamp(2rem,4.4vw,3.2rem);margin:.8rem 0 1rem}
.band + .section{padding-top:clamp(64px,9vw,120px)!important}
.head-btns{margin-top:.6rem}
.case-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,4vw,56px);align-items:center}
.case-grid .stage{min-height:0}
.case-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
#cookie-munch{scroll-margin-top:60px}
@media (max-width:900px){.case-grid{grid-template-columns:minmax(0,1fr)}}
.only-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.page-first{padding-top:clamp(40px,6vw,72px)!important}
.next-box{display:grid;grid-template-columns:1.4fr auto;gap:24px;align-items:center;background:var(--plum);color:#fff;border-radius:24px;padding:clamp(28px,5vw,56px)}
.next-box h2{font-size:clamp(1.8rem,3.6vw,2.6rem)}
.next-box p{color:#cfc4d4;margin-top:.6rem;max-width:52ch}
.next-btns{display:flex;flex-wrap:wrap;gap:10px}
.next-btns .btn-line{background:transparent;color:#fff;border:0;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.45)}
.next-btns .btn-line:hover{box-shadow:inset 0 0 0 1.5px #fff}
@media (max-width:760px){.next-box{grid-template-columns:1fr}}
</style>
</head>"""

# Jämförelsetabellen finns bara på /priser, knappen dit bara på startsidan
def only(text, keep):
    for tag in ("bara-hem", "bara-priser"):
        text, n = re.subn(r"[ \t]*<!-- %s\b.*?-->\n(.*?)[ \t]*<!-- /%s -->\n" % (tag, tag), (lambda m: m[1]) if tag == keep else "", text, flags=re.S)
        if n > 1: raise SystemExit("build-pages: dubbla märken " + tag)
    return text

main0, main1 = src.index('<main id="top"'), src.index("</main>")

for name, p in PAGES.items():
    url = f"https://sabimedia.se/{name}"
    body = only("".join(section(s) for s in p["parts"]), "bara-priser")
    if name == "tjanster":  # knapp under ingressen och exemplet direkt efter det som ingår
        body = re.sub(r'(<p class="lead">.*?</p>\n)', lambda m: m[1] + '        <div class="head-btns"><a class="btn btn-ink" href="#cookie-munch">Se exempel: Cookie Munch ↓</a></div>\n', body, count=1, flags=re.S)
        cut = body.index("</section>\n") + len("</section>\n")
        body = body[:cut] + cookie_munch() + body[cut:]
    body = re.sub(r'<section class="section([^"]*)" id="([^"]+)"( style="padding-top:0")?', r'<section class="section\1 page-first" id="\2"', body, count=1)
    body = re.sub(r'<span class="eyebrow">[^<]*</span>', f'<span class="eyebrow">{p["eyebrow"]}</span>', body, count=1)
    body = re.sub(r"<h2>(.*?)</h2>", r"<h1>\1</h1>", body, count=1, flags=re.S)
    # Osynlig mellanrubrik så att rubriknivåerna följer varandra (h1, h2, h3)
    for before, text in (('<div class="features">', "Det här ingår"), ('<div class="plans" id="plans">', "Paketen")):
        body = body.replace(before, f'<h2 class="only-sr">{text}</h2>\n      {before}', 1)
    page = src[:main0] + '<main id="top" tabindex="-1">\n' + body + p["after"] + src[main1:]

    page = re.sub(r"<title>.*?</title>", f'<title>{p["title"]}</title>', page, count=1)
    page = one(page, '<link rel="canonical" href="https://sabimedia.se/">', f'<link rel="canonical" href="{url}">')
    page = one(page, '<meta property="og:url" content="https://sabimedia.se/">', f'<meta property="og:url" content="{url}">')
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m[1] + p["desc"], page, count=1)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m[1] + p["desc"], page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1] + p["title"], page, count=1)
    data = {"@context": "https://schema.org", "@type": "ContactPage" if name == "kontakt" else "WebPage", "name": p["title"].split(" · ")[0], "url": url, "about": {"@id": "https://sabimedia.se/#foretag"}}
    if name == "faq":
        qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body, re.S)
        data.update({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qa]})
    page, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>", page, flags=re.S)
    if n != 1: raise SystemExit("build-pages: JSON-LD")

    page = one(page, '<li><a href="/" aria-current="page">Hem</a></li>', '<li><a href="/">Hem</a></li>')
    page, n = re.subn(r'(<li><a (?:class="[^"]*" )?href="/%s")' % name, r'\1 aria-current="page"', page, count=1)
    if n != 1: raise SystemExit("build-pages: menyn saknar /" + name)
    page = one(page, "</style>\n</head>", CSS)
    page = re.sub(r'href="#(ingar|priser|fragor|kontakt)"', lambda m: 'href="/%s"' % {"ingar": "tjanster", "priser": "priser", "fragor": "faq", "kontakt": "kontakt"}[m[1]], page)
    if 'class="hl"' not in body:
        page = re.sub(r'<link rel="preload" href="typsnitt/fraunces[^\n]*\n', "", page)
    open(f"site/{name}.html", "w", encoding="utf-8").write(page)

open("site/index.html", "w", encoding="utf-8").write(only(src, "bara-hem"))
