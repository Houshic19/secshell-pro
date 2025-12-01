"""
CTF Assistance Tool: Help capture flags in real CTF competitions.
Features: flag extraction, validation, patterns, and submission tracking.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from core.utils import ensure_dir


class CTFMode:
    """Real CTF assistance tool for flag extraction and tracking."""

    def __init__(self, workspace="./reports"):
        self.workspace = Path(workspace)
        ensure_dir(self.workspace)
        self.db_file = self.workspace / "ctf_data.json"
        self.flag_patterns_file = self.workspace / "ctf_patterns.json"
        self.captured_flags = {}
        self.flag_patterns = {}
        self._initialize()

    def _initialize(self):
        """Initialize CTF data files if they don't exist."""
        if not self.db_file.exists():
            self._save_data({
                "captured_flags": {},
                "statistics": {
                    "total_flags": 0,
                    "flags_by_category": {}
                }
            })

        if not self.flag_patterns_file.exists():
            self._create_default_patterns()

        self._load_data()

    def _load_data(self):
        """Load CTF data from database."""
        try:
            with open(self.db_file) as f:
                data = json.load(f)
                self.captured_flags = data.get("captured_flags", {})
        except:
            self.captured_flags = {}

        try:
            with open(self.flag_patterns_file) as f:
                data = json.load(f)
                self.flag_patterns = data.get("patterns", {})
        except:
            self.flag_patterns = {}

    def _save_data(self, data):
        """Save CTF data to database."""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[error] Failed to save CTF data: {e}")

    def _create_default_patterns(self):
        """Create default flag extraction patterns."""
        patterns = {
            "patterns": {
                "standard_flag": {
                    "name": "Standard Flag Format",
                    "regex": r"flag\{[^}]+\}",
                    "category": "standard",
                    "case_sensitive": True
                },
                "ctf_format": {
                    "name": "CTF Format",
                    "regex": r"CTF\{[^}]+\}",
                    "category": "ctf",
                    "case_sensitive": True
                },
                "hex_flag": {
                    "name": "Hex/Hash",
                    "regex": r"[a-f0-9]{32,64}",
                    "category": "hash",
                    "case_sensitive": False
                },
                "base64": {
                    "name": "Base64 Encoded",
                    "regex": r"[A-Za-z0-9+/]{20,}={0,2}",
                    "category": "encoding",
                    "case_sensitive": False
                },
                "md5": {
                    "name": "MD5 Hash",
                    "regex": r"[a-f0-9]{32}(?![a-f0-9])",
                    "category": "hash",
                    "case_sensitive": False
                },
                "sha1": {
                    "name": "SHA1 Hash",
                    "regex": r"[a-f0-9]{40}(?![a-f0-9])",
                    "category": "hash",
                    "case_sensitive": False
                }
            }
        }

        try:
            with open(self.flag_patterns_file, 'w') as f:
                json.dump(patterns, f, indent=2)
        except Exception as e:
            print(f"[error] Failed to create patterns: {e}")

    def extract_flags(self, text, pattern_name=None):
        """Extract flags from text using regex patterns."""
        found_flags = []

        if pattern_name:
            if pattern_name not in self.flag_patterns:
                print(f"[✗] Pattern '{pattern_name}' not found")
                return []
            patterns = {pattern_name: self.flag_patterns[pattern_name]}
        else:
            patterns = self.flag_patterns

        for pname, pattern_info in patterns.items():
            regex = pattern_info.get("regex", "")
            flags = re.findall(regex, text, re.IGNORECASE if not pattern_info.get("case_sensitive", False) else 0)
            
            for flag in flags:
                found_flags.append({
                    "flag": flag,
                    "pattern": pname,
                    "pattern_name": pattern_info.get("name", pname),
                    "category": pattern_info.get("category", "unknown"),
                    "timestamp": datetime.now().isoformat()
                })

        return found_flags

    def validate_flag(self, flag_text):
        """Validate flag format (basic checks)."""
        flag_text = flag_text.strip()

        validations = {
            "length": len(flag_text) > 0,
            "not_empty": len(flag_text.strip()) > 0,
            "printable": all(ord(c) < 128 and ord(c) >= 32 for c in flag_text),
            "no_newlines": '\n' not in flag_text and '\r' not in flag_text
        }

        is_valid = all(validations.values())
        
        return is_valid, validations

    def capture_flag(self, flag_text, challenge_name="", flag_category="manual"):
        """Capture and store a flag."""
        flag_text = flag_text.strip()
        
        is_valid, validations = self.validate_flag(flag_text)
        
        if not is_valid:
            print("[✗] Invalid flag format")
            print(f"    Validations: {validations}")
            return False

        flag_id = len(self.captured_flags) + 1
        flag_entry = {
            "id": flag_id,
            "flag": flag_text,
            "challenge": challenge_name,
            "category": flag_category,
            "timestamp": datetime.now().isoformat(),
            "submitted": False
        }

        self.captured_flags[str(flag_id)] = flag_entry
        self._save_progress()

        print(f"\n[✓] Flag captured!")
        print(f"    ID: {flag_id}")
        print(f"    Flag: {flag_text}")
        print(f"    Challenge: {challenge_name or '(not specified)'}")
        print(f"    Category: {flag_category}\n")

        return True

    def list_captured_flags(self, submitted_only=False):
        """List all captured flags."""
        if not self.captured_flags:
            print("\n[*] No flags captured yet.\n")
            return

        print("\n" + "="*70)
        print("[Captured Flags]")
        print("="*70)
        print(f"{'ID':<5} {'Flag':<35} {'Challenge':<15} {'Status'}")
        print("-"*70)

        for flag_id, flag_info in sorted(self.captured_flags.items(), key=lambda x: int(x[0])):
            if submitted_only and not flag_info.get("submitted"):
                continue
            
            flag = flag_info["flag"][:32] + "..." if len(flag_info["flag"]) > 35 else flag_info["flag"]
            challenge = flag_info.get("challenge", "")[:14]
            status = "✓ Submitted" if flag_info.get("submitted") else "⏳ Pending"
            
            print(f"{flag_id:<5} {flag:<35} {challenge:<15} {status}")

        print("="*70 + "\n")

    def mark_submitted(self, flag_id):
        """Mark a flag as submitted."""
        if str(flag_id) not in self.captured_flags:
            print(f"[✗] Flag ID {flag_id} not found")
            return False

        self.captured_flags[str(flag_id)]["submitted"] = True
        self.captured_flags[str(flag_id)]["submitted_at"] = datetime.now().isoformat()
        self._save_progress()

        flag_info = self.captured_flags[str(flag_id)]
        print(f"\n[✓] Flag {flag_id} marked as submitted")
        print(f"    Flag: {flag_info['flag']}")
        print(f"    Challenge: {flag_info.get('challenge', 'N/A')}\n")

        return True

    def extract_from_command_output(self, output, challenge_name=""):
        """Extract flags from command output and optionally capture them."""
        if not output:
            print("[✗] No output provided")
            return []

        flags = self.extract_flags(output)

        if not flags:
            print("[*] No flags extracted from output")
            return []

        print(f"\n[✓] Found {len(flags)} potential flag(s):")
        print("="*70)

        for i, flag_info in enumerate(flags, 1):
            print(f"\n{i}. [{flag_info['pattern_name']}] {flag_info['flag']}")
            print(f"   Category: {flag_info['category']}")

        print("\n" + "="*70)

        # Ask to capture
        if flags:
            try:
                capture = input("\nCapture these flags? (y/n): ").strip().lower()
                if capture in ('y', 'yes'):
                    for flag_info in flags:
                        self.capture_flag(
                            flag_info['flag'],
                            challenge_name=challenge_name,
                            flag_category=flag_info['category']
                        )
            except (KeyboardInterrupt, EOFError):
                pass

        return flags

    def show_statistics(self):
        """Show flag capture statistics."""
        if not self.captured_flags:
            print("\n[*] No statistics available yet.\n")
            return

        total = len(self.captured_flags)
        submitted = sum(1 for f in self.captured_flags.values() if f.get("submitted"))
        pending = total - submitted

        categories = {}
        for flag_info in self.captured_flags.values():
            cat = flag_info.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        print("\n" + "="*70)
        print("[CTF Statistics]")
        print("="*70)
        print(f"Total Flags Captured: {total}")
        print(f"  ✓ Submitted: {submitted}")
        print(f"  ⏳ Pending: {pending}")
        
        if categories:
            print(f"\nFlags by Category:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {cat}: {count}")

        print("="*70 + "\n")

    def list_patterns(self):
        """List available extraction patterns."""
        if not self.flag_patterns:
            print("[*] No patterns loaded")
            return

        print("\n" + "="*70)
        print("[Available Flag Patterns]")
        print("="*70)
        print(f"{'Pattern':<20} {'Name':<25} {'Category':<15}")
        print("-"*70)

        for pattern_id, pattern_info in self.flag_patterns.items():
            name = pattern_info.get("name", "")[:24]
            category = pattern_info.get("category", "")[:14]
            print(f"{pattern_id:<20} {name:<25} {category:<15}")

        print("="*70 + "\n")

    def add_custom_pattern(self, pattern_id, regex, name, category="custom"):
        """Add a custom extraction pattern."""
        self.flag_patterns[pattern_id] = {
            "name": name,
            "regex": regex,
            "category": category,
            "case_sensitive": False
        }

        # Save to patterns file
        patterns_data = json.loads(Path(self.flag_patterns_file).read_text())
        patterns_data["patterns"][pattern_id] = self.flag_patterns[pattern_id]
        
        with open(self.flag_patterns_file, 'w') as f:
            json.dump(patterns_data, f, indent=2)

        print(f"\n[✓] Custom pattern added: {pattern_id}")
        print(f"    Name: {name}")
        print(f"    Category: {category}\n")

    def export_flags(self, format="json"):
        """Export captured flags."""
        if format == "json":
            output = json.dumps(self.captured_flags, indent=2)
            filename = self.workspace / f"flags_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        elif format == "txt":
            lines = []
            for flag_id, flag_info in sorted(self.captured_flags.items(), key=lambda x: int(x[0])):
                lines.append(f"[{flag_id}] {flag_info['flag']} ({flag_info.get('challenge', 'N/A')})")
            output = "\n".join(lines)
            filename = self.workspace / f"flags_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        else:
            print(f"[✗] Unsupported format: {format}")
            return None

        try:
            with open(filename, 'w') as f:
                f.write(output)
            print(f"\n[✓] Flags exported to: {filename}\n")
            return str(filename)
        except Exception as e:
            print(f"[✗] Export failed: {e}\n")
            return None

    def _save_progress(self):
        """Save captured flags to database."""
        data = {
            "captured_flags": self.captured_flags,
            "statistics": {
                "total_flags": len(self.captured_flags),
                "submitted": sum(1 for f in self.captured_flags.values() if f.get("submitted")),
                "pending": sum(1 for f in self.captured_flags.values() if not f.get("submitted"))
            }
        }
        self._save_data(data)
