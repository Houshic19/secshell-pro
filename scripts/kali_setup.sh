#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3-pip python3-venv nmap gobuster whatweb hydra exiftool clamav whois zip
python3 -m pip install -r requirements.txt
echo "SecShell PRO dependencies installed. Create venv for isolation if desired."
