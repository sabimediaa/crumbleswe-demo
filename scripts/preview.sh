#!/usr/bin/env bash
# Förhandsvisar bara Sabimedia lokalt på http://localhost:8765, precis som på sabimedia.se.
# Bygger site/ först, så andra demos i mappen aldrig kommer med.
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/build-site.sh
exec firebase emulators:start --only hosting --project demo-sabimedia
