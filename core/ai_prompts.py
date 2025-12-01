"""
core/ai_prompts.py

Curated prompt templates and small helper functions to produce
consistent, resume-friendly pentest summaries and remediation guidance.

This module is AI-backend-agnostic. Use with core.ai_client.AIClient.ask(prompt).
"""

from textwrap import dedent
from typing import Dict, Any

# ---------- Prompts (templates) ----------

def prompt_scan_summary(target: str, findings: Dict[str, Any], max_chars=3000) -> str:
    """
    Build prompt asking AI to produce a concise, recruiter-friendly summary of scan findings.
    'findings' is a dict (e.g., parsed nmap/gobuster outputs).
    Return the full prompt string to send to an LLM.
    """
    findings_text = _summarize_findings_text(findings, max_chars=max_chars)
    p = dedent(f"""
    You are a professional cybersecurity analyst. Produce a concise technical summary (max 250 words)
    for the target: {target}.

    Include:
    1) short summary of high-level findings
    2) severity classification (Low/Medium/High/Critical) for each finding
    3) actionable remediation steps (clear, prioritized, numbered)
    4) list of artifacts produced (filenames)

    Findings (raw):
    {findings_text}

    Output format:
    - Provide a short TITLE line
    - Then a 'Findings' section with bullet points and severity
    - Then a 'Remediation' section with numbered steps
    - Then an 'Artifacts' section with filenames

    Keep the writing direct and technical; avoid storytelling. Use simple sentences.
    """)
    return p.strip()

def prompt_exploit_plan(target: str, finding: str) -> str:
    """
    Template to ask for a safe, non-malicious explanation of the impact and an exploitation plan
    described *theoretically* for educational purposes, without programming exploit code.
    """
    p = dedent(f"""
    You are an offensive-security educator. For the following target and finding, provide:
      - A short explanation of the impact (what an attacker could achieve)
      - A high-level step-by-step plan for a penetration tester to validate the finding (no exploit code, no destructive steps)
      - Safe checks the tester should perform to avoid damage
      - Recommended mitigations and detection rules

    Target: {target}
    Finding: {finding}

    Use numbered steps and keep it safe and professional.
    """)
    return p.strip()

def prompt_remediation_snippets(vuln_name: str, context: str="") -> str:
    """
    Provide concise remediation code/config snippets, e.g., secure config values, sample audit rules.
    Keep short and specific.
    """
    p = dedent(f"""
    You are a senior security engineer. Provide concise, copy-paste remediation suggestions for:
    Vulnerability: {vuln_name}
    Context: {context}

    Output:
    - One-line description of fix
    - Concrete configuration/snippet examples (<= 60 lines total)
    - Detection rule suggestion (SIEM/regex or audit approach)
    """)
    return p.strip()

# ---------- Small helpers ----------

def _summarize_findings_text(findings: Dict[str, Any], max_chars=3000) -> str:
    """
    Convert structured findings into a plain text blob for prompt consumption.
    Limits size to max_chars.
    """
    parts = []
    for k, v in findings.items():
        try:
            # simple formatting: key -> first-level summary
            if isinstance(v, dict):
                parts.append(f"{k}: " + ", ".join(f"{kk}={vv}" for kk, vv in list(v.items())[:5]))
            elif isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], dict):
                    # pull some keys
                    sample = []
                    for item in v[:5]:
                        sample.append(", ".join(f"{ik}:{iv}" for ik, iv in list(item.items())[:3]))
                    parts.append(f"{k}: " + " | ".join(sample))
                else:
                    parts.append(f"{k}: " + ", ".join(map(str, v[:20])))
            else:
                parts.append(f"{k}: {str(v)[:200]}")
        except Exception:
            parts.append(f"{k}: <unparseable>")
    joined = "\n".join(parts)
    if len(joined) > max_chars:
        return joined[:max_chars] + "\n...[truncated]"
    return joined

# ---------- Example usage helpers ----------

def build_scan_summary_prompt(target: str, parsed_results: Dict[str, Any]) -> str:
    """Convenience wrapper to build a summary prompt ready for AIClient.ask()"""
    return prompt_scan_summary(target, parsed_results)

def build_remediation_prompt(vuln_name: str, context: str="") -> str:
    return prompt_remediation_snippets(vuln_name, context)
