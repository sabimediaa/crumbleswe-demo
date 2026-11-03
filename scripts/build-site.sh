#!/usr/bin/env bash
# Bygger mappen site/ med bara det som ska publiceras på Sabimedias domän.
# Körs automatiskt före "firebase deploy" (se predeploy i firebase.json).
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf site
mkdir -p site/bilder

cp sabimedia.html site/index.html
cp integritetspolicy.html site/integritetspolicy.html
cp om-oss.html site/om-oss.html
cp boka.html site/boka.html
cp kundcase-cookie-munch.html site/kundcase-cookie-munch.html
cp favicon.ico robots.txt sitemap.xml site/
cp bilder/sabi-logo.png bilder/cookiemunch-desktop.jpg bilder/cookiemunch-mobil.jpg bilder/cookiemunch-logo.webp \
   bilder/exempel-kladbutik.jpg bilder/exempel-foodtruck.jpg bilder/exempel-frisor.jpg bilder/safiya.jpg \
   bilder/favicon-32.png bilder/apple-touch-icon.png bilder/ikon-512.png bilder/delningsbild.jpg site/bilder/

echo "site/ klar: $(find site -type f | wc -l | tr -d ' ') filer"
