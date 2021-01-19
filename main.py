#!/usr/bin/python3 

import json 
import time 
import pandas
import math 
import bot

from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime 
import sys 


def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data 


class BotInputHandler(PatternMatchingEventHandler):
    patterns = [sys.argv[1] + "/game_status.json"]

    def __init__(self, bot_id):
        super().__init__()
        self.bot_id = bot_id 


    def process(self, event):
        print(event.src_path, event.event_type)
        gamestatus = read_json(sys.argv[1] + '/game_status.json')
        bot.play(self.bot_id, gamestatus)   
    

    def on_modified(self, event):
        self.process(event)    
    

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("$ main.py <pasta io> <bot_id>")
        sys.exit()
    
    observer = Observer()
    observer.event_queue.maxsize = 0
    observer.schedule(BotInputHandler(int(args[1])), path=args[0] if args else ".")
    observer.start()

# watch for changes in game_status.json
print("Watching {} ...".format(args[0]))

try:
    while True:
        time.sleep(1)
    
except KeyboardInterrupt:
    observer.stop()

observer.join()
