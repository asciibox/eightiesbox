from pymongo import MongoClient
from datetime import datetime

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
            self.ask(40, self.creation_callback)
        else:
            self.launchMenuCallback()

    def creation_callback(self, result):
        if result:
            self.goto_next_line()
            current_time = datetime.utcnow()
            self.collection.insert_one({"text": result, "timestamp": current_time})
            self.output_oneliners()
            self.goto_next_line()
            self.output("Press any button to continue", 3, 0)
            self.wait(self.launchMenuCallback)

    def output_oneliners(self):
        cursor = self.collection.find({}).sort("timestamp", -1).limit(25)
        counter = 1
        for document in reversed(list(cursor)):
            self.output(f"{counter}: {document['text']}", 3, 0)
            self.goto_next_line()
            counter += 1

