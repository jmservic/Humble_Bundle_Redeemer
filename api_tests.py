from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN
#We're going to use the pickle module to save and load the cookies.
cj = MozillaCookieJar("./cookies.txt")
with Session() as s:
    print(f"Cookies before request to humble bundle main page:\n {s.cookies}")
    print(f"Cookie jar object:")
    for cookie in iter(cj):
        print(cookie)
    r = s.get(HUMBLE_MAIN, cookies=cj)
#    print(r.text) 
    print(f"Cookies after request to humble bundle main page: \n {s.cookies}")
    print(f"Cookie jar object:")
    for cookie in iter(cj):
        print(cookie)
