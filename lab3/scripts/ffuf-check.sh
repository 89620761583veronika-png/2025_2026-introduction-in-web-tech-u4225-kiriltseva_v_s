#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
FFUF=${FFUF:-ffuf}
"$FFUF" -V > logs/ffuf-version.txt
for list in common files; do
  "$FFUF" -w "security/wordlists/$list.txt" -u http://127.0.0.1:8083/FUZZ -mc 200,301,302,403 -t 2 -rate 5 -timeout 5 -noninteractive -of json -o "logs/ffuf-$list.json" > "logs/ffuf-$list.txt" 2>&1
done
