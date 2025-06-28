from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN, HumbleClient 
import os
#We're going to use the pickle module to save and load the cookies.

if not os.path.exists("./cookies"):
    os.mkdir("./cookies")
hb = HumbleClient(login="InqindiGaming@gmail.com")
print(f"Cookies before request to humble bundle main page:")
hb_cookies = hb.GetSessionCookies()
for cookie in hb_cookies:
    print(cookie)

hb.VisitHomePage()
hb_cookies = hb.GetSessionCookies()
print(f"Cookies after request to humble bundle main page:")
for cookie in hb_cookies:
    print(cookie)
#with Session() as s:
#    print(f"Cookies before request to humble bundle main page:\n {s.cookies}")
#    print(f"Cookie jar object:")
#    for cookie in iter(cj):
#        print(cookie)
#    r = s.get(HUMBLE_MAIN, cookies=cj)
#    print(r.text) 
#    print(f"Cookies after request to humble bundle main page: \n {s.cookies}")
#    print(f"Cookie jar object:")
#    for cookie in iter(cj):
#        print(cookie)
