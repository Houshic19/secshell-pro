# SecShell PRO - Complete Quick Reference

## 🚀 Start SecShell

**Recommended (One-Click)**
```bash
make run
```

**Or**
```bash
./run_secshell.sh
```

**Or (Desktop)**
Double-click: `~/Desktop/SecShellPRO.desktop`

---

## 📊 What You'll See

```
SecShell PRO — type 'help' for commands. Dry-run ON.
📊 Learning Level: BEGINNER
SecShell> _
```

Type `help` to see all commands!

---

## 🎯 Most Common Commands

| Command | Purpose |
|---------|---------|
| `shortcuts` | List security commands |
| `enum-full target=<host>` | Full target scan |
| `ctf list` | Show CTF challenges |
| `ctf start <id>` | Start a challenge |
| `stats` | Show your usage stats |
| `level` | Check skill level |
| `exit` | Leave SecShell |

---

## 🎮 CTF Assistance Tool (Real CTF Help!)

### Extract Flags Automatically
```bash
SecShell> ctf extract "<command_output>"
# Shows all detected flags, asks to capture
```

### Capture a Flag Manually
```bash
SecShell> ctf capture "flag{found_it}" challenge="web" category="web"
```

### View Your Captured Flags
```bash
SecShell> ctf flags
# List all flags with capture status

SecShell> ctf flags submitted=true
# Show only submitted flags
```

### Mark as Submitted
```bash
SecShell> ctf mark 1
# Mark flag #1 as submitted to competition
```

### Check Statistics
```bash
SecShell> ctf stats
# Shows total, submitted, pending breakdown by category
```

### Export Flags
```bash
SecShell> ctf export
# Creates flags_export_<timestamp>.json

SecShell> ctf export format=txt
# Creates text file instead
```

### Custom Patterns
```bash
SecShell> ctf list
# Show all built-in patterns (flag{...}, MD5, SHA1, etc.)

SecShell> ctf add-pattern id=custom regex="PATTERN" name="Custom"
# Add custom extraction pattern
```

### Typical Competition Workflow
```bash
# 1. Set up custom pattern if needed
SecShell> ctf add-pattern id=myctf regex="SECRET\{[^}]+\}" category="web"

# 2. Run security commands
SecShell> enum-full target=vulnerable.site

# 3. Extract flags from output
SecShell> ctf extract "[output_from_scan]" challenge="enum_phase"

# 4. Capture additional flags manually
SecShell> ctf capture "flag_found_manually" challenge="web"

# 5. Track progress
SecShell> ctf flags
SecShell> ctf stats

# 6. Mark as submitted when done
SecShell> ctf mark 1

# 7. Export for submission/backup
SecShell> ctf export format=txt
```

---

## 📄 Report Generation (New!)

**Automatic** - After any command:
```
[exec] nmap -A example.com
[output] ... results ...
[report] Generate report? (y/n): y
[✓] Report generated: reports/report_2025-11-29_10-30-45.pdf
```

**View Reports**
```bash
ls reports/report_*
```

**Report Contents**
- ✓ Timestamp
- ✓ Target info
- ✓ Scan output
- ✓ Findings & vulnerabilities
- ✓ Professional formatting

---

## 🧠 Learning System

### Check Your Level
```
SecShell> level
[📈 Your Level] INTERMEDIATE
```

### Get Tips
```
SecShell> tips
[💡] You're strong at reconnaissance!
[💡] Try web scanning next!
```

### View Stats
```
SecShell> stats
[📊] Most used: nmap (12 times), gobuster (8 times)
```

---

## 🔧 Tool Management

### List Tools
```
SecShell> tools list
[Shows 13+ security tools with install status]
```

### Install Tool
```
SecShell> tools install smbmap
Installing smbmap...
✓ smbmap installed successfully
```

### Check Tool
```
SecShell> tools check nmap
[✓] nmap: Tool working
```

---

## 🎯 Security Shortcuts (Examples)

