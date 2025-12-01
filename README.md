SecShell PRO — Intelligent Security Automation Platform
========================================================

A comprehensive security tool orchestration framework with intelligent learning, 
CTF challenges, and professional report generation.

## Features

### Core Intelligence
- **Adaptive Learning**: Tracks command history, learns patterns, suggests next steps
- **Skill Level Tracking**: Beginner → Intermediate → Advanced → Expert progression
- **Smart Suggestions**: AI-powered recommendations based on usage patterns
- **Tool Management**: Automatic installation and verification of 13+ security tools

### Security & Automation
- **15+ Security Shortcuts**: Pre-built workflows for common pentesting tasks
- **YAML Shortcuts**: Define custom commands and workflows
- **Plugin System**: Load custom tools and utilities
- **Safety Features**: Require force flag for destructive operations

### Operational Features
- **PDF Report Generation**: Professional security reports with findings and metadata
- **CTF Mode**: 8 built-in capture-the-flag challenges with hints and scoring
- **Command History**: Full audit trail of executed commands
- **Learning Database**: Persistent storage of skills, patterns, and progress

### Setup & Deployment
- **One-Click Setup**: `make run` or `bash start_secshell.sh`
- **Desktop Launcher**: Quick access from desktop
- **Automated Testing**: Comprehensive test suite
- **Docker Ready**: Container-based deployment

## Quick Start

### Option 1: One-Command Setup (Recommended)
```bash
make run
```

### Option 2: Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 core/main.py
```

### Option 3: Desktop Launcher
- Double-click `~/Desktop/SecShellPRO.desktop`
- Or use: `bash start_secshell.sh`

## Configuration

Edit `configs/config.yaml`:
```yaml
workspace: ./reports              # Output directory
default_dry_run: false            # Enable actual execution
plugins_dir: ./plugins            # Custom plugins
shortcuts_dir: ./shortcuts        # Command definitions
learner_db: ./reports/learner_db.json  # Learning data
```

## Commands

### Core Commands
```
shortcuts         - List all available security shortcuts
stats             - Show command statistics and usage
tips              - Get personalized learning tips
level             - Show your current skill level
tools list        - Show available security tools
tools install <name> - Install a specific tool
help <name>       - Get detailed help for a shortcut
```

### Report Generation
```
<command>         - After execution, prompted: "Generate report? (y/n)"
                  Creates professional PDF in reports/ directory
```

### CTF Assistance Tool
```
ctf extract <output>      - Extract flags from command output
ctf capture <flag>        - Manually capture a flag
ctf flags                 - List all captured flags
ctf mark <id>            - Mark flag as submitted
ctf stats                - Show capture statistics
ctf export               - Export flags to file
ctf list                 - Show available patterns
ctf add-pattern          - Add custom extraction pattern
```

### Security Shortcuts (Examples)
```
enum-full target=<host>      - Full target enumeration
brute-ssh target=<host>      - SSH brute force
web-vuln-scan target=<host>  - Web vulnerability scan
osint-domain target=<domain> - OSINT domain recon
watch-ssh                    - Watch for SSH attempts
```

## File Structure

```
secshell-pro/
├── core/
│   ├── main.py                 # REPL and command handler
│   ├── dispatcher.py           # Command routing and execution
│   ├── learner.py             # Adaptive learning engine
│   ├── report_generator.py    # PDF report generation
│   ├── ctf_mode.py            # CTF challenge system
│   ├── tool_installer.py      # Tool management
│   ├── plugin_manager.py      # Plugin system
│   └── ... (other modules)
├── shortcuts/                  # YAML shortcut definitions
│   ├── pentest.yaml
│   ├── advanced.yaml
│   ├── osint.yaml
│   └── soc.yaml
├── reports/                    # Generated reports and data
│   ├── report_*.pdf          # Security reports
│   ├── ctf_data.json         # CTF progress
│   └── learner_db.json       # Learning data
├── configs/config.yaml         # Main configuration
├── requirements.txt            # Python dependencies
├── Makefile                    # Build automation
└── README.md                   # This file
```

## Features by Phase

### Phase 1-2: Foundation & Tools ✓
- Fixed execution engine
- Verified 10+ security tools
- Created tool management system

### Phase 3: AI Integration ✓
- Optional OpenAI integration
- Smart summarization
- Flexible AI client

### Phase 4: Intelligence ✓
- Adaptive learner with skill progression
- Pattern recognition and suggestions
- Tool installer with 13 managed tools
- Plugin system for custom shortcuts

### Phase 5: One-Click Setup ✓
- Makefile with multiple targets
- Desktop launcher
- Automated dependency installation

### Phase 6: Personalization ✓
- Creator credit (Houshic Balasubramanian)
- Customizable banner with fun phrases
- Clean, professional UI

### Phase 7: Reports & CTF ✓
- Professional PDF report generation
- 8 built-in CTF challenges
- Hint system with progressive difficulty
- Scoring and leaderboard system
- Full dispatcher integration

## CTF Challenges

### Available Challenges
1. **Port Discovery 101** (50 pts) - Nmap port scanning
2. **Web Headers Hunt** (50 pts) - HTTP header identification
3. **DNS Domain Enumeration** (50 pts) - DNS reconnaissance
4. **Service Identification** (75 pts) - Service version detection
5. **Web Vulnerability Scout** (100 pts) - Web scanning
6. **WHOIS Investigation** (50 pts) - Domain WHOIS lookup
7. **UDP Service Discovery** (75 pts) - UDP scanning
8. **Directory Discovery** (75 pts) - Web directory enumeration

### Example Workflow
```bash
SecShell> ctf list
[Shows all challenges]

