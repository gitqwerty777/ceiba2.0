#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, grequests, hashlib
import json, codecs
import cgitb

from pyquery import PyQuery as pq

fullData = {"bulletin":[], "syllabus":[], "grade":[], "homework":[], "courseName":[]}
duplicateChecker = set()

def getHashValue(data):
    hashvalue = hashlib.md5()
    hashvalue.update(json.dumps(data, indent=4))
    hashvalue = hashvalue.digest()
    return hashvalue

def handleBulletin(content):
    bulletin = pq(content)
    table = bulletin("table")
    Notifications = []
    for row in table("tr").items():
        Notification = dict()
        for ci, col in enumerate(row("td").items()):
            if(ci == 0):
                Notification["id"] = col.text()
            elif(ci == 1):
                Notification["date"] = col.text()
            elif(ci == 2):
                Notification["link"] = col("a").attr("href")
                Notification["title"] = col("a").text()
            elif(ci == 3):
                Notification["duration"] = col.text()
        if(len(Notification) != 0):
            Notifications.append(Notification)
    return Notifications
        
def handleSyllabus(content):
    syllabus = pq(content)
    table = syllabus("table")
    contents = []
    for row in table("tr").items():
        mycontent = dict() 
        for ci, col in enumerate(row("td").items()):
            if(ci == 0):
                mycontent["week"] = col.text()
            elif(ci == 1):
                mycontent["date"] = col.text()
            elif(ci == 2):
                mycontent["title"] = col.text()
            elif(ci == 3):
                mycontent["filename"] = []
                mycontent["filelink"] = []
                for filep in col("p").items():
                    mycontent["filelink"].append(filep("a").attr("href"))
                    mycontent["filename"].append(filep("a").text())
        if(len(mycontent) != 0):
            contents.append(mycontent)
    return contents

def handleHW(content):
    hw = pq(content)
    table = hw("table")
    homeworks = []
    for row in table("tr").items():
        homework = dict()
        for ci, col in enumerate(row("td").items()):
            if(ci == 0):
                homework["index"] = col.text()
            elif(ci == 1):
                homework["member"] = col.text()
            elif(ci == 2):
                homework["way"] = col.text()
            elif(ci == 3):
                homework["ratio"] = col.text()
            elif(ci == 4):
                homework["mainname"] = col("a").text()
                homework["mainlink"] = col("a").attr("href")
            elif(ci == 5):
                homework["headline"] = col.text()
            elif(ci == 7):
                homework["commitdate"] = col.text()
            elif(ci == 8):
                homework["evallink"] = col("a").attr("href")
        if(len(homework) != 0):
            #print homework
            homeworks.append(homework)
    return homeworks

def handleGrade(content):
    grade = pq(content)
    table = grade("table")
    scores = []
    for row in table("tr").items():
        score = dict()
        for ci, col in enumerate(row("td").items()):
            if(ci == 0):
                score["title"] = col.text()
            elif(ci == 1):
                score["ratio"] = col.text()
            elif(ci == 2):
                score["sublink"] = col("a").attr("href")
            elif(ci == 5):
                score["score"] = col.text()
            elif(ci == 6):
                score["comment"] = col.text()
        if(len(score) != 0):
            #print score
            scores.append(score)
    return scores

# http://stackoverflow.com/questions/25115151/how-to-pass-parameters-to-hooks-in-python-grequests
def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(response, *request_args, **request_kwargs):
        #print "ci = ", factory_kwargs["cid"], " fi = ", factory_kwargs["fid"], " url = ", response.url
        

        ci = factory_kwargs["cid"]
        fi = factory_kwargs["fid"]
        print response.url + "\t ci = " + str(ci) + "\t fi = " + str(fi) + "\n"
        if(factory_kwargs["url"] != response.url):
            content = response.content.decode('big5')
            if(fi == 0):
                #handlers[0](content) TODO:
                data = handleBulletin(content)
                hashvalue = getHashValue(data)
                if (hashvalue not in duplicateChecker):
                    duplicateChecker.add(hashvalue)
                    fullData["bulletin"].append(data)
                else:
                    fullData["bulletin"].append([])
            elif(fi == 1):
                data = handleSyllabus(content)
                hashvalue = getHashValue(data)
                if (hashvalue not in duplicateChecker):
                    duplicateChecker.add(hashvalue)
                    fullData["syllabus"].append(data)
                else:
                    fullData["syllabus"].append([])
            elif(fi == 2):
                data = handleHW(content)
                hashvalue = getHashValue(data)
                if (hashvalue not in duplicateChecker):
                    duplicateChecker.add(hashvalue)
                    fullData["homework"].append(data)
                else:
                    print "homework ", ci , "is the same"
                    fullData["homework"].append([])
            elif(fi == 3):
                data = handleGrade(content)
                hashvalue = getHashValue(data)
                if (hashvalue not in duplicateChecker):
                    duplicateChecker.add(hashvalue)
                    fullData["grade"].append(data)
                else:
                    fullData["grade"].append([])
        #print fullData
        return response
    return response_hook
    
