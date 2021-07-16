import sys
sys.path.append("..")
from __main__ import app
from flask import request, abort

@app.errorhandler(418)
def resource_not_found(e):
    return str(e)

@app.route("/teapot")
def teapot():
    abort(418)