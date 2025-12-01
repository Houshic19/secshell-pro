# small utilities used by multiple modules
import os, json, time
from pathlib import Path

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def save_json(path, obj):
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None
