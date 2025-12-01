# SecShell PRO - Complete Master Guide

**Intelligent Security Automation Platform**

A comprehensive security tool orchestration framework with intelligent learning, real CTF assistance, and professional report generation.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Features](#core-features)
3. [CTF Mode Guide](#ctf-mode-guide)
4. [Available Commands](#available-commands)
5. [Security Shortcuts](#security-shortcuts)
6. [Report Generation](#report-generation)
7. [Learning System](#learning-system)
8. [Plugin System](#plugin-system)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation & Launch (One Command)

```bash
cd /home/kali/Desktop/secshell-pro
make run
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 core/main.py
```

### First Time Running SecShell

```
SecShell> help                  # See all available commands
SecShell> enum-full target=site.com  # Try a security shortcut
SecShell> ctf list             # See CTF patterns
SecShell> stats                # Check learning progress
```

---

## Core Features

### 🤖 Adaptive Learning System
- **Skill Level Tracking**: Automatic progression from Beginner → Expert
- **Pattern Recognition**: AI learns your workflow and suggests next steps
- **History Tracking**: Complete audit trail of all executed commands
- **Smart Recommendations**: Context-aware suggestions based on usage

### 🛡️ Security Automation
- **15+ Pre-built Shortcuts**: Common pentesting workflows
- **YAML Customization**: Create custom shortcuts and commands
- **13+ Tool Management**: Automatic installation and verification
- **Safety Features**: Force flags required for dangerous operations

### 📊 Professional Reports
- **PDF Generation**: Professional security assessment reports
- **Structured Findings**: Organized vulnerability documentation
- **Metadata Tracking**: Timeline, targets, scope information
- **Export Options**: JSON and text formats available

### 🚩 CTF Mode (Real Assistance Tool)
- **Auto Flag Extraction**: Automatic detection from command output
- **Custom Patterns**: Add competition-specific extraction rules
- **Flag Tracking**: Organize, validate, and manage captured flags
- **Submission Status**: Track which flags you've submitted
- **Statistics & Export**: Monitor progress and export results

### 🔌 Plugin System
- **Custom Tools**: Load custom Python plugins
- **Extensions**: Extend functionality without core modifications
- **Plugin Manager**: Automatic plugin discovery and loading

---

## CTF Mode Guide

### Quick Reference

```bash
ctf list                              # Show available patterns
ctf extract "<output>"               # Auto-extract flags
ctf capture "<flag>"                 # Save a flag manually
ctf flags                            # List all captured flags
ctf mark <id>                        # Mark flag as submitted
ctf stats                            # Show statistics
ctf export                           # Export flags
ctf add-pattern id=X regex=Y        # Add custom pattern
```

### Built-in Extraction Patterns

| Pattern | Format | Example |
|---------|--------|---------|
| standard_flag | flag{...} | flag{found_it} |
| ctf_format | CTF{...} | CTF{exploit_success} |
| hex_flag | 32+ hex chars | a1b2c3d4e5f6... |
| md5 | 32 hex chars | 5d41402abc4b2a76b9719d911017c592 |
| sha1 | 40 hex chars | 356a192b7913b04c54574d18c28d46e6395428ab |
| base64 | 20+ base64 chars | Zm9vYmFyYmF6cXV4... |

### Typical Competition Workflow

```bash
# Before competition
SecShell> ctf add-pattern id=myctf regex="FLAG\{[^}]+\}"
SecShell> ctf list  # Verify patterns

# During competition
SecShell> enum-full target=vulnerable.site
# [output with scan results]

# Extract flags automatically
SecShell> ctf extract "[paste_scan_output]" challenge="enum"
# [System shows matches and asks to capture]
# Capture these flags? (y/n): y

# Manual capture
SecShell> ctf capture "found_flag" challenge="web_app"

# Track progress
SecShell> ctf flags              # View all
SecShell> ctf stats              # Show statistics
SecShell> ctf mark 1             # Mark as submitted

# Export results
SecShell> ctf export format=txt  # Export to text
```

### Flag Capture Examples

```bash
# Minimal capture
ctf capture "flag{example}"

# With metadata
ctf capture "flag{web_rce}" challenge="web_app" category="web"

# Hash capture
ctf capture "5d41402abc4b2a76b9719d911017c592" challenge="crypto" category="hash"

# Base64 capture
ctf capture "Zm9vYmFyYmF6" challenge="encoding" category="encoding"
```

---

## Available Commands

### Core Commands

```bash
help                    # Show all available commands
status                  # Display current status and statistics
exit / quit             # Exit SecShell
clear                   # Clear screen
history [limit]         # Show command history
stats                   # Show learning statistics
```

### CTF Assistance Commands

```bash
ctf list                              # List patterns
ctf extract "<text>" [challenge=X]    # Extract flags
ctf capture "<flag>" [challenge=X]    # Save flag
ctf flags [submitted=true|false]      # List flags
ctf mark <id>                         # Mark submitted
ctf stats                             # Statistics
ctf export [format=json|txt]          # Export flags
ctf add-pattern id=X regex=Y          # Custom pattern
```

### Report Generation

```bash
report generate [output=filename]     # Generate PDF report
report list                           # Show recent reports
report view <filename>                # Display report
```

### Tool Management

```bash
tools install <tool_name>            # Install security tool
tools list                           # Show installed tools
tools verify                         # Check tool status
tools update                         # Update all tools
```

### Learning & History

```bash
learn show                           # Show learning database
learn clear                          # Clear learning data
history [limit]                      # Show command history
```

---

## Security Shortcuts

### Quick Reconnaissance

```bash
enum-full target=domain.com              # Full enumeration
port-scan target=192.168.1.1             # Port scanning
web-scan target=site.com                 # Web scanning
osint-domain domain=target.com           # OSINT on domain
```

### Custom Shortcuts

Define in `shortcuts/custom.yaml`:

```yaml
my-scan:
  description: "My custom scanning workflow"
  commands:
    - enum-full target=$1
    - port-scan target=$2
  help: "Usage: my-scan <domain> <ip>"
```

Use it:
```bash
my-scan example.com 192.168.1.1
```

---

## Report Generation

### Generate a Report

```bash
SecShell> enum-full target=vulnerable.site
# [scanning happens]

SecShell> report generate output=pentest_report
# [✓] Report generated: reports/pentest_report.pdf
```

### Report Contents

- Executive summary
- Vulnerabilities discovered
- Severity breakdown (Critical, High, Medium, Low)
- Recommendations
- Timeline of activities
- Target information

### Access Reports

```bash
SecShell> report list        # See all reports
SecShell> report view <name> # Open in PDF viewer
```

---

## Learning System

### Automatic Learning

SecShell tracks:
- ✓ Commands executed
- ✓ Tools used
- ✓ Success/failure patterns
- ✓ Skill progression
- ✓ Time spent on tasks

### Skill Levels

| Level | Experience | Unlocks |
|-------|------------|---------|
| Beginner | 0-50 commands | Basic shortcuts |
| Intermediate | 50-200 commands | Advanced shortcuts, custom patterns |
| Advanced | 200-500 commands | Expert tools, automation |
| Expert | 500+ commands | Full system access, custom plugins |

### View Progress

```bash
SecShell> stats                # Show learning stats
SecShell> learn show           # View learning database
SecShell> history 20           # Last 20 commands
```

---

## Plugin System

### Create Custom Plugin

File: `plugins/my_plugin.py`

```python
class MyPlugin:
    name = "My Custom Tool"
    version = "1.0"
    
    def execute(self, args):
        print(f"Plugin executed with args: {args}")
        return True
```

### Load Plugin

```bash
SecShell> plugin load my_plugin
# [✓] Plugin loaded: My Custom Tool
```

### List Plugins

```bash
SecShell> plugin list
```

---

## CTF Mode Statistics

### View Statistics

```bash
SecShell> ctf stats

Output:
  Total Flags Captured: 12
    ✓ Submitted: 8
    ⏳ Pending: 4
  
  Flags by Category:
    • web: 4
    • crypto: 3
    • hash: 2
    • standard: 3
```

### Export Flags

```bash
# JSON export
ctf export format=json
# → reports/flags_export_TIMESTAMP.json

# Text export
ctf export format=txt
# → reports/flags_export_TIMESTAMP.txt
```

---

## Troubleshooting

### Issue: SecShell won't start

```bash
# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Tools not installing

```bash
# Check permissions
sudo apt update
sudo apt install -y <tool_name>

# Verify installation
tools verify
```

### Issue: Lost command history/learning data

```bash
# Backup before clearing
SecShell> history > my_history.txt
SecShell> learn show > my_learning.txt

# Data is in reports/learner_db.json
```

### Issue: CTF flags not extracting

```bash
# Check patterns
ctf list

# Add custom pattern
ctf add-pattern id=debug regex="YOUR_PATTERN"

# Test manually
ctf capture "your_flag"
```

---

## Configuration Files

### Main Config: `configs/config.yaml`

```yaml
system:
  debug: false
  log_level: INFO

tools:
  auto_install: true
  verify_on_startup: true

learning:
  enabled: true
  persistence: true

ctf:
  auto_save: true
  validation_strict: true
```

### Shortcuts: `shortcuts/*.yaml`

```yaml
shortcut_name:
  description: "What it does"
  commands:
    - "command1 args"
    - "command2 args"
  help: "Usage information"
```

---

## Database Files

All data is stored in `reports/`:

```
reports/
├── ctf_data.json              # Captured flags
├── ctf_patterns.json          # Extraction patterns
├── learner_db.json            # Learning statistics
├── tools_installed.json       # Tool inventory
└── report_*.pdf               # Generated reports
```

---

## Tips & Best Practices

### CTF Competition

1. **Setup Patterns Early**: Add custom patterns before competition
2. **Extract First**: Use auto-extraction on all output
3. **Mark Submitted**: Keep status in sync with competition
4. **Export Regularly**: Backup your captures
5. **Check Stats**: Monitor progress with `ctf stats`

### Security Scanning

1. **Start with OSINT**: `osint-domain target=site.com`
2. **Enumerate**: `enum-full target=site.com`
3. **Scan Ports**: `port-scan target=ip.address`
4. **Scan Web**: `web-scan target=site.com`
5. **Generate Report**: `report generate output=pentest`

### Learning System

1. **Build Muscle Memory**: Use same shortcuts repeatedly
2. **Try Different Tools**: Expand your skill set
3. **Check Stats**: Monitor progression
4. **Save History**: Export command history for review

---

## File Structure

```
secshell-pro/
├── core/                  # Main application code
├── configs/              # Configuration files
├── plugins/              # Custom plugins directory
├── reports/              # Generated reports and data
├── shortcuts/            # YAML shortcut definitions
├── assets/               # Banner, icons, resources
├── Makefile              # Build automation
├── requirements.txt      # Python dependencies
└── [shell scripts]       # Startup scripts
```

---

## Support & Resources

### Documentation Files

- **README.md** - Feature overview
- **QUICKSTART.md** - Getting started
- **CTF_COMMANDS.md** - CTF command reference
- **MASTER_GUIDE.md** - This comprehensive guide

### Command Help

```bash
SecShell> help            # General help
SecShell> help <cmd>      # Help for specific command
SecShell> ctf --help      # CTF mode help
```

### Check Status

```bash
SecShell> status          # System status
SecShell> tools verify    # Tool installation status
SecShell> ctf list        # Available patterns
```

---

## Version Info

**SecShell PRO** - Phase 7 Complete
- Intelligent Learning System ✓
- PDF Report Generation ✓
- Real CTF Assistance Tool ✓
- Plugin Architecture ✓
- 15+ Security Shortcuts ✓

---

**Ready for professional security automation and CTF competitions!** 🚀

Last Updated: November 29, 2025
