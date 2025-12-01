# CTF Assistance Tool - Real Flag Capture & Extraction

## Overview

SecShell PRO now includes a **real CTF assistance tool** designed to help you capture flags during actual Capture-The-Flag competitions. This tool provides:

- **Automatic flag extraction** using regex patterns
- **Flag validation** to ensure quality
- **Flag tracking** for organizing captures
- **Pattern management** for different flag formats
- **Export functionality** for submission or documentation

## Quick Start

### Extract Flags from Output

```bash
SecShell> ctf extract "<command_output>"
# Shows all detected flags with patterns

# Then optionally capture them
# System asks: "Capture these flags? (y/n): y"
```

### Manually Capture a Flag

```bash
SecShell> ctf capture "flag{your_flag_here}" challenge="web_challenge" category="web"

# Output:
# [✓] Flag captured!
#     ID: 1
#     Flag: flag{your_flag_here}
#     Challenge: web_challenge
```

### View Captured Flags

```bash
SecShell> ctf flags
# Shows all captured flags with status

SecShell> ctf flags submitted=true
# Shows only submitted flags
```

### Mark Flag as Submitted

```bash
SecShell> ctf mark 1
# Mark flag ID 1 as submitted to the competition
```

### View Statistics

```bash
SecShell> ctf stats
# Shows total captured, submitted, pending
# Breakdown by category
```

## Available Commands

### Flag Extraction

#### `ctf extract <output> [challenge=name]`
Extract flags from command output automatically.

```bash
# Extract from nmap output
SecShell> ctf extract "Port 22/tcp open ssh"

# Extract with challenge name
SecShell> ctf extract "flag{abc123}" challenge="web_app"
```

**What happens:**
1. Scans output against all patterns
2. Shows all matches with pattern types
3. Asks if you want to capture them
4. Auto-saves to database if confirmed

### Flag Capture

#### `ctf capture <flag_text> [challenge=name] [category=type]`
Manually add a flag you found.

```bash
SecShell> ctf capture "flag{found_it}"
SecShell> ctf capture "md5hash123" challenge="crypto" category="hash"
SecShell> ctf capture "aGVsbG8=" challenge="encoding" category="base64"
```

**Categories:** manual, hash, encoding, standard, web, crypto, reversing, pwn, misc

### Flag Management

#### `ctf flags [submitted=true|false]`
List all captured flags.

```bash
SecShell> ctf flags
# Shows all flags with ID, text, challenge, status

SecShell> ctf flags submitted=true
# Shows only submitted flags
```

#### `ctf mark <flag_id>`
Mark a flag as submitted to the competition.

```bash
SecShell> ctf mark 1
# Marks flag #1 as submitted
```

#### `ctf export [format=json|txt]`
Export all captured flags.

```bash
SecShell> ctf export
# Creates reports/flags_export_<timestamp>.json

SecShell> ctf export format=txt
# Creates reports/flags_export_<timestamp>.txt
```

### Pattern Management

#### `ctf list` or `ctf patterns`
Show available extraction patterns.

```bash
SecShell> ctf list
# Shows all built-in patterns:
# - standard_flag: flag{...}
# - ctf_format: CTF{...}
# - hex_flag: [a-f0-9]{32,64}
# - md5, sha1, base64, etc.
```

#### `ctf add-pattern id=<id> regex=<regex> [name=<name>] [category=<cat>]`
Add a custom extraction pattern.

```bash
SecShell> ctf add-pattern id=custom_web regex="SECRET\{[^}]+\}" name="Custom Secret" category="web"
```

**Then it's available for extraction:**
```bash
SecShell> ctf extract "SECRET{my_secret}"
# Now detects with custom_web pattern
```

### Statistics

#### `ctf stats`
Show capture statistics.

```bash
SecShell> ctf stats
# Output:
# Total Flags Captured: 5
#   ✓ Submitted: 2
#   ⏳ Pending: 3
#
# Flags by Category:
#   • web: 2
#   • hash: 2
#   • standard: 1
```

## Built-in Extraction Patterns

| Pattern | Regex | Example | Use Case |
|---------|-------|---------|----------|
| standard_flag | `flag\{[^}]+\}` | flag{my_flag} | Standard CTF flags |
| ctf_format | `CTF\{[^}]+\}` | CTF{FLAG123} | CTF format flags |
| hex_flag | `[a-f0-9]{32,64}` | a1b2c3d4... | Hex strings/hashes |
| md5 | `[a-f0-9]{32}` | 5d41402abc... | MD5 hashes |
| sha1 | `[a-f0-9]{40}` | aaf4c61ddcc... | SHA1 hashes |
| base64 | `[A-Za-z0-9+/]{20,}` | aGVsbG8= | Base64 encoded |

## Workflow Examples

### Example 1: Web Challenge

