import subprocess
from pathlib import Path
from utils.logger import log

def run_gobuster(target, wordlist='/usr/share/wordlists/dirb/common.txt', outdir='reports'):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    outfile = out / f"{target}_gobuster.txt"
    cmd = f"gobuster dir -u https://{target} -w {wordlist} -o {outfile}"
    log("gobuster.run", cmd)
    return subprocess.run(cmd, shell=True).returncode
