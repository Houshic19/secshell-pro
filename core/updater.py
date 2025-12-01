import requests
import os
from pathlib import Path
from core.utils import ensure_dir
import json

class Updater:
    def __init__(self, cfg):
        self.feed = cfg.get("auto_update_feed")
        self.shortcuts_dir = Path(cfg.get("shortcuts_dir", "./shortcuts"))
        self.allow = cfg.get("allow_auto_update", False)
        ensure_dir(self.shortcuts_dir)

    def fetch_feed(self):
        if not self.feed:
            return None
        try:
            r = requests.get(self.feed, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print("[updater.fetch_error]", e)
            return None

    def check_once(self):
        if not self.allow:
            print("[updater] auto update disabled")
            return
        feed = self.fetch_feed()
        if not feed:
            return
        for item in feed.get("shortcuts", []):
            url = item.get("url")
            target = self.shortcuts_dir / item.get("target_path", item.get("name", "remote.yaml"))
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(r.text)
                print("[updater] updated", target)
            except Exception as e:
                print("[updater.item_error]", e)
