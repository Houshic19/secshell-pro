# Makefile for SecShell PRO - one-command setup & run

.PHONY: help all setup-venv install-deps install-tools run test install-desktop clean

help:
	@echo "SecShell PRO Makefile - available targets:"
	@echo "  make setup-venv     - create Python venv at .venv"
	@echo "  make install-deps   - install Python dependencies into .venv"
	@echo "  make install-tools  - install system pentest tools (requires sudo)"
	@echo "  make run            - run SecShell PRO using .venv Python"
	@echo "  make test           - run automated test script"
	@echo "  make install-desktop- create a desktop shortcut on ~/Desktop (optional)"
	@echo "  make all            - setup-venv + install-deps"

all: setup-venv install-deps

setup-venv:
	@if [ -d .venv ]; then \
		echo "Using existing .venv"; \
	else \
		python3 -m venv .venv && echo "Created .venv"; \
	fi
	.venv/bin/python3 -m pip install --upgrade pip

install-deps: setup-venv
	@echo "Installing Python dependencies into .venv (uses requirements.txt)"
	.venv/bin/pip install -r requirements.txt

install-tools:
	@echo "This will try to install common pentest tools via apt. Requires sudo and network."
	@read -p "Continue and run sudo apt update/install? [y/N] " yn; \
	if [ "$$yn" = "y" ] || [ "$$yn" = "Y" ]; then \
		sudo apt update && sudo apt install -y nmap gobuster whatweb hydra whois jq zip; \
		echo "System tools installation attempted."; \
	else \
		echo "Aborted install-tools"; \
	fi

run: setup-venv
	@echo "Starting SecShell PRO... (use Ctrl-C to exit)"
	.venv/bin/python3 core/main.py

test: setup-venv
	@bash test_intelligent.sh

install-desktop:
	@echo "This will create a desktop launcher: ~/Desktop/SecShellPRO.desktop"
	@read -p "Create desktop shortcut? [y/N] " yn; \
	if [ "$$yn" = "y" ] || [ "$$yn" = "Y" ]; then \
		LAUNCHER=\"$$HOME/Desktop/SecShellPRO.desktop\"; \
		echo "[Desktop Entry]" > $$LAUNCHER; \
		echo "Type=Application" >> $$LAUNCHER; \
		echo "Name=SecShell PRO" >> $$LAUNCHER; \
		echo "Exec=$(pwd)/start_secshell.sh" >> $$LAUNCHER; \
		echo "Terminal=true" >> $$LAUNCHER; \
		chmod +x $$LAUNCHER; \
		echo "Created $$LAUNCHER"; \
	else \
		echo "Aborted desktop install"; \
	fi

clean:
	rm -rf .venv
	@echo "Removed .venv (if existed)"
