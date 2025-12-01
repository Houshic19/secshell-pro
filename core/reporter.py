from pathlib import Path
from datetime import datetime

def generate_markdown(target, findings, workspace="reports"):
    Path(workspace).mkdir(parents=True, exist_ok=True)
    now = datetime.utcnow().isoformat()
    md = [f"# Scan report — {target}", f"Generated: {now}", ""]
    for k,v in findings.items():
        md.append(f"## {k}")
        md.append("```json")
        import json
        md.append(json.dumps(v, indent=2)[:5000])
        md.append("```")
    out = Path(workspace) / f"{target}_report.md"
    out.write_text("\n".join(md))
    return str(out)