class CeibaParser:
    def __init__(self, user, pw):
        self.mainPage = None
        self.session = None
        self.courseIDs = []
        self.courseURLs = []
        self.fullData = {}

        self.login(user, pw)
        self.getCourses()

    def login(self, user, pw):
        # http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
        URL = 'https://ceiba.ntu.edu.tw/ChkSessLib.php'
        payload = {
            'user': user,
            'pass': pw,
            "Submit": "登入"
        }
        # TODO: use twisted to do async requests
        #session = requests_cache.CachedSession()
        self.session = requests.Session()
        r1 = self.session.head(URL, allow_redirects=True) # redirect
        #print (r1.status_code, r1.url, str(r1.cookies))
        r2 = self.session.post(r1.url, data=payload, allow_redirects=True) # login
        #print (r2.status_code, r2.url, str(r2.cookies))
        r4 = self.session.get(r2.url, allow_redirects=True) # redirect and get
        #print (r4.status_code, r4.url, str(r4.cookies))

        # r4.text.__class__  -> unicode
        # maybe encoding error
        # http://www.jb51.net/article/17560.htm
        self.mainPage = r4.content.decode('big5')

    def getCourses(self):
        self.mainPage = pq(self.mainPage);
        table = self.mainPage("table:first")
        for ri, tr in enumerate(table("tr").items()):
            for ci, td in enumerate(tr("td").items()):
                if(ci == 4):
                    fullData["courseName"].append(td("a").html())
                    self.courseURLs.append(td("a").attr["href"])

        #print self.courseURLs

        courseRequest = (grequests.get(u, allow_redirects=True, session=self.session) for u in self.courseURLs)
        courseResponse = grequests.map(courseRequest)
        for u in courseResponse:
            self.courseIDs.append(u.url.rsplit('/', 2)[-2])
            #print u.url.rsplit('/', 2)[-2]

    def parse(self):

        functionURLformat = "https://ceiba.ntu.edu.tw/modules/main.php?csn=%s&default_fun=%s&current_lang=chinese"
        functionNames = ['bulletin', 'syllabus', 'hw', 'grade']
        handlers = [handleBulletin, handleSyllabus, handleHW, handleGrade]

        #functionRequests = [] # tuple
        for ci, cname in enumerate(self.courseIDs):
            self.session.get(self.courseURLs[ci], allow_redirects=True) # should goto course main page at least once to reset course information
            functionRequests = [] # tuple
            for fi, fname in enumerate(functionNames):
                functionURL = functionURLformat % (cname, fname)
                functionRequest = grequests.get(functionURL, allow_redirects=True, session=self.session, hooks={'response': [hook_factory(cid=ci, fid=fi, url=functionURL)]})
                functionRequests.append(functionRequest)
            grequests.map(tuple(functionRequests))

if __name__ == "__main__":
    #cgitb.enable()
    #print("Content-Type: text/html;charset=utf-8")
    username = "r05922061"
    password = password
    # password = raw_input()
    parser = CeibaParser(username, password)
    parser.parse()

    with open("./"+ username +".json", "w") as file:
        json.dump(fullData, file, indent=4)
    #print json.dumps(fullData, indent=4, separators=(',', ': '), ensure_ascii=False, encoding='utf-8')
    print json.dumps(fullData, indent=4, separators=(',', ': '), ensure_ascii=False, encoding='utf-8').encode("utf-8")
     #print str(fullData).encode("utf-8")
    

