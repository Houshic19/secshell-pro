# CTF Assistance Tool - Command Reference

## Quick Reference Card

### Basic Commands

```bash
ctf list                              # Show available patterns
ctf extract "<output>"               # Auto-extract flags
ctf capture "<flag>"                 # Save a flag manually
ctf flags                            # List all captured flags
ctf mark <id>                        # Mark flag as submitted
ctf stats                            # Show statistics
ctf export                           # Export flags
```

## Complete Command Reference

### 1. Flag Extraction

**Command:** `ctf extract`

Extract flags automatically from command output using regex patterns.

```bash
# Basic extraction (shows matches, asks to capture)
ctf extract "port 22 ssh flag{found_it}"

# With challenge name
ctf extract "output" challenge="web_challenge"

# Multi-line output
ctf extract "$(command_output)"
```

**Behavior:**
- Scans against all patterns
- Shows matches with pattern type
- Prompts: "Capture these flags? (y/n):"
- Auto-saves if confirmed

**Patterns Used:** All 6 built-in patterns (flag{}, MD5, SHA1, hex, base64, CTF{})

---

### 2. Flag Capture

**Command:** `ctf capture`

Manually capture a flag with validation.

```bash
# Minimal
ctf capture "flag{example}"

# With challenge info
ctf capture "flag{web_rce}" challenge="web_app"

# With category
ctf capture "flag{xss}" challenge="web" category="web"

# Full specification
ctf capture "md5hash" challenge="crypto" category="hash"
```

**Categories:** manual, hash, encoding, standard, web, crypto, reversing, pwn, misc

**Validation:**
- ✓ Not empty
- ✓ Printable characters
- ✓ No newlines/special chars

---

### 3. Flag Listing

**Command:** `ctf flags`

List all captured flags with status.

```bash
# All flags
ctf flags

# Only submitted
ctf flags submitted=true

# Only pending
ctf flags submitted=false
```

**Output Format:**
```
ID    Flag                          Challenge    Status
1     flag{example}                 web_app      ⏳ Pending
2     md5hash                       crypto       ✓ Submitted
```

---

### 4. Submission Status

**Command:** `ctf mark` or `ctf submit`

Mark a captured flag as submitted to the competition.

```bash
# Mark flag #1 as submitted
ctf mark 1

# Alternative syntax
ctf submit 1
```

**Effect:**
- Updates submission timestamp
- Changes status to "✓ Submitted"
- Reflected in stats

---

### 5. Statistics

**Command:** `ctf stats`

Show flag capture statistics.

```bash
ctf stats
```

**Output Shows:**
```
Total Flags Captured: 5
  ✓ Submitted: 2
  ⏳ Pending: 3

Flags by Category:
  • web: 2
  • hash: 2
  • standard: 1
```

---

### 6. Pattern Management

**Command:** `ctf list` or `ctf patterns`

Show available extraction patterns.

```bash
ctf list

# or
ctf patterns
```

**Built-in Patterns:**
```
standard_flag    Standard Flag Format    flag{...}
ctf_format       CTF Format             CTF{...}
hex_flag         Hex/Hash               [a-f0-9]{32,64}
md5              MD5 Hash               [a-f0-9]{32}
sha1             SHA1 Hash              [a-f0-9]{40}
base64           Base64 Encoded         [A-Za-z0-9+/]{20,}
```

---

### 7. Custom Patterns

**Command:** `ctf add-pattern`

Add custom extraction patterns for specific CTFs.

```bash
# Minimal
ctf add-pattern id=custom_web regex="SECRET\{[^}]+\}"

# With name and category
ctf add-pattern id=myctf regex="FLAG\[.*?\]" name="MyCompetition" category="standard"

# Complex regex
ctf add-pattern id=encoded regex="enc_[A-Z0-9]+" category="encoding"
```

**Parameters:**
- `id` (required) - Pattern identifier
- `regex` (required) - Regex pattern
- `name` (optional) - Display name
- `category` (optional) - Category name

**After adding:**
- Immediately available for extraction
- Stored in ctf_patterns.json
- Persistent across sessions

---

### 8. Export

**Command:** `ctf export`

Export all captured flags to file.

```bash
# Default (JSON)
ctf export

# Text format
ctf export format=txt

# Specify format
ctf export format=json
```

**Output Files:**
- `reports/flags_export_20251129_103045.json`
- `reports/flags_export_20251129_103045.txt`

**JSON Format:**
```json
{
  "1": {
    "id": 1,
    "flag": "flag{example}",
    "challenge": "web",
    "category": "standard",
    "timestamp": "2025-11-29T10:30:45",
    "submitted": false
  }
}
```

**Text Format:**
```
[1] flag{example} (web - standard)
[2] md5hash (crypto - hash)
```

---

## Use Case Examples

### Use Case 1: Web Challenge

```bash
# Run web scan
enum-full target=target.site > output.txt

# Extract flags
ctf extract "$(cat output.txt)" challenge="web_enum"

# System shows detected flags and asks to capture
[✓] Found 2 potential flags
1. [Standard Flag] flag{found_it}
2. [Hex] a1b2c3d4...

Capture these flags? (y/n): y

# Flags are saved
[✓] 2 flags captured

# Later, mark as submitted
ctf mark 1
ctf mark 2

# Check progress
ctf stats
```

