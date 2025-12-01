import subprocess
import json
from pathlib import Path
from core.utils import ensure_dir

class ToolInstaller:
    """Manages installation and discovery of security tools"""
    
    TOOLS_DB = {
        # Network scanning
        "nmap": {
            "package": "nmap",
            "apt": "nmap",
            "pip": None,
            "check": "nmap --version",
            "description": "Network mapping and scanning tool"
        },
        "masscan": {
            "package": "masscan",
            "apt": "masscan",
            "pip": None,
            "check": "masscan --version",
            "description": "Fast network scanner"
        },
        
        # Enumeration
        "gobuster": {
            "package": "gobuster",
            "apt": "gobuster",
            "pip": None,
            "check": "gobuster version",
            "description": "Directory/DNS/VHost enumeration tool"
        },
        "dirb": {
            "package": "dirb",
            "apt": "dirb",
            "pip": None,
            "check": "dirb",
            "description": "Web directory scanner"
        },
        "ffuf": {
            "package": "ffuf",
            "apt": "ffuf",
            "pip": None,
            "check": "ffuf -h",
            "description": "Fast web fuzzer"
        },
        
        # Web scanning
        "whatweb": {
            "package": "whatweb",
            "apt": "whatweb",
            "pip": None,
            "check": "whatweb --version",
            "description": "Web technology identifier"
        },
        "nikto": {
            "package": "nikto",
            "apt": "nikto",
            "pip": None,
            "check": "nikto -Version",
            "description": "Web server vulnerability scanner"
        },
        
        # Brute force
        "hydra": {
            "package": "hydra",
            "apt": "hydra",
            "pip": None,
            "check": "hydra -h",
            "description": "Network login brute force tool"
        },
        
        # Exploitation
        "sqlmap": {
            "package": "sqlmap",
            "apt": "sqlmap",
            "pip": None,
            "check": "sqlmap --version",
            "description": "SQL injection testing tool"
        },
        
        # SMB enumeration
        "smbmap": {
            "package": "smbmap",
            "apt": "smbmap",
            "pip": "smbmap",
            "check": "smbmap -h",
            "description": "SMB share enumeration"
        },
        
        # DNS enumeration
        "dnsrecon": {
            "package": "dnsrecon",
            "apt": "dnsrecon",
            "pip": "dnsrecon",
            "check": "dnsrecon -h",
            "description": "DNS enumeration tool"
        },
        
        # Passive reconnaissance
        "whois": {
            "package": "whois",
            "apt": "whois",
            "pip": None,
            "check": "whois --version",
            "description": "Domain WHOIS lookup"
        },
        "dig": {
            "package": "dnsutils",
            "apt": "dnsutils",
            "pip": None,
            "check": "dig -v",
            "description": "DNS lookup utility"
        },
    }

    def __init__(self, config_path="./reports/tools_installed.json"):
        self.config_path = Path(config_path)
        ensure_dir(self.config_path.parent)
        self._load_installed()

    def _load_installed(self):
        """Load list of installed tools"""
        try:
            self.installed = json.loads(self.config_path.read_text())
        except:
            self.installed = {}

    def _save_installed(self):
        """Save installed tools list"""
        self.config_path.write_text(json.dumps(self.installed, indent=2))

    def check_tool(self, toolname):
        """Check if a tool is installed and working"""
        if toolname not in self.TOOLS_DB:
            return False, "Unknown tool"
        
        tool = self.TOOLS_DB[toolname]
        try:
            result = subprocess.run(
                tool["check"],
                shell=True,
                capture_output=True,
                timeout=5
            )
            is_installed = result.returncode == 0
            if is_installed:
                self.installed[toolname] = {"installed": True, "version": "checked"}
                self._save_installed()
            return is_installed, "Tool working" if is_installed else "Tool not found"
        except subprocess.TimeoutExpired:
            return False, "Check timed out"
        except Exception as e:
            return False, str(e)

    def install_tool(self, toolname, method="apt"):
        """Install a tool using specified method"""
        if toolname not in self.TOOLS_DB:
            return False, f"Tool '{toolname}' not found in database"
        
        tool = self.TOOLS_DB[toolname]
        
        if method == "apt":
            if not tool.get("apt"):
                return False, "APT installation not available for this tool"
            return self._install_apt(toolname, tool["apt"])
        
        elif method == "pip":
            if not tool.get("pip"):
                return False, "PIP installation not available for this tool"
            return self._install_pip(toolname, tool["pip"])
        
        else:
            return False, "Unsupported installation method"

    def _install_apt(self, toolname, package):
        """Install tool via apt"""
        try:
            print(f"Installing {toolname} via apt...")
            result = subprocess.run(
                ["sudo", "apt", "install", "-y", package],
                capture_output=True,
                timeout=300
            )
            if result.returncode == 0:
                is_ok, msg = self.check_tool(toolname)
                if is_ok:
                    self.installed[toolname] = {"installed": True, "method": "apt"}
                    self._save_installed()
                    return True, f"✓ {toolname} installed successfully"
                else:
                    return False, f"Installation completed but verification failed: {msg}"
            else:
                error = result.stderr.decode('utf-8', errors='ignore')
                return False, f"Installation failed: {error[:200]}"
        except subprocess.TimeoutExpired:
            return False, "Installation timed out (>300s)"
        except Exception as e:
            return False, str(e)

    def _install_pip(self, toolname, package):
        """Install tool via pip"""
        try:
            print(f"Installing {toolname} via pip...")
            result = subprocess.run(
                ["pip3", "install", package],
                capture_output=True,
                timeout=300
            )
            if result.returncode == 0:
                is_ok, msg = self.check_tool(toolname)
                if is_ok:
                    self.installed[toolname] = {"installed": True, "method": "pip"}
                    self._save_installed()
                    return True, f"✓ {toolname} installed successfully"
                else:
                    return False, f"Installation completed but verification failed: {msg}"
            else:
                error = result.stderr.decode('utf-8', errors='ignore')
                return False, f"Installation failed: {error[:200]}"
        except subprocess.TimeoutExpired:
            return False, "Installation timed out (>300s)"
        except Exception as e:
            return False, str(e)

    def get_installed_tools(self):
        """Return list of installed tools"""
        installed = []
        for toolname in self.TOOLS_DB.keys():
            is_ok, _ = self.check_tool(toolname)
            if is_ok:
                installed.append(toolname)
        return installed

    def get_available_tools(self):
        """Return all available tools with descriptions"""
        return {
            name: tool["description"] 
            for name, tool in self.TOOLS_DB.items()
        }

    def get_tool_info(self, toolname):
        """Get detailed info about a tool"""
        if toolname not in self.TOOLS_DB:
            return None
        
        tool = self.TOOLS_DB[toolname]
        is_installed, status = self.check_tool(toolname)
        
        return {
            "name": toolname,
            "description": tool["description"],
            "installed": is_installed,
            "status": status,
            "install_methods": [m for m in ["apt", "pip"] if tool.get(m)],
            "check_command": tool["check"]
        }

    def install_missing_tools(self):
        """Try to install all missing tools (requires sudo)"""
        results = {}
        for toolname in self.TOOLS_DB.keys():
            is_installed, _ = self.check_tool(toolname)
            if not is_installed:
                tool = self.TOOLS_DB[toolname]
                if tool.get("apt"):
                    success, msg = self.install_tool(toolname, "apt")
                    results[toolname] = (success, msg)
        return results
