from util import open_json
from __main__ import app
import json

def startup():
    global gear, all_gear_ids
    gear = open_json("gear/gear.json")

    all_gear_ids = []
    for i in gear:
        all_gear_ids += [gear[i]["id"]]

    all_gear_ids = json.dumps(all_gear_ids)

@app.route('/gear/<path:id>')
def get_gear(id):
    #Non-numeric IDs need to be converted to the ID that the API uses
    if str(id) in gear:
        return gear[str(id)]
    else:
        return {
            "error" : "Gear ID is invalid"
        }

@app.route('/gear/all_ids')
def get_all_gear_ids():
    return all_gear_ids