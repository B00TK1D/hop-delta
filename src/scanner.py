import os
import time
from datetime import datetime
import threading

import db

exploit_thread = None

def scan_loop():
    while True:
        db.clear_log()
        try:
            os.system("sudo cp logs/bssid-01.csv logs/bssid-01.csv.tmp > /dev/null 2>&1")
            with open("logs/bssid-01.csv.tmp", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("BSSID"):
                        continue
                    if line.startswith("Station"):
                        break
                    try:
                        bssid = line.split(",")[0]
                        first_seen_str = line.split(",")[1]
                        last_seen_str = line.split(",")[2]
                        # Convert first seen and last seen from strings to time epochs
                        # 2023-03-21 11:37:30
                        first_seen = datetime.strptime(first_seen_str, " %Y-%m-%d %H:%M:%S").timestamp()
                        last_seen = datetime.strptime(last_seen_str, " %Y-%m-%d %H:%M:%S").timestamp()
                        #print(bssid, first_seen_str, last_seen_str)
                        if first_seen != last_seen:
                            db.log_bssid(bssid, first_seen, last_seen)
                    except Exception as e:
                        #print(e)
                        pass
        except Exception as e:
            print(e)
        time.sleep(2)

def reset():
    os.system("rm -rf logs > /dev/null 2>&1")
    os.system("mkdir logs > /dev/null 2>&1")

def init():
    global exploit_thread
    # Place the interface into monitor mode
    os.system("rm -rf logs > /dev/null 2>&1")
    os.system("mkdir logs > /dev/null 2>&1")
    os.system("sudo airmon-ng start wlp0s20f3 > /dev/null 2>&1")
    exploit_thread = threading.Thread(target=scan_loop)
    exploit_thread.start()
    os.system("sudo sudo airodump-ng --write logs/bssid --output-format csv wlp0s20f3mon & > /dev/null 2>&1")
    pass