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
from steam_utils import EncodeProtoBuff, EncryptPassword
import Steam_RSA_Public_Key_Request_pb2 
from time import sleep

STEAM_DOMAIN = "store.steampowered.com"
STEAM_API_DOMAIN = "https://api.steampowered.com"
STEAM_LOGIN_DOMAIN = "https://login.steampowered.com"
STEAM_REGISTER_KEY = "https://store.steampowered.com/account/registerkey"
STEAM_REGISTER_KEY_API = "/account/ajaxregisterkey"
STEAM_PASS_RSA_PUBLIC_KEY_API = "/IAuthenticationService/GetPasswordRSAPublicKey/v1"
STEAM_BEGIN_AUTH_API = "/IAuthenticationService/BeginAuthSessionViaCredentials/v1"
STEAM_POLL_AUTH_STATUS_API = "/IAuthenticationService/PollAuthSessionStatus/v1"
STEAM_FINALIZE_LOGIN_API = "/jwt/finalizelogin"
STEAM_GAMES = "https://steamcommunity.com/my/games/"
STEAM_MAIN = "https://store.steampowered.com"
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

    def __init__(self, login=None, password=None, user_agent=USER_AGENT):
        self.__session = Session()
        self.__login = login
        self.__password = password
        self.__loggedIn = False
        self.__LoadCookies()
        self.__user_agent = user_agent

    def Login(self, payload=None):
        if self.__loggedIn:
            print(f"Already logged into steam as {self.__login}")
            return
        self.VisitHomePage()
        res = self.__session.get(STEAM_REGISTER_KEY)
        #print(res.url)
        if "login" not in res.url:
            self.__loggedIn = True
            print(f"Already logged into steam as {self.__login}")
            return

        #Possible do a state diagram for logging in?
        rsa_pk_response = self.GetRSAPublicKey()
        begin_auth_req = Steam_RSA_Public_Key_Request_pb2.SteamBeginAuthCredRequest()
        begin_auth_req.account_name = self.__login
        begin_auth_req.encrypted_password = EncryptPassword(self.__password, rsa_pk_response)
        begin_auth_req.encryption_timestamp = rsa_pk_response.timestamp
        begin_auth_req.remember_login = True
        begin_auth_req.platform_type = 1
        begin_auth_req.website_id = "Store"
        begin_auth_req.device_details.device_friendly_name = self.__user_agent
        begin_auth_req.device_details.platform_type = 2
        begin_auth_req.language = 0

        #print(begin_auth_req)
        begin_auth_req_serialized = begin_auth_req.SerializeToString()
        #print(begin_auth_req_serialized)
        #print(EncodeProtoBuff(begin_auth_req_serialized))
        body = {"input_protobuf_encoded": EncodeProtoBuff(begin_auth_req_serialized)}

        res = self.__session.post(STEAM_API_DOMAIN + STEAM_BEGIN_AUTH_API, data=body)

        print(res.status_code)
        print(res.content)
        begin_auth_response = Steam_RSA_Public_Key_Request_pb2.SteamBeginAuthCredResponse()
        begin_auth_response.ParseFromString(res.content)
        print(begin_auth_response)

        #If auth session is created poll the request repeatedly
        print(self.GetSessionCookies())
        print(self.__CookieString())

        while(True):
            poll_session_response = self.PollAuthSessionStatus(begin_auth_response.client_id, begin_auth_response.request_id)
            print(poll_session_response)
            if poll_session_response.refresh_token:
                break
            sleep(5)
        
        res = self.__session.post(STEAM_LOGIN_DOMAIN + STEAM_FINALIZE_LOGIN_API, data={"nonce": poll_session_response.refresh_token,
                                                                                     "sessionid": self.__session.cookies.get("sessionid", domain=STEAM_DOMAIN)})
        print(res.status_code)
        print(res.content)
        data = res.json()
        print(data)

        for request in data["transfer_info"]:
            url = request["url"]
            params = request["params"]
            params["steamID"] = begin_auth_response.steam_id 
            print(f"Setting token for URL: {url} and params {params}")
            res = self.__session.post(request['url'], data=request['params'])
            print(res.status_code)
            print(res.content)
            print(res.headers)
        
        res = self.__session.get(STEAM_REGISTER_KEY)
        print(res.url)
        if "login" not in res.url:
            self.__loggedIn = True
            print("Successfully logged into steam!! CONGRATS!!!")

    def PollAuthSessionStatus(self, client_id, request_id):
        poll_auth_session_req = Steam_RSA_Public_Key_Request_pb2.SteamPollAuthSessionRequest()
        poll_auth_session_req.client_id = client_id
        poll_auth_session_req.request_id = request_id

        poll_auth_session_req_serialized = poll_auth_session_req.SerializeToString()
        #print(poll_auth_session_req_serialized)
        #print(list(poll_auth_session_req_serialized))
        #print(EncodeProtoBuff(poll_auth_session_req_serialized))
        body = {"input_protobuf_encoded": EncodeProtoBuff(poll_auth_session_req_serialized)}

        res = self.__session.post(STEAM_API_DOMAIN + STEAM_POLL_AUTH_STATUS_API, data=body)

        print(res.status_code)
        print(res.content)
        poll_auth_session_response = Steam_RSA_Public_Key_Request_pb2.SteamPollAuthSessionResponse()
        poll_auth_session_response.ParseFromString(res.content)
        return poll_auth_session_response

    def GetLibraryDetails(self):
        if not self.__loggedIn:
            return

        res = self.__session.get(STEAM_GAMES)
        soup = BeautifulSoup(res.text, "html.parser")
        gameslist_config = soup.find(id="gameslist_config")
        gameslist_dict = json.loads(gameslist_config["data-profile-gameslist"])
        return gameslist_dict

    def RegisterKey(self, gamekey):
        res = self.__session.post(f"https://{STEAM_DOMAIN}{STEAM_REGISTER_KEY_API}", data={"product_key": gamekey,
                                                                                "sessionid": self.__session.cookies.get("sessionid", domain=STEAM_DOMAIN)})
        print(res.status_code)
        rtn_data = res.json()
        print(rtn_data)
        return rtn_data

    def VisitHomePage(self):
        if self.__session:
            print(f"Final URL of visit home page = {self.__session.get(STEAM_MAIN, headers={'User-Agent': self.__user_agent}).url}")

    def GetRSAPublicKey(self):
        print(self.__login)
        rsa_pk_request = Steam_RSA_Public_Key_Request_pb2.SteamRSAPublicKeyRequest()
        rsa_pk_request.account_name = self.__login
        rsa_pk_serialized = rsa_pk_request.SerializeToString()

        payload = { "origin":"https://store.steampowered.com",
                   "input_protobuf_encoded": EncodeProtoBuff(rsa_pk_serialized)
                }
        res = self.__session.get(STEAM_API_DOMAIN + STEAM_PASS_RSA_PUBLIC_KEY_API,
                           params=payload,
                           headers={'User-Agent': self.__user_agent})
        if not res.ok:
            return ""

        rsa_pk_response = Steam_RSA_Public_Key_Request_pb2.SteamRSAPublicKeyResponse()
        #print(res.status_code)
#        res.encoding = "ascii"
        #print(bytes(res.text,"utf-8"))
        #print(res.text)
        #print(res.content)
        #print(len(res.text))
        #print([hex(ord(char_val)) for char_val in res.text])
        #print(len(bytes(res.text,"utf-8")))
        #print([bin(char_val) for char_val in bytes(res.text, "utf-8")])
        #print([char_val for char_val in bytes(res.text, "utf-8")])
        #print(bin(-128))
        #print([bin(ord(char_val)) for char_val in res.text])
        #response_text = res.text 
        #response_text = response_text.replace(response_text[1], chr(512), 1)
      #  print([ord(char_val) for char_val in response_text])
        rsa_pk_response.ParseFromString(res.content)#bytes(response_text, "utf-8"))
        return rsa_pk_response

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
