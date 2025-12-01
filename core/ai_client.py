# Optional AI wrapper supporting OpenAI and local LLM
# To enable: add your OpenAI API key to configs/config.yaml

import os, subprocess, json, time

class AIClient:
    def __init__(self, cfg):
        self.openai_key = cfg.get("openai_api_key", "")
        self.use_local = cfg.get("use_local_llm", False)
        self.local_cmd = cfg.get("local_llm_cmd", "")

    def ask_openai(self, prompt, model="gpt-4o-mini"):
        """Query OpenAI API if key is configured"""
        if not self.openai_key:
            return "[ai.disabled] OpenAI API key not configured"
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"user","content":prompt}],
                max_tokens=400,
                temperature=0.2
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[ai.error] {str(e)[:100]}"

    def ask_local(self, prompt):
        """Use local LLM command if configured"""
        if not self.local_cmd:
            return "[ai.error] local command not configured"
        try:
            p = subprocess.run(f"{self.local_cmd} {json.dumps(prompt)}", shell=True, capture_output=True, text=True, timeout=60)
            return p.stdout or p.stderr
        except Exception as e:
            return f"[ai.error] {e}"

    def ask(self, prompt):
        """Ask AI backend (OpenAI or local LLM)"""
        if self.openai_key:
            return self.ask_openai(prompt)
        elif self.use_local:
            return self.ask_local(prompt)
        else:
            return "[ai.disabled] no AI backend configured. To enable: add openai_api_key to configs/config.yaml"
