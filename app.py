import api_paths
from flask import Flask, request, abort
from download import init
import asyncio
import time
import threading
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Perseus API!. Please read the docs https://github.com/Drakomire/perseus-restful-api.'

from api_paths import ship, teapot

#This  function will update all data. The API data can be updated without any downtime with this function.
def startup():
    ship.startup()

class Poll:
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """ Method that runs forever """
        getVersion = lambda: requests.get("https://raw.githubusercontent.com/Drakomire/perseus-data/restful/dist/version").content
        cur_version = getVersion()
        init()
        startup()
        while True:
            version = getVersion()
            if cur_version != version:
                init()
                startup()
                cur_version = version
                print("Updated")

            time.sleep(self.interval)


if __name__ == "__main__":
    poll = Poll()
    app.run(debug=True,port=5000,threaded=True)