SecShell> ctf start port_scan_101
[Challenge starts, description displayed]

SecShell> ctf hint
[💡 Hint 1/2] Use nmap with the -p- flag...

SecShell> ctf flag 22
[✓] CORRECT FLAG! [+] +50 points! [🏆] Total Score: 50

SecShell> ctf leaderboard
[Shows your progress and completed challenges]
```

## Report Generation

### Automatic Reporting
After running any security command:
```
[exec] nmap -A example.com
[output]
Nmap scan report for example.com
...

[report] Would you like to generate a report? (y/n): y
[✓] Report generated: reports/report_2025-11-29_10-30-45.pdf
```

### Report Contents
- Title with timestamp
- Target and metadata
- Full scan output
- Findings and vulnerabilities
- Professional formatting with tables

## Learning System

### How It Works
1. Every command execution is recorded
2. System tracks patterns and preferences
3. Skill level adjusts based on:
   - Number of commands executed (10, 50 required)
   - Number of different tools used (5, 10 required)
   - Command diversity
4. Higher levels unlock smarter suggestions

### Skill Levels
- **Beginner**: First 10 commands, few tools
- **Intermediate**: 10-50 commands, 5+ tools
- **Advanced**: 50+ commands, 10+ tools
- **Expert**: All challenges completed, mastered patterns

### Getting Tips
```bash
SecShell> tips
[💡 Learning Tips]
- Your most used tool: nmap (8 uses)
- Try web scanning for HTTP targets
- You're strong with reconnaissance!
```

## Testing

### Run All Tests
```bash
bash test_intelligent.sh  # Core functionality
bash test_phase7.sh      # Reports and CTF
bash demo_phase7.sh      # Full feature demo
```

### Make Targets
```bash
make help              # Show all targets
make setup-venv        # Create Python venv
make install-deps      # Install dependencies
make install-tools     # Install security tools
make run               # Run SecShell
make test              # Run all tests
make clean             # Clean up
```

## Keyboard Shortcuts

- `Ctrl+C` - Exit or cancel current operation
- `Ctrl+D` - Exit SecShell
- `Tab` - Auto-complete commands
- `↑/↓` - Command history navigation

## Security Notes

- **Dry-Run Mode**: Enabled by default, commands show without executing
- **Destructive Safety**: Unsafe operations require `force=true`
- **Audit Trail**: All commands logged to `learner_db.json`
- **Configuration**: Sensitive values go in `config.yaml` (git-ignored)

## Troubleshooting

### Commands not executing
- Check `default_dry_run` in config.yaml (set to `false` for real execution)
- Verify tool is installed: `tools check <name>`
- Check dry-run status in help message

### Reports not generating
- Ensure `reportlab` is installed: `pip install reportlab`
- Check disk space in `reports/` directory
- Falls back to text reports if PDF fails

### CTF mode issues
- Verify `ctf_challenges.json` exists in reports/
- Check flag format (case-insensitive, no extra spaces)
- Try `ctf hint` for correct flag format

### Learning system not progressing
- Execute more commands: `ctf list`, `shortcuts`, `tips` don't count
- Use different tools in shortcuts
- Check `learner_db.json` in reports/ for tracking

## Contributing

To add custom shortcuts:
1. Create or edit `shortcuts/custom.yaml`
2. Format: `name, cmd, desc, safe (bool), tags`
3. Reload with: `shortcuts` command

To add CTF challenges:
1. Edit `reports/ctf_challenges.json`
2. Add entry with: `id, name, description, hints[], flag, points`
3. Restart SecShell to reload

## Requirements

- Python 3.8+
- Linux/Kali Linux (tested)
- pip package manager
- 13+ security tools (auto-installable via `tools install`)

### Python Dependencies
- prompt_toolkit (REPL)
- PyYAML (config)
- rich (formatting)
- reportlab (PDF reports)
- requests (HTTP)
- beautifulsoup4 (HTML parsing)
- fuzzywuzzy (fuzzy matching)

## License

Created by: Houshic Balasubramanian
Purpose: Security education and penetration testing automation

## Credits

- Kali Linux tools and utilities
- Security research community
- Open-source libraries

## Version

**SecShell PRO v1.0 - Phase 7 Complete** 🚀

Features: Intelligence + Reports + CTF + One-Click Setup
Status: Production Ready
Last Updated: November 2025
