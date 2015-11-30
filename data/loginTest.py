# -*- coding: big5 -*-
import requests, grequests
from pyquery import PyQuery as pq

# http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module

def handleResponse(r, *args, **kargs):
    for arg in args:
        print arg
    print r.url, " ok!"

def handleBulletin():
    pass
def handleSyllabus():
    pass
def handleHW():
    pass
def handleGrade():
    pass
    
class CeibaParser:
    def __init__(self, user, pw):
        self.mainPage = None
        self.session = None
        self.login(user, pw)
        self.parse()

    def login(self, user, pw):
        URL = 'https://ceiba.ntu.edu.tw/ChkSessLib.php'
        payload = {
            'user': user,
            'pass': pw,
            "Submit": "登入"
        }
        # TODO: use twisted to do async requests
        #session = requests_cache.CachedSession()
        self.session = requests.Session()
        r1 = self.session.head(URL, allow_redirects=True) # will redirect
        print (r1.status_code, r1.url, str(r1.cookies))
        r2 = self.session.post(r1.url, data=payload, allow_redirects=True)
        print (r2.status_code, r2.url, str(r2.cookies))
        r4 = self.session.get(r2.url, allow_redirects=True)
        print (r4.status_code, r4.url, str(r4.cookies))

        # r4.text.__class__  -> unicode
        # maybe encoding error
        # http://www.jb51.net/article/17560.htm
        self.mainPage = r4.content.decode('big5')

    def parse(self):
        self.mainPage = pq(self.mainPage);
        table = self.mainPage("table:first")
        courseURLs = []
        for ri, tr in enumerate(table("tr").items()):
            for ci, td in enumerate(tr("td").items()):
                if(ci == 4):
                    courseURLs.append(td("a").attr["href"])
        print courseURLs

        courseRequest = (grequests.get(u, allow_redirects=True, session=self.session, hooks=dict(response=handleResponse)) for u in courseURLs)
        courseResponse = grequests.map(courseRequest)
        courseIDs = []
        for u in courseResponse:
            courseIDs.append(u.url.rsplit('/', 2)[-2])
            print u.url.rsplit('/', 2)[-2]

        functionURLformat = "https://ceiba.ntu.edu.tw/modules/main.php?csn=%s&default_fun=%s&current_lang=chinese"
        functionNames = ['bulletin', 'syllabus', 'hw', 'grade']
        for ci, cname in enumerate(courseIDs):
            for fi, fname in enumerate(functionNames):
                functionURL = functionURLformat % (cname, fname)
                print functionURL
                if(fi == 0):
                    if(ci == 2):
                        functionrs = self.session.get(functionURL, allow_redirects=True)
                        print functionrs.content.decode('big5')
                    handleBulletin()
                elif(fi == 1):
                    handleSyllabus()
                elif(fi == 2):
                    handleHW()
                elif(fi == 3):
                    handleGrade()

if __name__ == "__main__":
    parser = CeibaParser("b01902059", "fakepassword")
    handlers = [handleBulletin, handleSyllabus, handleHW, handleGrade]




