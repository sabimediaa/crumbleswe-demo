"""Publicerar klickbara demosidor med påhittade företag (exempel-*.html) under /demo-*.
Typsnitt från Google Fonts tas bort och ersätts med sajtens egna, så att inget hämtas från någon annan
(som integritetspolicyn lovar). Sidorna får noindex och en tydlig demo-list. Körs av build-site.sh."""
import re, shutil

DEMOS = {  # källfil: (publicerad adress, bilder som sidan använder)
    "exempel-restaurang.html": ("demo-restaurang", ["bistro-ruta.webp"]),
    "exempel-foretag.html": ("demo-bageri", []),
}

FONTS = """<style>
/* Sajtens egna typsnitt i stället för Google Fonts */
@font-face{font-family:"Inter";src:url(/typsnitt/inter.woff2) format("woff2");font-weight:400 700;font-display:swap}
@font-face{font-family:"Outfit";src:url(/typsnitt/inter.woff2) format("woff2");font-weight:400 700;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/typsnitt/fraunces-kursiv.woff2) format("woff2");font-style:italic;font-weight:400 700;font-display:swap}
.sabi-demo-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:9999;display:flex;gap:12px;align-items:center;
  background:#1b1620;color:#fff;font:600 14px/1.3 "Inter",system-ui,sans-serif;padding:10px 12px 10px 16px;border-radius:999px;
  box-shadow:0 12px 30px -10px rgba(0,0,0,.5);max-width:calc(100vw - 32px)}
.sabi-demo-bar a{color:#fff;background:#d42c33;border-radius:999px;padding:7px 12px;text-decoration:none;white-space:nowrap}
</style>
"""

for src, (slug, images) in DEMOS.items():
    page = open(src, encoding="utf-8").read()
    page, n = re.subn(r'\s*<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>', "", page)
    if n == 0: raise SystemExit("build-demos: hittade inga Google Fonts-länkar i " + src)
    if "googleapis" in page or "gstatic" in page: raise SystemExit("build-demos: Google-adresser kvar i " + src)
    head = '<meta name="robots" content="noindex">\n' + FONTS
    bar = '<div class="sabi-demo-bar">Demo med påhittat företag <a href="/">Till Sabimedia</a></div>\n'
    # Alla källfiler har inte </head> och </body> (taggarna är frivilliga i HTML), så sätt in efter <meta charset> och sist i filen då
    if "</head>" in page: page = page.replace("</head>", head + "</head>", 1)
    else: page = re.sub(r'<meta charset[^>]*>\s*', lambda m: m.group(0) + head, page, count=1)
    if "</body>" in page: page = page.replace("</body>", bar + "</body>", 1)
    else: page = page.rstrip() + "\n" + bar
    if 'content="noindex"' not in page or "sabi-demo-bar\">" not in page:
        raise SystemExit("build-demos: kunde inte lägga in noindex och demo-list i " + src)
    page = re.sub(r'(src|href)="bilder/', r'\1="/bilder/', page)
    open(f"site/{slug}.html", "w", encoding="utf-8").write(page)
    for img in images:
        shutil.copy(f"bilder/{img}", f"site/bilder/{img}")
print("build-demos:", ", ".join(s for s, _ in DEMOS.values()))
