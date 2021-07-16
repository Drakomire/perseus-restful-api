import sys
sys.path.append("..")
from __main__ import app
from util import open_json
from flask import request
import json

def startup():
    global ship_lookup_table, retrofit_id_lookup_table, ships, nicknames

    ship_lookup_table = open_json("ships/lookup_table.json")
    retrofit_id_lookup_table = open_json("ships/retrofit_id_lookup_table.json")
    ships = open_json("ships/ships.json")
    nicknames = open_json("ships/nicknames.json")

    global all_ship_names, all_ship_ids

    all_ship_names = {
        "en" : [],
        "jp" : [],
        "cn" : [],
    }

    for i in ships:
        try:
            all_ship_names["en"] += [ships[i]["name"]["en"]]
        except:
            pass
        try:
            all_ship_names["jp"] += [ships[i]["name"]["cn"]]
        except:
            pass
        try:
            all_ship_names["cn"] += [ships[i]["name"]["cn"]]
        except:
            pass

    all_ship_ids = []
    for i in ships:
        all_ship_ids += [ships[i]["id"]]


@app.route('/ship/<path:id>')
def get_ship(id):
    #Non-numeric IDs need to be converted to the ID that the API uses
    if not id.isnumeric():
        if request.args.get('nicknames') == "True" and id.lower() in nicknames:
            id = nicknames[id.lower()]
        if id.lower() in ship_lookup_table:
          id = ship_lookup_table[id.lower()]
    if str(id) in retrofit_id_lookup_table:
        id = retrofit_id_lookup_table[str(id)]
    if str(id) in ships:
        return ships[str(id)]
    else:
        return {
            "error" : "Ship name or ID is invalid"
        }

@app.route('/ship/all_names')
def get_all_ships():
    lang = request.args.get('nicknames') or 'en'
    return json.dumps(all_ship_names[lang],ensure_ascii=False)


@app.route('/ship/all_ids')
def get_all_ship_ids():
    return json.dumps(all_ship_ids)