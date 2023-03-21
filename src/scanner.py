import os
import time
import threading

import db

exploit_thread = None

def scan_loop():
    while True:
        db.clear_log()
        try:
            with open("bssid-log.csv", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("BSSID"):
                        continue
                    bssid = line.split(",")[0]
                    first_seen_str = line.split(",")[1]
                    last_seen_str = line.split(",")[2]
                    # Convert first seen and last seen from strings to time epochs
                    first_seen = time.mktime(time.strptime(first_seen_str, "%Y-%m-%d %H:%M:%S"))
                    last_seen = time.mktime(time.strptime(last_seen_str, "%Y-%m-%d %H:%M:%S"))
                    db.log_bssid(bssid, first_seen, last_seen)
        except:
            pass
        time.sleep(1)
    pass


def init():
    global exploit_thread
    # Place the interface into monitor mode
    os.system("sudo airmon-ng start wlp0s20f3")
    os.system("sudo nohup sudo airodump-ng -w bssid-log.csv --output-format csv wlp0s20f3mon &")
    exploit_thread = threading.Thread(target=scan_loop)
    exploit_thread.start()
    pass
