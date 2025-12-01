import subprocess
from pathlib import Path
from core.adapter_base import ToolAdapter
import xml.etree.ElementTree as ET

class NmapAdapter(ToolAdapter):
    def __init__(self):
        pass

    def run(self, target, args='-sC -sV -p- --min-rate 500', outdir='reports'):
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        base = outdir / f"{target}_nmap"
        cmd = f"nmap {args} -oA {base} {target}"
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "returncode": p.returncode,
            "stdout": p.stdout,
            "stderr": p.stderr,
            "artifacts": [str(base)+ext for ext in [".nmap", ".xml", ".gnmap"] if (base.parent/(base.name+ext)).exists()]
        }

    def parse_output(self, xmlpath):
        if not Path(xmlpath).exists():
            return {}
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        hosts = []
        for host in root.findall("host"):
            addr_elem = host.find("address")
            addr = addr_elem.get("addr") if addr_elem is not None else ""
            ports = []
            for p in host.findall(".//port"):
                portid = p.get("portid")
                state = p.find("state").get("state") if p.find("state") is not None else ""
                svc = p.find("service")
                svcname = svc.get("name") if svc is not None else ""
                ports.append({"port": portid, "state": state, "service": svcname})
            hosts.append({"addr": addr, "ports": ports})
        return {"hosts": hosts}
