# -*- coding: big5 -*-
import requests
from pyquery import PyQuery as pq

# http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module

URL = 'https://ceiba.ntu.edu.tw/ChkSessLib.php'
payload = {
    'user': 'b01902059',
    'pass': 'password', 
    "Submit": "登入"
}

session = requests.Session()
r1 = session.head(URL, allow_redirects=True) # will redirect
print (r1.status_code, r1.url, str(r1.cookies))
r2 = session.post(r1.url, data=payload, allow_redirects=True)
print (r2.status_code, r2.url, str(r2.cookies))
r4 = session.get(r2.url, allow_redirects=True)
print (r4.status_code, r4.url, str(r4.cookies))
# TODO: use twisted to rewrite

# r4.text.__class__  -> unicode
# maybe encoding error
# http://www.jb51.net/article/17560.htm
ceibamain = r4.content.decode('big5')

ceibamain = pq(ceibamain);
#print str(ceibamain).encode("utf-8")

table = ceibamain("table:first")

courseURLs = []
for ri, tr in enumerate(table("tr").items()):
    for ci, td in enumerate(tr("td").items()):
        if(ci == 4):
            courseURLs.append(td("a").attr["href"])

for url in courseURLs:
    
