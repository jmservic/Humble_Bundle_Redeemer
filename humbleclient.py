from abc import ABC, abstractmethod
from requests import Session
import pickle
from os.path import exists
from time import sleep

HUMBLE_MAIN = "https://www.humblebundle.com/"
HUMBLE_KEYS = "https://www.humblebundle.com/home/keys"
HUMBLE_LOGIN = "https://www.humblebundle.com/login"
HUMBLE_LOGIN_REQUEST = "https://www.humblebundle.com/processlogin"
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

    def Login(self, params=None):
        if self.__loggedIn:
            return (True, None)

        #response = self.__session.get(HUMBLE_KEYS, headers={"User-Agent": USER_AGENT})
        #print(f"Status code = {response.status_code}")
        #print(f"Final URL of the Response = {response.url}")
        #print(f"Request headers {response.request.headers}")
        #if not HUMBLE_LOGIN in response.url:
        #    self.__loggedIn = True
        #    return (True, None)

        headers = {"Csrf-Prevention-Token": self.__session.cookies["csrf_cookie"]
                   , "User-Agent": USER_AGENT
                   , "Accept-Encoding": "gzip, deflate, br"}
        if not params:
            params = {}
        params["goto"] = "/home/keys"
        params["password"] = self.__password
        params["username"] = self.__login
        params["qs"] = "reason=secureArea"
        #print(headers)
        #sleep(5)
        response = self.__session.post(HUMBLE_LOGIN_REQUEST, data=params, headers=headers) 
        print(f"Status code of post request {response.status_code}")
        print(f"Request headers {response.request.headers}")
        print(f"Request body {response.request.body}")
        #print(f"Text of post request {response.text}")
        print(f"The reponse itself {response}")

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


