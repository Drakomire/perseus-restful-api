import json

def open_json(path):
    f = open("data/" + path, "r", encoding='utf-8')
    return json.loads(f.read())