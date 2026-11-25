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

WEBBDESIGN = '''  <section class="section" id="webbdesign" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Webbdesign och webbutveckling</span>
        <h2>Webbdesign för företag, <em class="hl">från början till slut.</em></h2>
        <p class="lead">Att skapa hemsida för företag på egen hand tar tid. Vi tar hand om både hur den ser ut och hur den fungerar, så att du kan fokusera på dina kunder.</p>
      </div>
      <div class="own">
        <div class="own-card"><h3>Webbdesign</h3><p>Som webbdesignbyrå formar vi hemsidan efter ditt varumärke, med dina färger, din logga och dina bilder. Den ska vara lätt att förstå och se bra ut i mobil, surfplatta och dator.</p></div>
        <div class="own-card"><h3>Webbutveckling</h3><p>Vi bygger funktionerna du behöver, till exempel formulär, bokningar, beställningar och betalning. Vad som ingår beror på vilket paket du väljer.</p></div>
        <div class="own-card"><h3>Bygga hemsida utan krångel</h3><p>Du berättar vad du behöver och skickar ditt material. Vi bygger, du säger vad du tycker, och inget publiceras innan du är nöjd.</p></div>
        <div class="own-card"><h3>Ta emot beställningar online</h3><p>Med Business får du en hemsida med beställningsformulär, och alla onlinebeställningar kommer direkt till din mejl.</p></div>
        <div class="own-card"><h3>Skapa företagshemsida</h3><p>Har du ingen egen hemsida än? Vi börjar med ett möte om dina behov, din målgrupp och din stil. Sedan får du ett första utkast att tycka till om.</p></div>
        <div class="own-card"><h3>Förbättra hemsida</h3><p>Känns din hemsida gammal, eller hör för få kunder av sig? <a href="/kontakt">Skicka länken till oss</a> så föreslår vi vad som kan bli bättre, eller om det är dags för en ny hemsida.</p></div>
        <div class="own-card"><h3>Öppna webbutik</h3><p>Vill du ha en hemsida med produkter som kunden kan köpa direkt? Med Custom bygger vi en webbutik med varukorg, betalning och en egen adminpanel.</p></div>
        <div class="own-card"><h3>Ta emot bokningar online</h3><p>Låt kunden skicka en bokningsförfrågan på hemsidan. Med Custom kan du få ett bokningssystem med kalender och lediga tider.</p></div>
      </div>
    </div>
  </section>
'''

PRISFRAGOR = '''  <section class="section" id="vad-kostar" style="padding-top:0">
    <div class="wrap faq-grid">
      <div class="section-head" style="margin:0">
        <span class="eyebrow">Webbyrå · Priser</span>
        <h2>Vad kostar en hemsida <em class="hl">till företag?</em></h2>
        <p class="lead">Vi är en webbyrå med fast pris. Hos oss kostar en hemsida från 1&nbsp;200&nbsp;kr med Start, från 2&nbsp;500&nbsp;kr med Business och från 4&nbsp;000&nbsp;kr med Custom. Priset är en engångskostnad exklusive moms.</p>
      </div>
      <div class="faq">
        <details open><summary>Får jag en hemsida till fast pris?</summary><p>Ja. Priserna ovan är från-priser, men innan vi börjar får du ett fast pris att godkänna. Då vet du vad din hemsida kostar.</p></details>
        <details><summary>Kan jag köpa en hemsida utan abonnemang?</summary><p>Ja, hos oss får du en hemsida utan abonnemang. Du betalar en engångskostnad, inga månadsavgifter till oss, och du äger hemsidan själv.</p></details>
        <details><summary>Vilken kostnad har en hemsida efter lansering?</summary><p>Domän och webbhotell är löpande, och dem betalar du direkt till leverantören. Behöver du hjälp efter supportperioden tar vi betalt per timme.</p></details>
        <details><summary>Är en billig hemsida för småföretag bra nog?</summary><p>Det kan den vara. Med Start får du en billig hemsida med egen design, mobilanpassning och kontaktformulär. Vill du ha en hemsida billigt till att börja med kan du lägga till funktioner senare mot offert.</p></details>
        <details><summary>Hemsida för småföretag: vilket pris och paket passar?</summary><p>Start räcker långt om du vill synas och bli kontaktad. Business passar dig som tar emot förfrågningar, bokningar eller beställningar. Custom är för dig som behöver till exempel webbshop eller bokningssystem. Alla våra paket för en ny hemsida är gjorda för småföretag, och du ser priset innan du bestämmer dig.</p></details>
        <details><summary>Hur jämför jag priser hos olika webbyråer?</summary><p>När du jämför pris på hemsida bör du titta på vad som ingår, om det tillkommer månadsavgifter och vem som äger hemsidan. <a href="#jamfor">Här ser du vad som ingår hos oss.</a></p></details>
      </div>
    </div>
  </section>
'''

PAGES = {
    "tjanster": dict(
        menu="Tjänster", title="Skapa hemsida för företag – webbdesign · Sabimedia",
        desc="Vill du skapa hemsida för företag? Vi jobbar med webbdesign och webbutveckling och bygger funktioner som förenklar vardagen. Se vad som ingår.",
        eyebrow="Tjänster · Skapa hemsida för företag", parts=["ingar", "sa-funkar-det", "agande"],
        after=next_step("Vad kostar det?", "Tre paket med fast pris. Jämför dem eller fråga oss vad som passar dig.",
                        [("btn-accent", "/priser", "Se priserna →"), ("btn-line", "/kontakt", "Kontakta oss")])),
    "priser": dict(
        menu="Priser", title="Billig hemsida till fast pris – priser och paket · Sabimedia",
        desc="Billig hemsida från 1 200 kr exkl. moms. Se vad en hemsida kostar och jämför tre paket med fast engångspris, utan månadsavgift till Sabimedia.",
        eyebrow="Priser · Billig hemsida", parts=["priser"],
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
#webbdesign .own{grid-template-columns:repeat(4,1fr)}
@media (max-width:1100px){#webbdesign .own{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){#webbdesign .own{grid-template-columns:1fr}}
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
        body = body[:cut] + cookie_munch() + WEBBDESIGN + body[cut:]
        body = one(body, "Vi jobbar med webbdesign i Borås och i hela Sverige. Varje hemsida är byggd för små företag som", "Vi bygger hemsidor med funktioner som förenklar företagets vardag. Vårt jobb är webbdesign och webbutveckling för små företag som")
        body = one(body, "ett proffsigare sätt att ta emot beställningar.", "ett proffsigare sätt att ta emot beställningar online.")
    if name == "priser":
        body = one(body, "Vill du köpa hemsida till ditt företag? Sabi media är en webbyrå med fast pris och tydligt innehåll. Välj den hemsida som passar hur ditt företag tar emot kunder.", "Att köpa hemsida ska vara enkelt. Du får en billig hemsida till fast engångspris, utan abonnemang och utan månadsavgift till Sabimedia. Välj det paket som passar hur ditt företag tar emot kunder.") + PRISFRAGOR
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
