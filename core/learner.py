import json
from pathlib import Path
from core.utils import ensure_dir
from collections import Counter
import time

class Learner:
    def __init__(self, dbpath="./reports/learner_db.json"):
        self.dbpath = Path(dbpath)
        ensure_dir(self.dbpath.parent)
        if not self.dbpath.exists():
            self.dbpath.write_text(json.dumps({
                "history": [],
                "stats": {},
                "patterns": {},
                "favorite_commands": [],
                "learning_level": "beginner"
            }))
        self._load()

    def _load(self):
        try:
            content = self.dbpath.read_text()
            if content.strip():
                self.data = json.loads(content)
            else:
                self.data = {"history": [], "stats": {}, "patterns": {}, "favorite_commands": [], "learning_level": "beginner"}
        except Exception:
            self.data = {"history": [], "stats": {}, "patterns": {}, "favorite_commands": [], "learning_level": "beginner"}
        
        # Ensure all required keys exist
        for key in ["history", "stats", "patterns", "favorite_commands", "learning_level"]:
            if key not in self.data:
                if key == "history":
                    self.data[key] = []
                elif key == "learning_level":
                    self.data[key] = "beginner"
                else:
                    self.data[key] = {}

    def record(self, cmdname, ctx, result=None):
        """Record command execution with context and result"""
        entry = {
            "cmd": cmdname,
            "ctx": ctx,
            "result": result or {},
            "timestamp": time.time()
        }
        self.data["history"].append(entry)
        
        # Track stats per command
        if cmdname not in self.data.get("stats", {}):
            self.data["stats"][cmdname] = {"count": 0, "success": 0, "last_used": None}
        
        self.data["stats"][cmdname]["count"] += 1
        self.data["stats"][cmdname]["last_used"] = time.time()
        
        # Trim history
        self.data["history"] = self.data["history"][-3000:]
        
        # Update learning level
        self._update_learning_level()
        
        self.dbpath.write_text(json.dumps(self.data, indent=2))

    def _update_learning_level(self):
        """Update skill level based on command diversity"""
        total_commands = len(self.data.get("history", []))
        unique_commands = len(set(h["cmd"] for h in self.data.get("history", [])))
        
        if total_commands < 10:
            self.data["learning_level"] = "beginner"
        elif total_commands < 50 and unique_commands >= 5:
            self.data["learning_level"] = "intermediate"
        elif total_commands >= 50 and unique_commands >= 10:
            self.data["learning_level"] = "advanced"
        else:
            self.data["learning_level"] = "expert"

    def get_learning_level(self):
        """Return user's proficiency level"""
        return self.data.get("learning_level", "beginner")

    def get_stats(self):
        """Get command usage statistics"""
        return self.data.get("stats", {})

    def top(self, n=10):
        """Get most frequently used commands"""
        names = [h["cmd"] for h in self.data.get("history", [])]
        return Counter(names).most_common(n)

    def get_patterns(self):
        """Get learned workflow patterns (e.g., 'enum-full' often followed by 'web-vuln-scan')"""
        history = self.data.get("history", [])
        patterns = {}
        
        for i in range(len(history) - 1):
            current = history[i]["cmd"]
            next_cmd = history[i + 1]["cmd"]
            
            if current not in patterns:
                patterns[current] = {}
            if next_cmd not in patterns[current]:
                patterns[current][next_cmd] = 0
            
            patterns[current][next_cmd] += 1
        
        return patterns

    def suggest_next_command(self, current_cmd, n=3):
        """Suggest next commands based on learned patterns"""
        patterns = self.get_patterns()
        
        if current_cmd not in patterns:
            return []
        
        # Get most common following commands
        following = patterns[current_cmd]
        sorted_cmds = sorted(following.items(), key=lambda x: x[1], reverse=True)
        
        return [cmd for cmd, count in sorted_cmds[:n]]

    def get_quick_tips(self):
        """Give tips based on learning level"""
        level = self.get_learning_level()
        
        tips = {
            "beginner": [
                "💡 Try 'help <shortcut>' to learn about any command",
                "💡 Use 'shortcuts' to list all available commands",
                "💡 Start with safe commands (no force=true needed)",
                "💡 Commands run in dry-run mode by default - add force=true to execute"
            ],
            "intermediate": [
                "💡 Check command stats with 'stats' command",
                "💡 Try chaining related commands for faster workflow",
                "💡 Use fuzzy matching - typos are forgiven",
                "💡 Custom shortcuts can be added to shortcuts/*.yaml"
            ],
            "advanced": [
                "💡 Workflow patterns are being learned - use common sequences",
                "💡 Consider creating custom tool adapters in core/",
                "💡 Extend plugins in plugins/ directory",
                "💡 Analyze learner_db.json for detailed workflow insights"
            ],
            "expert": [
                "💡 You're mastering SecShell PRO!",
                "💡 Share your workflow patterns with the community",
                "💡 Consider contributing new security tools",
                "💡 Optimize shortcuts based on your workflow"
            ]
        }
        
        return tips.get(level, tips["beginner"])

