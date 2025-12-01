from pathlib import Path
from rich import print

def render_banner():
    root = Path(__file__).resolve().parents[1]
    b = root / "assets" / "banner.txt"
    if b.exists():
        print(b.read_text())
    else:
        print("SecShell PRO")
