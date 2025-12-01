#!/usr/bin/env bash
# Launcher that ensures virtualenv is active then runs SecShell PRO
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1

# Ensure venv exists
if [ ! -d ".venv" ]; then
    echo "Virtualenv not found. Creating .venv and installing dependencies..."
    python3 -m venv .venv || { echo "Failed to create venv"; exit 1; }
    .venv/bin/python3 -m pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }
fi

# Run using venv Python
.venv/bin/python3 core/main.py
