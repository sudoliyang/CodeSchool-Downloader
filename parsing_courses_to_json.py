import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import urllib
from time import sleep
import atexit

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

def readACourse(link):
    global browser
    
    course = {
        "name": "",
        "path": "",
        "url" : "",
        "folders": []
    }
    
    browser.get("https://www.codeschool.com" + link + "/videos")
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    NAME = soup.find('h1',{'class','courseBanner-title'}).text
    PATH = soup.find('p',{'class':'mbf tss ttu'}).find('a').text
    
    if PATH == "HTML/CSS":
        PATH = "HTML&CSS"
    elif PATH == ".NET":
        PATH = "dot NET"
    print PATH + "  /  " + NAME
    
    course['name'] = NAME
    course['path'] = PATH
    course['url'] = "https://www.codeschool.com" + link + "/videos"
    
    cleanSoup = soup.find('div',{'class':'row has-sector'})
    videos = cleanSoup.findAll('a',{'class':'bdrn js-level-open'})
    titles = cleanSoup.find_all('strong')
    
    videoCount = 0
    flag = 0
    for title in titles:
        if title.has_attr('class'):
            video = {
                "name": "",
                "url": "",
            }
            URL = clickTitle(videos[videoCount]['href'])
            
            TITLE = title.text
            if "?" in title.text:
                TITLE.replace('?','<Q>')


            video['name'] = TITLE
            video['url'] = URL
            folder['videos'].append(video)

            videoCount+=1
        else:
            if flag:
                course['folders'].append(folder)
            folder = {
                "name" : "",
                "videos" : [] 
            }
            folder['name'] = title.text
            flag = 1
            
        if videoCount >= len(videos):
            course['folders'].append(folder)
            break
    return course

def readVideoDirectURL():
    global browser
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    URL = soup.find('video')['src']
    return URL

def clickTitle(href):
    global browsr 
    browser.find_element_by_css_selector("a[href*='"+ href +"']").click()
    sleep(0.6)
    URL = readVideoDirectURL()
    browser.find_element_by_class_name('js-video-manager-close').click()
    sleep(0.5)
    return URL

sign_in()
Links = LinkGenerator()

courses = []
for index, link in enumerate(Links):
    print str(index) + "  " + "https://www.codeschool.com" + link + '/videos'
    course = readACourse(link)
    courses.append(course)
