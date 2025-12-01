import subprocess, shlex, os
from pathlib import Path
from core.utils import ensure_dir
import threading, time

class Executor:
    def __init__(self, cfg):
        self.cfg = cfg
        self.workspace = Path(cfg.get("workspace", "./reports"))
        ensure_dir(self.workspace)

    def run(self, cmd, timeout=None, capture=True):
        timeout = timeout or self.cfg.get("default_timeout", 180)
        if self.cfg.get("default_dry_run", True):
            print("[dry-run] command not executed:", cmd)
            return {"returncode": 0, "stdout": "", "stderr": "", "artifacts": []}

        try:
            p = subprocess.run(cmd, shell=True, capture_output=capture, text=True, timeout=timeout)
            artifacts = self._collect_artifacts()
            return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "artifacts": artifacts}
        except subprocess.TimeoutExpired:
            return {"returncode": -1, "stdout": "", "stderr": "timeout", "artifacts": []}
        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e), "artifacts": []}

    def _collect_artifacts(self):
        # return recent files in workspace
        items = []
        for p in self.workspace.glob("**/*"):
            if p.is_file():
                items.append(str(p))
        return items
