from abc import ABC, abstractmethod
from requests import Session 
from requests.cookies import cookiejar_from_dict, create_cookie, morsel_to_cookie
import pickle
from os.path import exists
from time import sleep
import http.client, urllib.parse
import http.cookies

HUMBLE_MAIN = "https://www.humblebundle.com/"
HUMBLE_KEYS = "https://www.humblebundle.com/home/keys"
HUMBLE_LOGIN = "https://www.humblebundle.com/login"
HUMBLE_LOGIN_API = "http://localhost:1234/processlogin"#"https://www.humblebundle.com/processlogin"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
class GameKeyClient(ABC):

    @abstractmethod
    def Login(self, login, password):
        pass

    @abstractmethod
    def GetGamesInfo(self):
        pass

    @abstractmethod
    def ChooseContent(self, gamekey, identifiers):
        pass

    @abstractmethod
    def RedeemKey(self, keytype, gamekey, keyindex):
        pass

class HumbleClient(GameKeyClient):
    
    def __init__(self, login=None, password=None):
        self.__session = Session()
        self.__login = login
        self.__password = password
        self.__loggedIn = False
        self.__LoadCookies()

    def Login(self, payload=None):
        if self.__loggedIn:
            return (True, None)
        
        response = self.__session.get(HUMBLE_KEYS, headers={"User-Agent": USER_AGENT})
        #print(f"Status code = {response.status_code}")
        #print(f"Final URL of the Response = {response.url}")
        #print(f"Request headers {response.request.headers}")
        if not HUMBLE_LOGIN in response.url:
            print("Already Logged In")
            self.__loggedIn = True
            return (True, None)
        #Using http.client because Cloudflare continues to block the requests-module for processlogin requests
        conn = http.client.HTTPSConnection("www.humblebundle.com")

        headers = {"Csrf-Prevention-Token": self.__session.cookies["csrf_cookie"]
                   , "User-Agent": USER_AGENT
                   , "Cookie": self.__CookieString()
                   , "Content-type": "application/x-www-form-urlencoded"
                   #, "accept": "application/json, text/javascript, */*; q=0.01"
                   #, "accent-language": "en-US,en;q=0.9"
                   #, "origin": "https://www.humblebundle.com"
                   #, "priority": "u=1, i"
                   #, "referer": "https://www.humblebundle.com/login?goto=/home/keys"
                   #, "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"'
                   #, "sec-ch-ua-mobile": "?0"
                   #, "sec-ch-ua-platform": '"Windows"'
                   #, "sec-fetch-dest": "empty"
                   #, "sec-fetch-mode": "cors"
                   #, "sec-fetch-site": "same-origin"
                   #, "x-requested_with": "XMLHttpRequest"
                   }
        if not payload:
            payload = {}
        payload["goto"] = "/home/keys"
        payload["password"] = self.__password
        payload["username"] = self.__login
        payload["qs"] = "reason=secureArea"
        payload["guard"] = "CCPG5S5"
        payloadStr = urllib.parse.urlencode(payload)
        print(headers)
        print(payloadStr)
        #sleep(2)
        conn.request("POST", "/processlogin", payloadStr, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        print(res.getheaders())
        print(res.status)
        print(res.reason)
        print(type(res))
        #with open("SuccessfulPostHeaders.txt", "w") as f:
        #    f.write(res.getheader("Set-Cookie"))
        responseHeaders = res.getheaders()
        set_cookie_dict = {}
        set_cookies = []
        for (name, value) in responseHeaders:
            if(name == "Set-Cookie"):
        #        print(name, value)
                cookie = http.cookies.SimpleCookie()
                cookie.load(rawdata=value)
                set_cookies.append(cookie)
                cookieSplit = value.split("=", maxsplit=1)
                set_cookie_dict[cookieSplit[0]] = cookieSplit[1].split(";", maxsplit=1)[0]
       #print(set_cookie_dict)
       #print("The SimpleCookie:")
       #print(set_cookies[0]["_simpleauth_sess"].value)
       #print(dict(self.__session.cookies))
        #print(self.__session.cookies.get("_simpleauth_sess"))
        print("Before updating Cookies from http.client Post Request:")
        print(self.__CookieString())
        print()
        #new_cj = cookiejar_from_dict(set_cookie_dict)
        #self.__session.cookies = cookiejar_from_dict(dict(self.__session.cookies), new_cj, False)
        valid_request_cookie_keys = ["vesion", "port", "domain", "path", "secure", "expires", "discard", "comment", "comment_url", "rfc2109"]
        for cookieGroup in set_cookies:
            for (cookie, morsel) in cookieGroup.items():
                print(cookie, morsel.value)
                kw_args = {}
                for (key, kv) in morsel.items():
                    if key.lower() in valid_request_cookie_keys:
                        print(key, kv)
                        kw_args[key] = kv
                self.__session.cookies.set_cookie(morsel_to_cookie(morsel))
        print("After updating Cookies from http.client Post Request:")
        print(self.__CookieString())
        #response = self.__session.post(HUMBLE_LOGIN_API, data=payload, headers=headers) 
        #print(f"Status code of post request {response.status_code}")
        #print(f"Request headers {response.request.headers}")
        #print(f"Request body {response.request.body}")
        #print(f"Text of post request {response.text}")
        #print(f"The reponse itself {response}")

    def GetGamesInfo(self):
        pass

    def ChooseContent(self, gamekey, identifiers):
        pass

    def RedeemKey(self, keytype, gamekey, keyindex=0):
        pass

    def VisitHomePage(self):
        if self.__session:
            print(f"Final URL of visit home page = {self.__session.get(HUMBLE_MAIN, headers={'User-Agent': USER_AGENT}).url}")

    def GetSessionCookies(self):
        if self.__session:
            return self.__session.cookies.copy()
    
    def __CookieString(self):
        return "; ".join([f"{key}={value}" for (key, value) in self.__session.cookies.items()])

    def __LoadCookies(self):
        if not self.__session or not self.__login:
            return
        cookies_file = f"./cookies/hb_{self.__login.lower()}_cookies.txt"
        if not exists(cookies_file):
            return
        with open(cookies_file, "r+b") as f:
            cj = pickle.load(f)
            cj.clear_expired_cookies()
            self.__session.cookies = cj
    
    def __del__(self):
        if self.__session :
            try:
                if self.__login and len(self.__session.cookies) > 0:
                    cookies_file = f"./cookies/hb_{self.__login.lower()}_cookies.txt"
                    with open(cookies_file, "w+b") as f:
                        pickle.dump(self.__session.cookies, f)
            except Exception as ex:
                print(f"Exception of type {type(ex)}: {ex}")
            finally:
                self.__session.close()


