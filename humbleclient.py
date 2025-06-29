from abc import ABC, abstractmethod
from requests import Session
import pickle
from os.path import exists

HUMBLE_MAIN = "https://www.humblebundle.com/"

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

    def Login(self, login, password):
        pass

    def GetGamesInfo(self):
        pass

    def ChooseContent(self, gamekey, identifiers):
        pass

    def RedeemKey(self, keytype, gamekey, keyindex=0):
        pass

    def VisitHomePage(self):
        if self.__session:
            self.__session.get(HUMBLE_MAIN)

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


