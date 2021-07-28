import json
from pathlib import Path
from sys import argv

if "prod" in argv:
    DIST_PATH = "data"
else:
    DIST_PATH = str(Path(Path.home(),"Documents","GitHub","azurapi-data","dist"))

def open_json(path):
    f = open(DIST_PATH + "/" + path, "r", encoding='utf-8')
    return json.loads(f.read())