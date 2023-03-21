import os
import time
import threading

import db

exploit_thread = None

def scan_loop():
    while True:
        with open("bssid-log.csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("BSSID"):
                    continue
                bssid = line.split(",")[0]
                db.log_bssid(bssid)
        # Clear the file
        with open("bssid-log.csv", "w") as f:
            f.write("")
        time.sleep(1)
    pass


def init():
    global exploit_thread
    os.system("nohup airodump-ng -w bssid-log.csv --output-format csv mon0 &")
    exploit_thread = threading.Thread(target=scan_loop)
    exploit_thread.start()
    pass
