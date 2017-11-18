import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib
from time import sleep
import atexit

Username = ""
Password = ""
browser = webdriver.Firefox()

def saveToJSON():
    global browser
    prettyScreencast = json.dumps(Screencasts, sort_keys=True, indent=2, separators=(',', ': '))
    with open("screencasts.json", "w") as json_file:
        json_file.write(prettyScreencast)

def cleanPathName(name):
    if name == "HTML/CSS":
        name = "HTML&CSS"
    elif name == ".NET":
        name = "dot NET"
    return name

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

def parsePageScreenCastLinks():
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.select("a.db.has-play")
    page_links = []
    for article in articles:
        page_links.append(article["href"])
    return page_links

def generateScreenCastsLinks():
    links = []
    browser.get("https://www.codeschool.com/screencasts")
    sleep(5)
    page_links = parsePageScreenCastLinks()
    links.extend(page_links)
    changePage = '''
    function changePage(page_number){
        var links = document.querySelectorAll("a.video-page-link")
        for(var i = links.length - 1; i > -1; i--){
            var link = links[i]
            if(link.dataset.page == page_number){
                console.log(link)
                link.click()
                break
            }
        }
    };
    '''
    for i in range(2,10):
        browser.execute_script(changePage + "changePage(%s)" % i)
        sleep(10)
        page_links = parsePageScreenCastLinks()
        links.extend(page_links)

    # remove duplicates
    links = set(links)
    return links

def getVideoDirectURL(url):
    global browser

    isException = True
    reTryCount = 0

    while(isException and reTryCount < 3):
        try:
            browser.get(url)
            html  = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            url =  soup.select_one("video")["src"]
            path =  soup.select_one(".tag--heading").text
            name =  soup.select_one(".tci").text
            isException = False
        except KeyError:
            print "KeyError"
            sleep(2)
            reTryCount += 1

    return name, path, url


sign_in()
Links = generateScreenCastsLinks()

Screencasts = []
for index, link in enumerate(Links):
    screencast = {  "name":"",
                    "url":"",
                    "video":"",
                    "path":""}
    print index, link
    screencast["url"] = "https://www.codeschool.com" + link
    screencast["name"], screencast["path"], screencast["video"] = getVideoDirectURL(screencast["url"])
    screencast["path"] = cleanPathName(screencast["path"])
    print screencast["name"]
    Screencasts.append(screencast)

