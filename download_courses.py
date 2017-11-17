import json
import os
import urllib

ROOT = "download/Courses/"

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

with open('courses.json') as json_file:
	courses = json.load(json_file)

for course in courses:
	MAIN_PATH = course['path']
	COURSE_NAME = course['name']
	for level in course['levels']:
		FOLDER_PATH = level['name']
		PATH = MAIN_PATH + "/" + COURSE_NAME + "/" + FOLDER_PATH
		for video in level['videos']:
			video['name']
			downloadAFileWithPath(video['url'], PATH, video['name'], "mp4")

