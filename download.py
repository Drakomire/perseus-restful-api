"""
File Downloads
"""
import requests
import json
import io
import os
from os import path
import hashlib
import glob
import time

dir = os.path.dirname(__file__)

#REMINDER TO ADD WHITELIST/BLACKLIST FOR DOWNLOADS

# Taken from https://stackoverflow.com/a/600612/119527

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        pass

def safe_open(path, *args, **kwargs):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, *args, **kwargs)


def init(force: bool=False,url='https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/'):
    if not isinstance(force, bool):
        raise TypeError("argument force should be of type bool")

    ##Fix trailing slash if user doesn't add one for useability. I feel like that would be a pretty annoying thing to debug.
    if not url.endswith("/"):
        url = url + "/"

    kept = 0
    changed = 0
    downloaded = 0
    deleted = 0

    downloaded_files = glob.glob("data/**/*.json")
    for i,val in enumerate(downloaded_files):
        downloaded_files[i] = path.join(dir,val).replace("perseus/perseus","perseus")

    #Get checksums
    j = requests.get(url+'checksums.json').content
    checksums = json.loads(j)

    f = open("data/checksums.json","wb")
    f.write(j)
    f.close()

    for key in checksums:
        filepath = path.join(dir,"data",key)
        if (path.exists(filepath) and not force):
            #Checksum file to chek for changes
            #If the checksum is differnt redownload the file
            f = open(filepath, "rb")
            if (checksums[key] == hashlib.md5(f.read()).hexdigest()):
                kept += 1
            else:
                j = requests.get(url+key).content
                f = open(filepath, "w")
                f.write(j.decode("utf-8"))
                changed+=1
            f.close()
        else:
            #Download the file
            downloaded += 1
            j = requests.get(url+key).content
            f = safe_open(filepath, "w")
            f.write(j.decode("utf-8"))
            f.close()
        if filepath in downloaded_files:
            downloaded_files.remove(filepath)

    #Remove all the depecated files
    for i in downloaded_files:
        deleted += 1
        os.remove(i)

    if (not force):
        print(downloaded+changed,"files downloaded.",deleted,"files deleted.",kept,"files did not require an update.")
    else:
        print(downloaded+changed,"files downloaded.",deleted,"files deleted.")