import subprocess
from pathlib import Path
from core.adapter_base import ToolAdapter

class HydraAdapter(ToolAdapter):
    def run(self, target, userlist, passlist, proto="ssh", outdir="reports", extra_args=""):
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        outfile = outdir / f"{target}_hydra.txt"
        cmd = f"hydra -L {userlist} -P {passlist} -o {outfile} {proto}://{target} {extra_args}"
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "artifacts": [str(outfile)]}

    def parse_output(self, path):
        # naive parse
        try:
            with open(path) as f:
                return {"lines": f.read().splitlines()}
        except Exception:
            return {}
