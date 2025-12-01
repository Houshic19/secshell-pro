#!/usr/bin/env python3
import subprocess, argparse, json

p = argparse.ArgumentParser()
p.add_argument('--domain', required=True)
p.add_argument('--out')
args = p.parse_args()

whois = subprocess.run(["whois", args.domain], capture_output=True, text=True).stdout

print(json.dumps({"domain": args.domain, "whois": whois[:2000]}, indent=2))
