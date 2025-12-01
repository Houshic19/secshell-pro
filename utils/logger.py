from datetime import datetime
import json, os

LOGFILE = './reports/secshell.log'

def setup_logger():
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

def log(key, msg):
    setup_logger()
    entry = {
        'ts': datetime.utcnow().isoformat(),
        'key': key,
        'msg': str(msg)
    }
    with open(LOGFILE, 'a') as f:
        f.write(json.dumps(entry) + "\n")
