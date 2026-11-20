#!/bin/sh
# Compila (e opcionalmente grava) o firmware das placas com o arduino-cli.
#
# O arduino-cli so compila os arquivos da pasta do sketch, entao este script monta uma pasta plana
# (build/sketch) juntando app/, hal/ e core/. A pasta build/ nao vai para o git.
#
# Uso:
#   tools/build.sh                         compila
#   tools/build.sh upload /dev/ttyACM0     compila e grava na porta indicada
#   CORE_DIR=/outro/core tools/build.sh    usa outro core (so para teste local)
set -eu
cd "$(dirname "$0")/.."

FQBN="esp32:esp32:esp32c6:CDCOnBoot=cdc"
CORE_DIR="${CORE_DIR:-core}"

rm -rf build/sketch
mkdir -p build/sketch
cp app/app.ino build/sketch/sketch.ino
cp app/config.h build/sketch/
cp hal/*.h hal/*.c hal/*.cpp build/sketch/
cp "$CORE_DIR"/*.h "$CORE_DIR"/*.c build/sketch/

arduino-cli compile --fqbn "$FQBN" --output-dir build/out build/sketch

if [ "${1:-}" = "upload" ]; then
    arduino-cli upload --fqbn "$FQBN" -p "${2:?informe a porta, ex.: /dev/ttyACM0}" --input-dir build/out build/sketch
fi
