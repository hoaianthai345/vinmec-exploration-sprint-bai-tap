#!/usr/bin/env bash
# Xuất slides/slides.html thành slides.pdf ở gốc repo bằng Chrome headless.
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --allow-file-access-from-files \
  --print-to-pdf="$PWD/slides.pdf" "file://$PWD/slides/slides.html" 2>/dev/null
echo "Đã xuất slides.pdf"
