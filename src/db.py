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
    bssidstmp = bssids.copy()
    for bssid in bssidstmp:
        if (now - bssidstmp[bssid]["last_seen"]) > timeout_threshold:
            del bssids[bssid]
        else:
            s += bssidstmp[bssid]["last_seen"] - bssidstmp[bssid]["first_seen"]
    s = s / max(len(bssids), 1)
    return s

def get_factors():
    global bssids
    bssidstmp = bssids.copy()
    factors = []
    for bssid in bssidstmp:
        factors.append({"bssid": bssid, "time": int(bssidstmp[bssid]["last_seen"] - bssidstmp[bssid]["first_seen"])})
    factors = sorted(factors, key=lambda d: d["time"])
    return factors