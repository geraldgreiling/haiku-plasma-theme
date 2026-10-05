#!/usr/bin/env bash
# Ersetzt den Platzhalter GITHUB_USER in allen Dateien durch deinen GitHub-Namen.
#   tools/set_github_user.sh meinname
set -euo pipefail
[ $# -eq 1 ] || { echo "Aufruf: $0 <github-benutzername>"; exit 1; }
cd "$(dirname "$0")/.."
grep -rlI --exclude-dir=build --exclude-dir=dist --exclude-dir=.git GITHUB_USER . | grep -v "tools/set_github_user.sh" |
    while read -r f; do sed -i "s/GITHUB_USER/$1/g" "$f"; echo "geändert: $f"; done
