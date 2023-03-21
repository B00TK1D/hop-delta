import time

bssids = {}

timeout_threshold = 120

def log_bssid(bssid):
    global bssids
    if bssid not in bssids:
        bssids[bssid]["first_seen"] = time.time()
        bssids[bssid]["last_seen"] = time.time()
    else:
        bssids[bssid]["last_seen"] = time.time()

def get_wait_time():
    global timeout_threshold, bssids
    now = time.time()
    s = 0
    for bssid in bssids:
        if (now - bssids[bssid]["last_seen"]) > timeout_threshold:
            del bssids[bssid]
        else:
            s += bssids[bssid]["last_seen"] - bssids[bssid]["first_seen"]
    s = s / len(bssids)
    return s