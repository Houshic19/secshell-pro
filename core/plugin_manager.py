import yaml
import json
from pathlib import Path
from core.utils import ensure_dir

class PluginManager:
    """Manage custom shortcuts and tools via plugins"""
    
    def __init__(self, plugins_dir="./plugins", shortcuts_dir="./shortcuts"):
        self.plugins_dir = Path(plugins_dir)
        self.shortcuts_dir = Path(shortcuts_dir)
        ensure_dir(self.plugins_dir)
        ensure_dir(self.shortcuts_dir)
    
    def create_shortcut_template(self, category="custom", name="example", cmd="echo hello", desc="Example shortcut"):
        """Generate a shortcut template YAML for custom tools"""
        template = {
            "shortcuts": [
                {
                    "name": name,
                    "cmd": cmd,
                    "desc": desc,
                    "safe": True,
                    "category": category
                }
            ]
        }
        return yaml.dump(template, default_flow_style=False)
    
    def create_custom_shortcut(self, name, cmd, desc, category="custom", safe=True):
        """Create and save a new custom shortcut"""
        shortcut = {
            "shortcuts": [
                {
                    "name": name,
                    "cmd": cmd,
                    "desc": desc,
                    "safe": safe,
                    "category": category
                }
            ]
        }
        
        # Save to custom shortcuts file
        custom_file = self.shortcuts_dir / f"{category}.yaml"
        
        # If file exists, load it and append
        if custom_file.exists():
            existing = yaml.safe_load(custom_file.read_text()) or {}
            existing_shortcuts = existing.get("shortcuts", [])
            # Check if shortcut already exists
            existing_shortcuts = [s for s in existing_shortcuts if s.get("name") != name]
            existing_shortcuts.append(shortcut["shortcuts"][0])
            shortcut["shortcuts"] = existing_shortcuts
        
        custom_file.write_text(yaml.dump(shortcut, default_flow_style=False))
        print(f"Created shortcut '{name}' in {category}.yaml")
        return True
    
    def list_shortcuts(self):
        """List all shortcuts by category"""
        shortcuts = {}
        for yaml_file in self.shortcuts_dir.glob("*.yaml"):
            category = yaml_file.stem
            try:
                data = yaml.safe_load(yaml_file.read_text())
                # Handle both list and dict formats
                if isinstance(data, list):
                    shortcuts[category] = data
                elif isinstance(data, dict) and "shortcuts" in data:
                    shortcuts[category] = data.get("shortcuts", [])
                else:
                    shortcuts[category] = []
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
        return shortcuts
    
    def create_tool_adapter_template(self, tool_name, tool_command):
        """Generate a template for creating a custom tool adapter"""
        template = f'''"""
Custom adapter for {tool_name}
"""
from core.adapter_base import AdapterBase

class {tool_name.capitalize()}Adapter(AdapterBase):
    def __init__(self, executor):
        super().__init__(executor)
        self.tool = "{tool_name}"
    
    def run(self, target, **kwargs):
        """
        Run {tool_name} against target
        
        Args:
            target: Target host/domain
            **kwargs: Additional parameters
        
        Returns:
            dict with 'stdout', 'stderr', 'code'
        """
        cmd = "{tool_command}" + f" {{target}}"
        return self.executor.run(cmd)
    
    def parse_output(self, output):
        """Parse and structure tool output"""
        return {{"raw": output}}
    
    def get_description(self):
        return "{tool_name} - Custom tool adapter"
'''
        return template
    
    def export_shortcuts(self, filepath):
        """Export all shortcuts to a JSON file for backup/sharing"""
        shortcuts = self.list_shortcuts()
        filepath = Path(filepath)
        filepath.write_text(json.dumps(shortcuts, indent=2))
        print(f"Exported shortcuts to {filepath}")
    
    def import_shortcuts(self, filepath):
        """Import shortcuts from a JSON file"""
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"File not found: {filepath}")
            return False
        
        data = json.loads(filepath.read_text())
        
        for category, shortcuts in data.items():
            yaml_file = self.shortcuts_dir / f"{category}.yaml"
            yaml_file.write_text(yaml.dump(
                {"shortcuts": shortcuts},
                default_flow_style=False
            ))
        
        print(f"Imported {len(data)} shortcut categories")
        return True
    
    def validate_shortcut(self, shortcut):
        """Validate shortcut structure"""
        required_fields = ["name", "cmd", "desc"]
        for field in required_fields:
            if field not in shortcut:
                return False, f"Missing required field: {field}"
        
        if not isinstance(shortcut.get("safe", True), bool):
            return False, "Field 'safe' must be boolean"
        
        return True, "Valid"
    
    def get_plugin_suggestions(self):
        """Get suggestions for plugins based on installed tools"""
        suggestions = {
            "exploit_frameworks": [
                {"name": "metasploit", "desc": "Metasploit Framework integration"},
                {"name": "burp", "desc": "Burp Suite CLI integration"},
            ],
            "passive_recon": [
                {"name": "shodan", "desc": "Shodan API integration"},
                {"name": "censys", "desc": "Censys API integration"},
            ],
            "reporting": [
                {"name": "html_report", "desc": "Generate HTML reports"},
                {"name": "pdf_export", "desc": "Export findings to PDF"},
            ],
            "automation": [
                {"name": "scheduled_scans", "desc": "Schedule recurring scans"},
                {"name": "webhook_alerts", "desc": "Send alerts via webhooks"},
            ]
        }
        return suggestions
