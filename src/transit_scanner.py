import os
import time
import threading
from collections import defaultdict
import flask


class TransitScanner:

    shared_bssids = defaultdict(lambda: defaultdict(dict))

    def __init__(self, scanner_id, distance):
        self.scanner_id = scanner_id
        self.distance = distance
        self.timeout_threshold = 120
        self.exploit_thread = None

    def clear_log(self):
        self.bssid_dict.clear()

    def log_bssid(self, bssid, first_seen, last_seen):
        self.shared_bssids[self.scanner_id][bssid] = {
            "first_seen": first_seen, "last_seen": last_seen}

    @classmethod
    def calculate_average_overlap_time(cls, scanner1_id, scanner2_id, bssids):
        overlap_times = []
        for bssid in bssids:
            if bssid in cls.shared_bssids[scanner1_id] and bssid in cls.shared_bssids[scanner2_id]:
                start_overlap = max(
                    cls.shared_bssids[scanner1_id][bssid]["first_seen"],
                    cls.shared_bssids[scanner2_id][bssid]["first_seen"]
                )
                end_overlap = min(
                    cls.shared_bssids[scanner1_id][bssid]["last_seen"],
                    cls.shared_bssids[scanner2_id][bssid]["last_seen"]
                )
                overlap_time = max(end_overlap - start_overlap, 0)
                overlap_times.append(overlap_time)

        if overlap_times:
            average_overlap_time = sum(overlap_times) / len(overlap_times)
            return average_overlap_time
        else:
            return 0

    @classmethod
    def calculate_average_speed(cls, distance, average_overlap_time):
        if average_overlap_time > 0:
            return distance / average_overlap_time
        else:
            return None

    @classmethod
    def transit_time_dashboard(self, scanner1_id, scanner2_id, bssids):
        average_overlap_time = self.calculate_average_overlap_time(
            scanner1_id, scanner2_id, bssids)
        average_speed = self.calculate_average_speed(
            self.distance, average_overlap_time)

        transit_time_str = f"{average_overlap_time:.2f} seconds"
        speed_str = "N/A" if average_speed is None else f"{average_speed:.2f} units/second"

        return render_template("transit-time.html", transit_time=transit_time_str, speed=speed_str)
