from pymongo import MongoClient
from datetime import datetime, timedelta

class OnelinerBBS:
    def __init__(self, util):
        self.mongo_client = util.mongo_client
        self.db = self.mongo_client["bbs"]
        self.collection = self.db["oneliners"]
        self.sid_data = util.sid_data
        self.goto_next_line = util.goto_next_line
        self.output = util.output
        self.askYesNo = util.askYesNo
        self.ask = util.ask
        self.launchMenuCallback = util.launchMenuCallback
        self.wait = util.wait
        self.util = util

    def show_oneliners(self):
        self.util.clear_screen()
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = 0
        self.output_oneliners()

        self.goto_next_line()
        self.askYesNo("Do you want to add a new oneliner?", self.oneliner_callback)

    def oneliner_callback(self, result):
        if result.lower() == 'y':
            self.goto_next_line()
            self.ask(35, self.creation_callback)
        else:
            self.launchMenuCallback()

    def creation_callback(self, result):
        if result:
            self.goto_next_line()
            current_time = datetime.utcnow()
            self.collection.insert_one({"text": result, "timestamp": current_time, "username" : self.sid_data.user_name, "chosen_bbs" : self.sid_data.chosen_bbs})
            self.output_oneliners()
            self.goto_next_line()
            self.output("Press any button to continue", 3, 0)
            self.wait(self.launchMenuCallback)

    def output_oneliners(self):
        current_time = datetime.utcnow()
        cursor = self.collection.find({"chosen_bbs" : self.sid_data.chosen_bbs}).sort("timestamp", -1).limit(25)
        counter = 1
        for document in reversed(list(cursor)):
            
            # Check if 'timestamp' is a datetime object
            if not isinstance(document['timestamp'], datetime):
                raise TypeError("Timestamp is not a datetime object")
            
            time_diff = self.humanize_date_difference(current_time, otherdate=document['timestamp'])
            self.util.output_wrap(f"({counter}) {document['username']}: {document['text']} - {time_diff}", 3, 0)
            self.goto_next_line()
            counter += 1

    def humanize_date_difference(self, now, otherdate=None, offset=None):
        if otherdate is not None:
            dt = now - otherdate
            offset = dt.total_seconds()
        if offset is not None and offset > 0:
            delta_s = int(offset) % 60
            delta_m = int(offset // 60) % 60
            delta_h = int(offset // 3600) % 24
            delta_d = int(offset // 86400)
        else:
            raise ValueError("Must supply otherdate or offset (from now)")

        if delta_d > 1:
            if delta_d > 6:
                date = now + timedelta(days=-delta_d, hours=-delta_h, minutes=-delta_m)
                return date.strftime('%A, %Y %B %m, %H:%I')
            else:
                wday = now + timedelta(days=-delta_d)
                return wday.strftime('%A')
        if delta_d == 1:
            return "Yesterday"
        if delta_h > 0:
            return "%dh%dm ago" % (delta_h, delta_m)
        if delta_m > 0:
            return "%dm ago" % delta_m  # Changed here to show only minutes if 0 hours
        else:
            return "%ds ago" % delta_s



