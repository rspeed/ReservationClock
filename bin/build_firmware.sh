#!/bin/sh

# Builds Micropython for the Raspberry Pi Pico W with frozen dependencies.

#TODO: Add arguments to change the port, board, etc.
PORT="rp2"
BOARD="RPI_PICO_W"

SCRIPT_PATH=$(realpath "${0}")
cd "$(dirname "${SCRIPT_PATH}")"

# Normalize paths (as needed)
MANIFEST_PATH=$(realpath "../manifest.py")
printf -v MANIFEST_PATH "%q" "${MANIFEST_PATH}"  # This needs to have escaped characters *and* be encased in double-quotes
PORT_DIR="ports/${PORT}"
BUILD_DIR="${PORT_DIR}/build-${BOARD}"

cd "../../micropython"

make -j2 -C "${PORT_DIR}" clean BOARD="${BOARD}"
make -j2 -C "${PORT_DIR}" submodules
make -j2 -C "${PORT_DIR}" BOARD="${BOARD}" FROZEN_MANIFEST="${MANIFEST_PATH}"
