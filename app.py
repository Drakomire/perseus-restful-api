import api_paths
from flask import Flask, request, abort
from download import init
import asyncio
import time
import threading
import requests
from waitress import serve
import sys

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
    app = Flask(__name__)
    from api_paths import ship, teapot
    @app.route('/')
    def index():
        return 'Welcome to the Perseus API!. Please read the docs https://github.com/Drakomire/perseus-restful-api.'

    poll = Poll(interval=60*6)
    if "prod" in sys.argv:
        print("Running waitress production server")
        serve(app,listen='*:5000')
    else:
        print("Running flask dev server")
        app.run(debug=True,port=5000,threaded=True)