```bash
enum-full target=scanme.nmap.org
brute-ssh target=192.168.1.1
web-vuln-scan target=example.com
osint-domain target=example.com
quick-scan target=192.168.1.0/24
masscan-fast target=10.0.0.0/8
dns-enum target=example.com
whois-lookup target=example.com
```

---

## 📚 Learning Path

### Day 1: Explore
```
SecShell> help
[Shows all commands]

SecShell> shortcuts
[See all security tools]

SecShell> level
[Check: BEGINNER]
```

### Day 2: Learn
```
SecShell> quick-scan target=localhost
[Run first command]

SecShell> stats
[See: 1 command run]

SecShell> tips
[Get recommendations]
```

### Day 3: Practice
```
SecShell> enum-full target=scanme.nmap.org
[Generate report]

SecShell> ctf start port_scan_101
[Try CTF challenge]

SecShell> ctf flag 22
[Submit answer]
```

### Week 1: Level Up
```
SecShell> level
[Progress: INTERMEDIATE!]

SecShell> ctf leaderboard
[Challenges: 3, Score: 150]
```

---

## ⚙️ Configuration

Edit `configs/config.yaml` to customize:

```yaml
default_dry_run: false          # Actually execute commands
workspace: ./reports            # Where reports save
```

---

## 🧪 Testing

```bash
bash test_phase7.sh            # Run Phase 7 tests
bash demo_phase7.sh            # See full demo
make test                      # All tests
```

---

## 💾 Important Files

| File | Purpose |
|------|---------|
| `reports/report_*.pdf` | Generated security reports |
| `reports/ctf_data.json` | Your CTF progress |
| `reports/ctf_challenges.json` | Challenge definitions |
| `reports/learner_db.json` | Your learning data |
| `shortcuts/*.yaml` | Command definitions |
| `configs/config.yaml` | Settings |

---

## 🆘 Quick Troubleshooting

### "Command didn't execute"
- It's in dry-run mode (safe)
- To actually run: `command force=true` or set `default_dry_run: false`

### "Tool not found"
- Run: `tools install <name>`

### "Report generation failing"
- Install: `pip install reportlab`

### "CTF flag shows wrong"
- Use: `ctf hint` to see correct format
- Flags are case-insensitive
- Watch for extra spaces

---

## 🎓 Pro Tips

1. **Fuzzy matching**: `enum-ful` → suggests `enum-full`
2. **Tab complete**: Press Tab for auto-complete
3. **History**: Press ↑/↓ to navigate history
4. **Custom commands**: Add your own in `shortcuts/custom.yaml`
5. **Reports**: Save every important scan
6. **Learning**: Check `tips` regularly for suggestions
7. **CTF**: Start with easy challenges to build momentum

---

## 📞 Quick Reference Cheat Sheet

```bash
# Learn
help                           # All commands
help enum-full                 # Specific command  
level                          # Your skill level
tips                          # Personalized tips
stats                         # Usage statistics

# Security
shortcuts                     # List all commands
enum-full target=HOST        # Scan a host
brute-ssh target=HOST        # SSH brute force
web-vuln-scan target=HOST    # Find web vulns

# CTF (New!)
ctf list                     # Show challenges
ctf start port_scan_101      # Begin challenge
ctf hint                     # Get hint
ctf flag ANSWER              # Submit answer
ctf leaderboard              # Your progress

# Tools (New!)
tools list                   # All tools
tools check NAME             # Verify installed
tools install NAME           # Install tool

# Reports (New!)
# Auto-prompted after commands
ls reports/report_*          # View reports

# System
exit                         # Leave SecShell
```

---

## 🚀 Next Steps

1. **Run it**: `make run`
2. **Explore**: Type `help`
3. **Learn**: Try `stats` and `tips`
4. **Practice**: Run a scan: `enum-full target=localhost`
5. **Report**: Generate a report when prompted
6. **CTF**: Try a challenge: `ctf start port_scan_101`
7. **Level up**: Keep using it, system learns your style!

---

**SecShell PRO v1.0 - Production Ready! 🎉**

All features working: Intelligence ✓ | Reports ✓ | CTF ✓ | One-Click Setup ✓

Type `make run` and start hacking! 🚀

