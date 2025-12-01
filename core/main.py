#!/usr/bin/env python3
import yaml, sys, os
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich import print as rprint
from core.ui import render_banner
from core.plugin_loader import PluginLoader
from core.updater import Updater
from core.dispatcher import CommandDispatcher

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "configs" / "config.yaml"

def load_config():
    with open(CFG_PATH) as f:
        return yaml.safe_load(f)

def load_shortcuts(path):
    import glob, yaml
    items = []
    for p in Path(path).glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text())
            # YAML may be a list of shortcut dicts, or a dict containing a 'shortcuts' key.
            if isinstance(data, list):
                items.extend(data)
            elif isinstance(data, dict) and "shortcuts" in data:
                sc = data.get("shortcuts") or []
                if isinstance(sc, list):
                    items.extend(sc)
            # if it's a dict mapping names to definitions, attempt to convert
            elif isinstance(data, dict):
                # convert mapping {name: {cmd:..., desc:...}} -> list of dicts
                for k, v in data.items():
                    if isinstance(v, dict):
                        v.setdefault("name", k)
                        items.append(v)
        except Exception:
            pass
    return items

def main():
    cfg = load_config()
    Path(cfg.get("workspace","reports")).mkdir(parents=True, exist_ok=True)
    render_banner()
    pl = PluginLoader(cfg.get("plugins_dir", "./plugins"))
    pl.load_plugins()
    Updater(cfg).check_once()
    shortcuts = load_shortcuts(cfg.get("shortcuts_dir","./shortcuts"))
    names = [s["name"] for s in shortcuts]
    completer = WordCompleter(names + ["help","exit","shortcuts","ai","stats","tips","level","tools"], ignore_case=True)
    dispatcher = CommandDispatcher(shortcuts, cfg)
    session = PromptSession()

    dry_run_status = "ON" if cfg.get("default_dry_run", True) else "OFF"
    rprint(f"[bold green]SecShell PRO[/bold green] — type 'help' for commands. Dry-run {dry_run_status}.")
    rprint(f"[dim]📊 Learning Level: {dispatcher.learner.get_learning_level().upper()}[/dim]")
    
    # Check if input is from a terminal
    is_interactive = sys.stdin.isatty()
    
    if is_interactive:
        session = PromptSession()
    
    while True:
        try:
            if is_interactive:
                text = session.prompt("SecShell> ", completer=completer)
            else:
                # Read from stdin in non-interactive mode
                try:
                    text = input("SecShell> ")
                except EOFError:
                    rprint("Exiting SecShell PRO")
                    break
        except (KeyboardInterrupt, EOFError):
            rprint("Exiting SecShell PRO")
            break
        text = (text or "").strip()
        if not text:
            continue
        if text in ("exit","quit"):
            break
        
        # Handle tool management commands
        if text.startswith("tools"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                print("[tools] Available commands: tools list, tools check <name>, tools install <name>, tools info <name>")
            else:
                subcommand = parts[1].strip().split()[0] if parts[1].strip() else None
                if subcommand == "list":
                    from core.tool_installer import ToolInstaller
                    ti = ToolInstaller()
                    print("[🔧 Available Tools]")
                    for name, desc in ti.get_available_tools().items():
                        installed, _ = ti.check_tool(name)
                        status = "✓" if installed else "✗"
                        print(f"  {status} {name}: {desc}")
                elif subcommand == "check":
                    tool_name = text.split(maxsplit=2)[2] if len(text.split(maxsplit=2)) > 2 else None
                    if tool_name:
                        from core.tool_installer import ToolInstaller
                        ti = ToolInstaller()
                        is_ok, msg = ti.check_tool(tool_name)
                        status = "✓" if is_ok else "✗"
                        print(f"[{status}] {tool_name}: {msg}")
                elif subcommand == "install":
                    tool_name = text.split(maxsplit=2)[2] if len(text.split(maxsplit=2)) > 2 else None
                    if tool_name:
                        from core.tool_installer import ToolInstaller
                        ti = ToolInstaller()
                        print(f"Installing {tool_name}...")
                        success, msg = ti.install_tool(tool_name, "apt")
                        print(msg)
                elif subcommand == "info":
                    tool_name = text.split(maxsplit=2)[2] if len(text.split(maxsplit=2)) > 2 else None
                    if tool_name:
                        from core.tool_installer import ToolInstaller
                        ti = ToolInstaller()
                        info = ti.get_tool_info(tool_name)
                        if info:
                            print(f"[ℹ️  {info['name']}]")
                            print(f"  Description: {info['description']}")
                            print(f"  Status: {'✓ Installed' if info['installed'] else '✗ Not installed'}")
                            print(f"  Install methods: {', '.join(info['install_methods'])}")
                        else:
                            print(f"[error] Tool '{tool_name}' not found")
            continue
        
        if text.startswith("help"):
            parts = text.split(maxsplit=1)
            if len(parts) == 1 or not parts[1].strip():
                rprint("[bold cyan]SecShell PRO Commands[/bold cyan]")
                rprint("  shortcuts       - List all available shortcuts")
                rprint("  stats           - Show command statistics")
                rprint("  tips            - Get personalized learning tips")
                rprint("  level           - Show your skill level")
                rprint("  tools [list|check|install|info] - Manage security tools")
                rprint("  ctf [extract|capture|flags|mark|stats|export] - Real CTF assistance")
                rprint("  ai prompt=<text> - Ask AI for security advice")
                rprint("  help <shortcut> - Get detailed help for a shortcut")
                rprint("  exit/quit       - Exit SecShell")
            else:
                # ask dispatcher to show detailed help for a shortcut
                shortcut_name = parts[1].strip()
                try:
                    dispatcher.show_help(shortcut_name)
                except Exception as e:
                    rprint(f"[help.error] {e}")
            continue
        # dispatch regular commands
        dispatcher.handle_input(text)



if __name__ == "__main__":
    main()
