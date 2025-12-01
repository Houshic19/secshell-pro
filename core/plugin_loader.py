import importlib.util
from pathlib import Path
from core.utils import ensure_dir

class PluginLoader:
    def __init__(self, plugins_dir="./plugins"):
        self.plugins_dir = Path(plugins_dir)
        ensure_dir(self.plugins_dir)

    def load_plugins(self):
        loaded = []
        for f in self.plugins_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(f.stem, f)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                loaded.append(f.name)
            except Exception as e:
                print(f"[plugin.error] {f.name}: {e}")
        return loaded
