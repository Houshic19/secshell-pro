import subprocess
from pathlib import Path
from core.adapter_base import ToolAdapter

class GobusterAdapter(ToolAdapter):
    def run(self, target, wordlist="/usr/share/wordlists/dirb/common.txt", outdir="reports"):
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        outfile = outdir / f"{target}_gobuster.txt"
        cmd = f"gobuster dir -u https://{target} -w {wordlist} -o {outfile} -q"
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "artifacts": [str(outfile)]}

    def parse_output(self, path):
        try:
            with open(path) as f:
                lines = f.read().splitlines()
            return {"entries": lines}
        except Exception:
            return {}
