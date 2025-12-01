#!/bin/bash

echo "=============================================="
echo "        SecShell PRO — Auto Installer         "
echo "=============================================="
echo

# --- Check Python ---
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 not found! Install Python 3 first."
    exit 1
fi

# --- Check pip ---
if ! command -v pip3 >/dev/null 2>&1; then
    echo "[ERROR] pip3 not found! Installing..."
    sudo apt update
    sudo apt install -y python3-pip
fi

echo "[OK] Python & Pip detected."

# --- Install Dependencies (SYSTEM-WIDE, NO VENV) ---
echo
echo "Installing project dependencies (NO venv)..."
pip3 install --upgrade pip

pip3 install \
    prompt_toolkit \
    PyYAML \
    rich \
    requests \
    tqdm \
    python-dotenv \
    defusedxml \
    beautifulsoup4 \
    lxml \
    fuzzywuzzy \
    python-Levenshtein \
    thefuzz \
    openai

echo "[OK] Python dependencies installed."

# --- Install Kali pentesting tools (if missing) ---
echo
echo "Installing necessary pentest tools..."
sudo apt update
sudo apt install -y nmap gobuster whatweb hydra whois zip jq

echo "[OK] Pentesting tools installed."

# --- Create reports folder if missing ---
if [ ! -d "reports" ]; then
    mkdir -p reports
    echo "[OK] Created reports/ directory."
fi

# --- Validate project structure ---
if [ ! -d "core" ]; then
    echo "[ERROR] No 'core/' folder found. Run script from project root."
    exit 1
fi

# --- Run SecShell PRO ---
echo
echo "=============================================="
echo "   Launching SecShell PRO (dry-run enabled)   "
echo "=============================================="
echo

python3 -m core.main

