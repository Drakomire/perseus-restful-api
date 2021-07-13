import api_paths
from flask import Flask, request, abort
from download import init

app = Flask(__name__)

if __name__ == "__main__":
    init()


@app.route('/')
def index():
    return 'Welcome to the Perseus API! Please use the wrapper https://github.com/Drakomire/perseus.py'

from api_paths import ship
app.run(debug=True,port=5000,threaded=True)