```bash
# Run web scan
SecShell> web-vuln-scan target=vulnerable.local

# Output shows HTML with hidden flag
# [output] ... <div class="flag">flag{web_rce}</div> ...

# Extract automatically
SecShell> ctf extract "[output_here]" challenge="web_rce"

# System detects and asks to capture
# [✓] Found 1 potential flag(s):
# 1. [Standard Flag Format] flag{web_rce}
# Capture these flags? (y/n): y

# Flag is saved
SecShell> ctf flags
# Shows flag #1 as pending
```

### Example 2: Crypto Challenge

```bash
# Get hash from crypto challenge
SecShell> ctf capture "5d41402abc4b2a76b9719d911017c592" challenge="crypto_md5" category="hash"

# Mark as submitted when done
SecShell> ctf mark 1

# Check progress
SecShell> ctf stats
# Submitted: 1/1
```

### Example 3: Multiple Flags from Output

```bash
# Run command that outputs multiple flags
SecShell> enum-full target=example.com > output.txt

# Extract all flags at once
SecShell> ctf extract "$(cat output.txt)" challenge="full_enum"

# System shows:
# Found 3 potential flags
# - flag{open_ports}
# - 192.168.1.1 (possibly IP flag)
# - 3c0f7a8b... (hash)

# You choose which to capture
```

### Example 4: Custom Pattern for Specific CTF

```bash
# Add custom pattern for competition
SecShell> ctf add-pattern id=myctf regex="MyFlag\[[^\]]+\]" name="MyCompetition Format" category="standard"

# Now when extracting:
SecShell> ctf extract "MyFlag[secret123]" challenge="myctf_round1"

# Detects with custom pattern!
```

## File Structure

### Stored Data

```
reports/
├── ctf_data.json           # All captured flags
├── ctf_patterns.json       # Extraction patterns
└── flags_export_*.json|txt # Exported flag lists
```

### Sample Flag Entry

```json
{
  "1": {
    "id": 1,
    "flag": "flag{example}",
    "challenge": "web_rce",
    "category": "web",
    "timestamp": "2025-11-29T10:30:45.123456",
    "submitted": true,
    "submitted_at": "2025-11-29T10:35:20.123456"
  }
}
```

## Advanced Usage

### Integrate with Shortcuts

Capture output from security tools automatically:

```bash
SecShell> enum-full target=example.com
[output] ... [long nmap output] ...

# Manually extract afterward
SecShell> ctf extract "nmap output here" challenge="enum"
```

### Pre-Competition Setup

1. Add custom patterns for the competition:
```bash
SecShell> ctf add-pattern id=hackathon regex="FLAG\{[^}]+\}" name="Hackathon" category="standard"
```

2. Ready to go! During competition:
```bash
SecShell> ctf extract "[tool output]" challenge="challenge_name"
SecShell> ctf capture "flag_text" challenge="challenge_name"
SecShell> ctf mark 1  # When submitted
SecShell> ctf stats   # Track progress
```

### Export for Team

Share captured flags with team:

```bash
SecShell> ctf export format=txt
# Creates flags_export_20251129_103045.txt

# Share via:
# scp reports/flags_export_*.txt team_member:
```

## Validation

The tool validates flags with basic checks:

- ✓ Not empty
- ✓ Printable characters
- ✓ No newlines/control characters
- ✓ Reasonable length

```bash
SecShell> ctf capture "invalid\nflag"
# [✗] Invalid flag format
#     Validations: {'no_newlines': False}
```

## Tips & Best Practices

1. **Use extract first** - Automatic detection catches many patterns
2. **Add custom patterns early** - Before competition starts
3. **Mark as submitted** - Track what you've turned in
4. **Regular exports** - Backup flags periodically
5. **Use challenge names** - Organize by problem
6. **Check stats** - See progress at a glance
7. **Categorize properly** - Helps with organization

## Troubleshooting

### Flag not detected
- Try `ctf add-pattern` with correct regex
- Manual capture with `ctf capture`

### Can't find captured flag
- Use `ctf flags` to list all
- Check if it's marked as submitted

### Export not working
- Ensure write permissions to reports/
- Try `ctf export format=txt` if JSON fails

## Integration with Reports

Captured flags are separate from reports. Use together:

```bash
# Run security command
SecShell> web-vuln-scan target=site.com

# Output shown, report generated:
[report] Generate report? (y/n): y

# Then extract any flags found:
SecShell> ctf extract "[output_above]" challenge="web_vuln"

# Now you have:
# - reports/report_*.pdf (vulnerability report)
# - reports/ctf_data.json (captured flags)
```

## Summary

| Task | Command |
|------|---------|
| Extract flags from output | `ctf extract "<output>"` |
| Capture flag manually | `ctf capture "<flag>"` |
| View captured flags | `ctf flags` |
| Mark as submitted | `ctf mark <id>` |
| Show stats | `ctf stats` |
| Export flags | `ctf export` |
| List patterns | `ctf list` |
| Add pattern | `ctf add-pattern id=<id> regex=<regex>` |

---

**Ready to dominate CTF competitions!** 🚀

Use this tool during competitions to efficiently capture, track, and manage flags from multiple challenges.
