from abc import ABC, abstractmethod
from requests import Session 
from requests.cookies import cookiejar_from_dict, create_cookie, morsel_to_cookie
import pickle
from os.path import exists
import http.client, urllib.parse
from http_utils import SetCookieHeaderToMorsels 
from enum import Enum
import json
from bs4 import BeautifulSoup

STEAM_DOMAIN = "store.steampowered.com"
STEAM_REGISTER_KEY = "https://store.teampowered.com/account/registerkey"
STEAM_REGISTER_KEY_API = "/account/ajaxregisterkey"
STEAM_PASS_RSA_PUBLIC_KEY_API = "/IAuthenticationService/GetPasswordRSAPublicKey/v1"
STEAM_BEGIN_AUTH_API = "/IAuthenticationService/BeginAuthSessionViaCredentials/v1"
STEAM_POLL_AUTH_STATUS_API = "/IAuthenticationService/PollAuthSessionStatus/v1"
STEAM_FINALIZE_LOGIN_API = "/jwt/finalizelogin"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"

class LibraryClient(ABC):

    @abstractmethod
    def Login(self, payload=None):
        pass

    @abstractmethod
    def GetLibraryDetails(self):
        pass

    @abstractmethod
    def RegisterKey(self, gamekey):
        pass

class SteamClient(LibraryClient):

    def __init__(self, login=None, password=None user_agent=USER_AGENT):
        self.__session = Session()
        self.__login = login
        self.__password = password
        self.__loggedIn = False
        self.__LoadCookies()

    def Login(self, payload=None):
        pass

    def GetLibraryDetails(self):
        pass

    def RegisterKey(self, gamekey):
        pass

    def Set_Login(self, login):
        self.__login = login

    def Set_Password(self, password):
        self.__password = password

    def GetSessionCookies(self):
        if self.__session:
            return self.__session.cookies.copy()

    def __SetCookies(self, responseHeaders):    
        morsels = SetCookieHeaderToMorsels(responseHeaders)
        for morsel in morsels.values():
            self.__session.cookies.set_cookie(morsel_to_cookie(morsel))

        
    def __CookieString(self):
        return "; ".join([f"{key}={value}" for (key, value) in self.__session.cookies.items()])

    def __LoadCookies(self):
        if not self.__session or not self.__login:
            return
        cookies_file = f"./cookies/steam_{self.__login.lower()}_cookies.txt"
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
                    cookies_file = f"./cookies/steam_{self.__login.lower()}_cookies.txt"
                    with open(cookies_file, "w+b") as f:
                        pickle.dump(self.__session.cookies, f)
            except Exception as ex:
                print(f"Exception of type {type(ex)}: {ex}")
            finally:
                self.__session.close()
