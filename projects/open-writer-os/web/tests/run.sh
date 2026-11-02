#!/bin/sh
# Offline test suite for the Open Writer OS 2.0 web app.
# Needs Python 3 and (for the JS core tests) Node 18+.
set -e
cd "$(dirname "$0")/.."
python3 build.py
if command -v node >/dev/null 2>&1; then
  node tests/tests.js
else
  echo "node not found; skipping JS core tests (run: node web/tests/tests.js)"
fi
cd ../..
python3 -m unittest discover -s tests -v
