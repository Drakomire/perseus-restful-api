import sys
sys.path.append("..")
from __main__ import app
from util import open_json

ship_lookup_table = open_json("ships/lookup_table.json")
ships = open_json("ships/ships.json")
nicknames = open_json("ships/nicknames.json")

@app.route('/ship/<path:id>')
def get(id):
    #Check if id is a number
    if not id.isnumeric():
        if id.lower() in nicknames:
            id = nicknames[id.lower()]
        id = ship_lookup_table[id.lower()]

    return ships[str(id)]
