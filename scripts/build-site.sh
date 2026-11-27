#!/usr/bin/env bash
# Bygger mappen site/ med bara det som ska publiceras på Sabimedias domän.
# Körs automatiskt före "firebase deploy" (se predeploy i firebase.json).
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf site
mkdir -p site/bilder site/typsnitt

cp sabimedia.html site/index.html
cp integritetspolicy.html site/integritetspolicy.html
cp villkor.html site/villkor.html
cp om-oss.html site/om-oss.html
cp branscher.html site/branscher.html
cp boka.html site/boka.html
cp kundcase-cookie-munch.html site/kundcase-cookie-munch.html
cp favicon.ico robots.txt sitemap.xml sok.js site/
cp bilder/sabi-logo.png bilder/cookiemunch-desktop.jpg bilder/cookiemunch-mobil.jpg bilder/cookiemunch-logo.webp \
   bilder/exempel-kladbutik.jpg bilder/exempel-restaurang.jpg bilder/exempel-stad.jpg bilder/safiya.jpg \
   bilder/favicon-32.png bilder/favicon-96.png bilder/favicon-192.png bilder/apple-touch-icon.png bilder/ikon-512.png bilder/delningsbild.jpg site/bilder/
# Mindre WebP-storlekar som används via srcset
cp bilder/{sabi-logo,cookiemunch-desktop,cookiemunch-mobil,cookiemunch-logo,exempel-kladbutik,exempel-restaurang,exempel-stad,safiya}-[0-9]*.webp site/bilder/

cp typsnitt/*.woff2 site/typsnitt/

# Undersidorna Tjänster, Priser, FAQ och Kontakt samt sidorna i sidor/ skapas från startsidan
python3 scripts/build-pages.py

# Klickbara demosidor med påhittade företag
python3 scripts/build-demos.py

# Paketen och prisjämförelsen läggs direkt i HTML-koden så att sökmotorer ser dem utan JavaScript
node scripts/prerender-priser.js

# Bilder och typsnitt cachas i ett år (firebase.json). Därför får varje adress en kod som
# räknas fram ur filens innehåll: byts filen ut får den ny adress och hämtas på nytt.
python3 - <<'PY'
import glob, hashlib, re, sys
def add(m):
    path = m.group(1)
    try:
        with open("site/" + path.lstrip("/"), "rb") as f: code = hashlib.md5(f.read()).hexdigest()[:8]
    except FileNotFoundError:
        sys.exit("Filen saknas i site/: " + path)
    return f"{path}?v={code}"
for page in glob.glob("site/*.html"):
    with open(page, encoding="utf-8") as f: html = f.read()
    html = re.sub(r"(?<![\w/.-])(/?(?:bilder|typsnitt)/[\w.-]+\.(?:jpg|png|webp|woff2))(?:\?v=\w+)?", add, html)
    with open(page, "w", encoding="utf-8") as f: f.write(html)
PY

echo "site/ klar: $(find site -type f | wc -l | tr -d ' ') filer"
