#!/bin/bash
set -e

echo "== Έλεγχος εξαρτήσεων Docker =="
if ! command -v docker >/dev/null; then
  echo "⚠️  Εγκατέστησε πρώτα το Docker." && exit 1
fi
if ! command -v docker-compose >/dev/null; then
  echo "⚠️  Εγκατέστησε docker-compose." && exit 1
fi

echo "== Δημιουργία φακέλων =="
mkdir -p core voice gui

echo "== Εκκίνηση Ζένιας =="
docker-compose up -d --build
echo "== Το σύστημα Ζένια είναι έτοιμο στο http://localhost:8000 =="
