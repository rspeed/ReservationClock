#!/bin/sh

# Builds Micropython for the Raspberry Pi Pico W with frozen dependencies.

#TODO: Add arguments to change the port, board, etc.

SCRIPT_PATH=`realpath "${0}"`
SCRIPT_DIR=`dirname "${SCRIPT_PATH}"`

cd "${SCRIPT_DIR}"

PORT="rp2"
BOARD="RPI_PICO_W"
FROZEN_MANIFEST=`realpath "../manifest.py"`
MICROPYTHON_DIR=`realpath "../../micropython"`
printf -v FROZEN_MANIFEST "%q" "${FROZEN_MANIFEST}"

cd "${MICROPYTHON_DIR}"

echo "${FROZEN_MANIFEST}"

make -j2 -C "ports/${PORT}" clean BOARD="${BOARD}"
make -j2 -C "ports/${PORT}" submodules
make -j2 -C "ports/${PORT}" BOARD="${BOARD}" FROZEN_MANIFEST="${FROZEN_MANIFEST}"