### Use Case 2: Hash Challenge

```bash
# Capture manually found hash
ctf capture "5d41402abc4b2a76b9719d911017c592" challenge="crypto_md5" category="hash"

# Check what we have
ctf flags

# Submit
ctf mark 1

# Stats
ctf stats
```

### Use Case 3: Multiple Challenges

```bash
# Before competition - add custom pattern
ctf add-pattern id=myctf regex="FLAG\{[^}]+\}" name="MyCompetition" category="standard"

# During competition
ctf extract "scan_output_1" challenge="challenge_1"
ctf capture "manual_flag_1" challenge="challenge_2"
ctf extract "scan_output_2" challenge="challenge_3"

# Check progress
ctf flags
ctf stats

# Submit as you go
ctf mark 1
ctf mark 2

# End of competition
ctf export format=txt
```

---

## Typical Competition Workflow

### Pre-Competition (Setup)
```bash
SecShell> ctf add-pattern id=comp regex="FLAG\{[^}]+\}" name="Competition" category="standard"
SecShell> ctf list  # Verify patterns
```

### During Competition (Execution)
```bash
# For each challenge/scan:
SecShell> enum-full target=vulnerable.site
# [output] ... long scan results ...

SecShell> ctf extract "$(previous_output)" challenge="enum_phase"
# [System shows potential flags]
# Capture these flags? (y/n): y

# Or manual capture
SecShell> ctf capture "found_flag" challenge="web_xss" category="web"

# Track all captures
SecShell> ctf flags

# Check progress
SecShell> ctf stats
```

### Submit Flags
```bash
# Once you submit to competition
SecShell> ctf mark 1  # Mark as submitted
SecShell> ctf mark 2
# ...
```

### End of Competition (Export)
```bash
SecShell> ctf export format=txt
# [✓] Exported to reports/flags_export_...txt
```

---

## Key Features

### Automatic Detection
- 6 built-in patterns included
- Detects most common flag formats
- Case-insensitive option available

### Validation
- Checks for empty/invalid flags
- Prevents newlines and control chars
- Basic format validation

### Organization
- Track by challenge name
- Categorize by type
- Track submission status
- Timestamps for all entries

### Flexibility
- Add custom patterns anytime
- Multiple format exports
- JSON and text output
- Persistent database

### Statistics
- Total flags captured
- Submitted vs pending count
- Breakdown by category
- Export for backup/sharing

---

## Tips & Best Practices

1. **Add patterns early** - Before competition starts
2. **Use challenge names** - Organize captures effectively
3. **Extract first** - Automatic detection finds most flags
4. **Mark as you submit** - Keep status in sync
5. **Export regularly** - Backup to prevent loss
6. **Categorize properly** - Makes searching easier
7. **Check stats** - Track progress at glance

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Flag not extracted | Use `ctf add-pattern` with correct regex |
| Can't find flag | Use `ctf flags` to list all |
| Pattern not working | Verify regex with `ctf add-pattern` |
| Export fails | Check write permissions in reports/ |
| Lost flags | Check `reports/ctf_data.json` |

---

## Data Persistence

All data automatically saved to:
- `reports/ctf_data.json` - Captured flags
- `reports/ctf_patterns.json` - Extraction patterns
- `reports/flags_export_*.json|txt` - Exports

Data survives:
- ✓ Exiting SecShell
- ✓ Restarting competition
- ✓ Adding new patterns
- ✓ Changing flags status

---

## Integration Points

### With Security Shortcuts
```bash
SecShell> enum-full target=site.com
# Output shown in terminal
SecShell> ctf extract "[output_above]" challenge="enum"
```

### With Report Generation
```bash
# You get both:
# - reports/report_*.pdf (vulnerability report)
# - reports/ctf_data.json (captured flags)
```

### With Learning System
```bash
SecShell> stats        # See command usage
SecShell> ctf extract "output"  # Capture flags
SecShell> ctf stats    # See flag progress
```

---

## Command Syntax Quick Reference

```
ctf list                                          Show patterns
ctf extract "<text>" [challenge=<name>]          Extract flags
ctf capture "<flag>" [challenge=<name>] [category=<cat>]  Save flag
ctf flags [submitted=true|false]                 List flags
ctf mark <id>                                    Submit flag
ctf stats                                        Show statistics
ctf export [format=json|txt]                     Export flags
ctf add-pattern id=<id> regex=<regex> [name=<name>] [category=<cat>]  Add pattern
```

---

## Summary

| Task | Command |
|------|---------|
| See available patterns | `ctf list` |
| Extract from output | `ctf extract "<text>"` |
| Save flag | `ctf capture "<flag>"` |
| View all flags | `ctf flags` |
| Mark submitted | `ctf mark <id>` |
| Statistics | `ctf stats` |
| Export | `ctf export` |
| Custom pattern | `ctf add-pattern ...` |

---

**Ready to dominate CTFs! 🚀**

Use these commands to efficiently manage flag capture during competitions.
