import shlex, yaml, os
from datetime import datetime
from pathlib import Path
from core.executor import Executor
from core.advisor import Advisor
from core.learner import Learner
from core.ai_client import AIClient
from core.report_generator import ReportGenerator
from core.ctf_mode import CTFMode
from fuzzywuzzy import process



class CommandDispatcher:
    def __init__(self, shortcuts, cfg):
        # shortcuts: list of dicts
        self.shortcuts = {s['name']: s for s in shortcuts}
        self.cfg = cfg
        self.executor = Executor(cfg)
        self.advisor = Advisor()
        self.learner = Learner(cfg.get("learner_db"))
        self.ai = AIClient(cfg)
        self.report_gen = ReportGenerator(cfg.get("workspace", "./reports"))
        self.ctf = CTFMode(cfg.get("workspace", "./reports"))
        self.names = list(self.shortcuts.keys())

    def suggest_closest(self, name):
        # fuzzy match
        choice, score = process.extractOne(name, self.names)
        if score > 60:
            return choice, score
        return None, 0

    def parse_input(self, text):
        parts = shlex.split(text)
        if not parts:
            return None, {}
        name = parts[0]
        kv = {}
        
        # Special handling for CTF commands
        if name == "ctf" and len(parts) > 1:
            kv["cmd"] = parts[1]
            if len(parts) > 2:
                # For "ctf flag <text>" or "ctf start <id>", capture the rest
                if parts[1] in ["flag", "start", "hint", "status", "leaderboard", "quit"]:
                    kv["value"] = " ".join(parts[2:])
        
        # Standard key=value and positional parsing
        for p in parts[1:]:
            if "=" in p:
                k,v = p.split("=",1)
                kv[k]=v
            elif p not in kv.get("cmd", ""):  # Skip if already parsed as cmd
                # assign to target if not provided
                kv.setdefault("target", p)
        return name, kv

    def handle_input(self, text):
        name, kv = self.parse_input(text)
        if not name:
            return
        if name == "ai":
            prompt = " ".join(kv.get("prompt","").split())
            print(self.ai.ask(prompt))
            return
        if name == "shortcuts":
            for k in self.names:
                print(k, "-", self.shortcuts[k].get("desc",""))
            return
        if name == "stats":
            stats = self.learner.get_stats()
            print("[📊 Command Stats]")
            for cmd, data in sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
                print(f"  {cmd}: {data['count']} uses")
            return
        if name == "tips":
            print("[💡 Learning Tips]")
            for tip in self.learner.get_quick_tips():
                print(tip)
            return
        if name == "level":
            level = self.learner.get_learning_level()
            print(f"[📈 Your Level] {level.upper()}")
            return
        
        # CTF Mode commands (Real CTF Assistance Tool)
        if name == "ctf":
            ctf_cmd = kv.get("cmd", "").strip()
            if not ctf_cmd:
                self.ctf.list_patterns()
                self.ctf.show_statistics()
                return
            
            if ctf_cmd == "list" or ctf_cmd == "patterns":
                self.ctf.list_patterns()
            elif ctf_cmd == "extract":
                output = kv.get("value", kv.get("target", "")).strip()
                challenge = kv.get("challenge", "")
                if not output:
                    print("[✗] Usage: ctf extract <output_text> challenge=<name>")
                else:
                    self.ctf.extract_from_command_output(output, challenge)
            elif ctf_cmd == "capture":
                flag_text = kv.get("value", kv.get("target", "")).strip()
                challenge = kv.get("challenge", "")
                category = kv.get("category", "manual")
                if not flag_text:
                    print("[✗] Usage: ctf capture <flag_text> challenge=<name> category=<type>")
                else:
                    self.ctf.capture_flag(flag_text, challenge, category)
            elif ctf_cmd == "flags":
                submitted_only = kv.get("submitted", "false").lower() == "true"
                self.ctf.list_captured_flags(submitted_only)
            elif ctf_cmd == "mark" or ctf_cmd == "submit":
                flag_id = kv.get("value", kv.get("target", "")).strip()
                if not flag_id:
                    print("[✗] Usage: ctf mark <flag_id>")
                else:
                    self.ctf.mark_submitted(int(flag_id))
            elif ctf_cmd == "stats":
                self.ctf.show_statistics()
            elif ctf_cmd == "export":
                format_type = kv.get("format", "json")
                self.ctf.export_flags(format_type)
            elif ctf_cmd == "add-pattern":
                pattern_id = kv.get("id", "")
                regex = kv.get("regex", "")
                pattern_name = kv.get("name", pattern_id)
                category = kv.get("category", "custom")
                if not pattern_id or not regex:
                    print("[✗] Usage: ctf add-pattern id=<id> regex=<regex> name=<name> category=<cat>")
                else:
                    self.ctf.add_custom_pattern(pattern_id, regex, pattern_name, category)
            else:
                print(f"[✗] Unknown CTF command: {ctf_cmd}")
                print("Available: list, extract, capture, flags, mark, stats, export, add-pattern")
            return
        
        # fuzzy suggestion
        if name not in self.shortcuts:
            cand, score = self.suggest_closest(name)
            if cand:
                print(f"[did you mean] {cand}? (score {score})")
            else:
                print("[unknown]", name)
            return

        sc = self.shortcuts[name]
        ctx = {"workspace": self.cfg.get("workspace","reports")}
        ctx.update(kv)
        try:
            cmd = sc["cmd"].format(**ctx)
        except KeyError as e:
            print("[missing param]", e)
            return

        # safety
        if (not sc.get("safe", True)) and self.cfg.get("require_force_for_unsafe", True) and kv.get("force") != "true":
            print("[unsafe] This shortcut is destructive. Add force=true to parameters to execute.")
            return

        # execute
        print("[exec]", cmd)
        res = self.executor.run(cmd)
        # learning & advisor with enhanced tracking
        self.learner.record(name, ctx, result=res)
        sug = self.advisor.suggest(name, res)
        if sug:
            print("[suggestions]")
            for s in sug:
                print("  -", s)
        
        # Show learned patterns
        next_cmds = self.learner.suggest_next_command(name)
        if next_cmds and self.learner.get_learning_level() != "beginner":
            print("[🧠 Smart Suggestions] Based on your patterns:")
            for i, cmd in enumerate(next_cmds, 1):
                desc = self.shortcuts.get(cmd, {}).get("desc", "")
                print(f"  {i}. {cmd}: {desc}")
        
        # Display output
        if res.get("stdout"):
            print("\n[output]")
            print(res["stdout"][:2000])
            if len(res["stdout"]) > 2000:
                print(f"... ({len(res['stdout']) - 2000} more characters)")
        
        # Ask for report generation
        self.report_gen.ask_generate_report(
            cmd_output=res.get("stdout", ""),
            target=ctx.get("target"),
            metadata={"command": name, "timestamp": datetime.now().isoformat()}
        )
        
        # if AI enabled, ask to summarize
        if self.cfg.get("openai_api_key") or self.cfg.get("use_local_llm"):
            summary_prompt = f"Summarize findings from the following output:\\n{res.get('stdout','')[:4000]}"
            print("[ai-summary]", self.ai.ask(summary_prompt))
        return res

    def show_help(self, name):
        """
        Print detailed help for a shortcut. Provides fuzzy suggestions if not found.
        """
        sc = self.shortcuts.get(name)
        if sc:
            print(f"\nShortcut: {name}")
            print(f"  Description : {sc.get('desc','(no description)')}")
            print(f"  Command     : {sc.get('cmd')}")
            print(f"  Safe        : {sc.get('safe', True)}")
            if sc.get('tags'):
                print(f"  Tags        : {', '.join(sc.get('tags'))}")
            if sc.get('notes'):
                print(f"  Notes       : {sc.get('notes')}")
            print("")  # newline
            return

        # fuzzy fallback
        try:
            cand, score = process.extractOne(name, list(self.shortcuts.keys()))
            if score and score >= 60:
                print(f"[did you mean] {cand} (score {score}) — run `help {cand}` for details")
            else:
                print(f"[unknown shortcut] {name}")
        except Exception:
            print(f"[unknown shortcut] {name}")

    def info(self, name):
        return self.show_help(name)

