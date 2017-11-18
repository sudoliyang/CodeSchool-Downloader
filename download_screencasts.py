import json
import os
import urllib

ROOT = "download/Screencasts/"

def creatDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def downloadAFileWithPath(url , path ,filename, ex):
    creatDir(ROOT + path)
    pathName = ROOT + path + '/' +  filename + '.' + ex
    pathDownLoading = pathName + '.downloading'

    if os.path.isfile(pathName):
        print "already have the file: " + pathName
        return
    if os.path.isfile(pathDownLoading):
        os.path.isfile(pathDownLoading)
        os.remove(pathDownLoading)
    try:
        urllib.urlretrieve(url,pathDownLoading)
        os.rename(pathDownLoading,pathName)
        print "add path: " + pathName
    except:
        print "error in downloadning"

with open('screencasts.json') as json_file:
    screencasts = json.load(json_file)

for screencast in screencasts: 
    MAIN_PATH = screencast['path']
    downloadAFileWithPath(screencast['video'], MAIN_PATH, screencast['name'], "mp4")
