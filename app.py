import api_paths
from flask import Flask, request, abort
from download import init
import asyncio
import time
import threading
import requests
from waitress import serve
import sys

class Poll:
    def __init__(self, url, interval=1):
        self.url = url
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """ Method that runs forever """
        getVersion = lambda: requests.get(self.url+"version").content
        cur_version = getVersion()
        init(url=self.url)
        startup()
        while True:
            version = getVersion()
            if cur_version != version:
                init(url=self.url)
                startup()
                cur_version = version
                print("Updated")

            time.sleep(self.interval)

def main(app):
    if "prod" in sys.argv:
        print("Running waitress production server")
        url = 'https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/'
        poll = Poll(url, interval=360)
        serve(app,listen='*:5000')
    else:
        print("Running flask dev server")
        startup()
        app.run(debug=True,port=5000,threaded=True)

if __name__ == "__main__":
    app = Flask(__name__)
    @app.route('/')
    def index():
        return 'Welcome to the Perseus API!. Please read the docs https://github.com/Drakomire/perseus-restful-api.'

    #This  function will update all data. The API data can be updated without any downtime with this function.
    from api_paths import ship, gear, teapot
    def startup():
        ship.startup()
        gear.startup()

    main(app)