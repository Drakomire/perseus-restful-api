import difflib
import json

from util import open_json
from __main__ import app

def startup():
    global gear, all_gear_ids, all_gear_names, gear_name_lookup_table
    gear = open_json("gear/gear.json")
    barrages = open_json("gear/barrage.json")

    all_gear_names = {
        "en" : [],
        "jp" : [],
        "cn" : [],
    }

    gear_name_lookup_table = {}

    for gear_id in gear:
        g = gear[gear_id]

        gear_name_lookup_table[g.get("name_EN","")] = gear_id
        gear_name_lookup_table[g.get("name_JP","")] = gear_id
        gear_name_lookup_table[g.get("name_CN","")] = gear_id


        all_gear_names["en"] += [f'{g.get("name_EN","")},{gear_id}']
        all_gear_names["jp"] += [f'{g.get("name_JP","")},{gear_id}']
        all_gear_names["cn"] += [f'{g.get("name_CN","")},{gear_id}']

        if "weapons" in g:
            g["weapons"] = [
                barrages[str(group[0])]     
                for group in g["weapons"]
            ]

    all_gear_ids = []
    for i in gear:
        all_gear_ids += [gear[i]["id"]]

    all_gear_ids = json.dumps(all_gear_ids)

@app.route('/gear/<path:id>')
def get_gear(id):
    #Non-numeric IDs need to be converted to the ID that the API uses
    id = gear_name_lookup_table.get(id,id)

    return gear.get(str(id), 
        {
            "error" : "Gear ID is invalid"
        }
    )

@app.route('/gear/search/<path:name>')
def search_for_gear(name):
    diff = difflib.get_close_matches(name, all_gear_names["en"], 20, .4)
    org_dif = []
    for item in diff:
        split = item.split(",")
        org_dif += [(split[0],split[1])]

    return json.dumps(org_dif)

@app.route('/gear/all_ids')
def get_all_gear_ids():
    return all_gear_ids