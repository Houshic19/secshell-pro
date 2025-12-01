#!/usr/bin/env python3
import json, argparse, re

p = argparse.ArgumentParser()
p.add_argument("--log", required=True)
p.add_argument("--out")
args = p.parse_args()

pattern = re.compile(r"(Failed password|Accepted password|authentication failure)")
result = []

with open(args.log, 'r', errors='ignore') as f:
    for line in f:
        if pattern.search(line):
            result.append(line.strip())

print(json.dumps({"matches": result}, indent=2))
