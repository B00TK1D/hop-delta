import time

bssids = {}

timeout_threshold = 120

def clear_log():
    global bssids
    bssids = {}

def log_bssid(bssid, first_seen, last_seen):
    global bssids
    bssids[bssid] = {"first_seen": first_seen, "last_seen": last_seen}

def get_wait_time():
    global timeout_threshold, bssids
    now = time.time()
    s = 0
    for bssid in bssids:
        if (now - bssids[bssid]["last_seen"]) > timeout_threshold:
            del bssids[bssid]
        else:
            s += bssids[bssid]["last_seen"] - bssids[bssid]["first_seen"]
    s = s / max(len(bssids), 1)
    return s