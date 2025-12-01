#!/usr/bin/env python3
import hashlib, argparse, json

def sha256sum(file):
    h = hashlib.sha256()
    with open(file,'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

p = argparse.ArgumentParser()
p.add_argument('--file', required=True)
p.add_argument('--out')
args = p.parse_args()

res = {"file": args.file, "sha256": sha256sum(args.file)}
print(json.dumps(res, indent=2))
