# rule-based advisor - extend rules easily
class Advisor:
    def __init__(self):
        # tool name -> rule fn
        self.rules = {
            "enum-full": self.rule_enum_full,
            "enum-web": self.rule_enum_web,
        }

    def suggest(self, executed_name, result):
        fn = self.rules.get(executed_name)
        try:
            if fn:
                return fn(result)
        except Exception:
            pass
        return []

    def rule_enum_full(self, res):
        out = (res.get("stdout") or "") + (res.get("stderr") or "")
        suggestions = []
        if "3306" in out or "mysql" in out.lower():
            suggestions.append("Detected MySQL. Try: enum-db target=<host>")
        if "80/tcp" in out or "443/tcp" in out or "http" in out.lower():
            suggestions.append("Detected web ports. Try: enum-web target=<host>")
        if "22/tcp" in out:
            suggestions.append("SSH detected. Check for weak credentials or unusual banners.")
        return suggestions

    def rule_enum_web(self, res):
        suggestions = []
        # parse gobuster artifacts
        if res.get("artifacts"):
            for a in res["artifacts"]:
                if "gobuster" in a:
                    suggestions.append("Found directories via gobuster → inspect {artifact}".format(artifact=a))
        return suggestions
