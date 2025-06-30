from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN, HumbleClient 
import os
from dotenv import load_dotenv
#We're going to use the pickle module to save and load the cookies.
load_dotenv()
hb_account = os.getenv("HB_ACCOUNT")
hb_password = os.getenv("HB_PASSWORD")

if not os.path.exists("./cookies"):
    os.mkdir("./cookies")
hb = HumbleClient(login=hb_account,password=hb_password)
print(f"Cookies before request to humble bundle main page:")
hb_cookies = hb.GetSessionCookies()
for cookie in hb_cookies:
    print(cookie)

hb.VisitHomePage()
hb_cookies = hb.GetSessionCookies()
print(f"Cookies after request to humble bundle main page:")
#for (cookie_name, cookie_value) in dict(hb_cookies).items():
#    print(cookie_name, cookie_value)
print("")
print(hb_cookies.get("_simpleauth_sess"))
#for cookie in hb_cookies:
#    print(cookie.domain)
hb.Login()
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
