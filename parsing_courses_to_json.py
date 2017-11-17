import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import urllib
from time import sleep
import atexit
from selenium.webdriver.common.keys import Keys

Username = ""
Password = ""
browser = webdriver.Firefox()

def saveToJSON():
    global courses
    prettyCourses = json.dumps(courses, sort_keys=True, indent=2, separators=(',', ': '))
    with open("courses.json", "w") as json_file:
        json_file.write(prettyCourses)

atexit.register(saveToJSON)

def sign_in():
    global browser,Username,Password
    sign_in_url = "http://www.codeschool.com/users/sign_in"
    browser.get(sign_in_url)
    browser.find_element_by_id("user_login").clear()
    browser.find_element_by_id("user_login").send_keys(Username)
    browser.find_element_by_id("user_password").clear()
    browser.find_element_by_id("user_password").send_keys(Password)
    browser.find_element_by_xpath("//div[@id='sign-in-form']/form/div/div/button").click()

def LinkGenerator():
    response = requests.get('https://www.codeschool.com/courses/')
    soup = BeautifulSoup(response.text,'lxml')
    list = []
    for item in soup.findAll('a','course-title-link'):
        list.append(item['href'])
    return list

def cleanPathName(name):
    if name == "HTML/CSS":
        name = "HTML&CSS"
    elif name == ".NET":
        name = "dot NET"
    return name

def readACourse(link):
    global browser
    course = {
        "name": "",
        "path": "",
        "url" : "",
        "levels": []
    }
    course_link = "https://www.codeschool.com" + link + "/videos"
    browser.get(course_link)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')


    course_name = soup.find('h1',{'class','courseBanner-title'}).text
    course_path = soup.find('p',{'class':'mbf tss ttu'}).find('a').text
    course_path = cleanPathName(course_path)

    course['name'] = course_name
    course['path'] = course_path
    course['url'] = course_link

    print course_path
    print course_name

    ls = soup.select("div.level")

    levels = []
    for l in ls:
        level_name = l.select_one("p.tss.level-title strong").text
        videos = l.select("li.list-item.video-title")
        level = {
            "name":"",
            "videos":[]
        }
        level["name"] = level_name
        print "  " + level_name
        for v in videos:
            video = {
                "name":"",
                "url":""
            }
            video_title = v.select_one("strong.tct").text
            click_url = v.select_one("a.bdrn.js-level-open")["href"]

            print "   " + video_title
            direct_url = clickTitle(click_url)
            video["name"] = video_title
            video["url"] = direct_url
            level["videos"].append(video)

            # print direct_url
        course["levels"].append(level)
    return course

def readVideoDirectURL():
    global browser
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    URL = soup.find('video')['src']
    return URL

def clickTitle(href):
    global browsr
    browser.execute_script('''document.querySelector("a[href='%s']").click()''' % href)
    sleep(2)
    URL = readVideoDirectURL()
    browser.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
    sleep(2)
    return URL

Links = LinkGenerator()
sign_in()
print "Signed !"

courses = []
for index, link in enumerate(Links):
    print str(index) + "  " + "https://www.codeschool.com" + link + '/videos'
    course = readACourse(link)
    courses.append(course)
