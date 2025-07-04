from abc import ABC, abstractmethod
from requests import Session 
from requests.cookies import cookiejar_from_dict, create_cookie, morsel_to_cookie
import pickle
from os.path import exists
from time import sleep
import http.client, urllib.parse
#import http.cookies
from http_utils import SetCookieHeaderToMorsels 
from enum import Enum
import json
from bs4 import BeautifulSoup

HUMBLE_DOMAIN = "www.humblebundle.com"
HUMBLE_MAIN = "https://www.humblebundle.com/"
HUMBLE_KEYS = "https://www.humblebundle.com/home/keys"
HUMBLE_LOGIN = "https://www.humblebundle.com/login"
HUMBLE_LOGIN_API = "http://localhost:1234/processlogin"#"https://www.humblebundle.com/processlogin"
HUMBLE_PROCESS_LOGIN = "/processlogin"
HUMBLE_ORDER_API = "https://www.humblebundle.com/api/v1/orders"
HUMBLE_CHOOSE_API = "/humbler/choosecontent"
HUMBLE_REDEEMKEY_API = "/humbler/redeemkey"
HUMBLE_CHOICE = "https://www.humblebundle.com/membership/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"

class LoginResult(Enum):
    SUCCESS = 0
    GUARD = 1
    BAD_USERNAME = 2
    BAD_PASSWORD = 3
    TWO_FACTOR = 4
    BLOCKED = 5
    TOO_MANY_REQUESTS = 6

class GameKeyClient(ABC):

    @abstractmethod
    def Login(self, login, password):
        pass

    @abstractmethod
    def GetOrdersDetail(self):
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

        if not HUMBLE_LOGIN in response.url:
            print("Already Logged In")
            self.__loggedIn = True
            return (True, None)

        #Using http.client because Cloudflare continues to block the requests-module for processlogin requests
        conn = http.client.HTTPSConnection(HUMBLE_DOMAIN)

        headers = {"Csrf-Prevention-Token": self.__session.cookies["csrf_cookie"]
                   , "User-Agent": USER_AGENT
                   , "Cookie": self.__CookieString()
                   , "Content-type": "application/x-www-form-urlencoded"
                   }

        if not payload:
            payload = {}

        payload["goto"] = "/home/keys"
        payload["password"] = self.__password
        payload["username"] = self.__login
        payload["qs"] = "reason=secureArea"
        payloadStr = urllib.parse.urlencode(payload)

        conn.request("POST", HUMBLE_PROCESS_LOGIN, payloadStr, headers)
        res = conn.getresponse()
        data = res.read()
        responseHeaders = res.getheaders()

        morsels = SetCookieHeaderToMorsels(responseHeaders)
        for morsel in morsels.values():
            self.__session.cookies.set_cookie(morsel_to_cookie(morsel))
        
        conn.close()
        return self.__ValidateLoginRequest(res.status, res.reason, data.decode("utf-8"))

    def GetOrdersDetail(self):
        gamekeys = self.__GetGameKeys()#['nmZqeAmGSpFWTWs4']#['A7CESV6Pp4ZWFarX']
        #["qyK3DHE65xGZTzMa", "8tHd5em7weh8u7wc", "Z8KftUKAEf8zG7zY", "8uBEqKBAtNcbtnYu", "XSrTR7atKHTUVkTf"]  
        order_details = self.__QueryOrders(gamekeys)
        for (gamekey, order_info) in order_details.items():
            #print(f"{gamekey} is {order_info['product']['machine_name']}.")
            #print(f"It's category is {order_info['product']['category']}")
            #if "subscription" in order_info["product"]["category"]:
            #   print(f"Has choice URL? {'choice_url' in order_info['product']}")
            if "choice_url" in order_info["product"]:
                #print(order_info)
                choice_details = self.GetChoiceDetails(order_info["product"]["choice_url"])
                #all_products_details = {}
                #for (name, game_info) in choice_details.items():
                    #print(game_info)
                #    print(name)
                    #I'm going to move this into a domain class
                    #if "tpkds" not in game_info:
                    #    print(game_info)
                    #    continue
                    #product_details = {}
                    #product_details["machine_name"] = game_info["tpkds"][0]["machine_name"]
                    #product_details["human_name"] = game_info["tpkds"][0]["human_name"]
                    #product_details["key_type"] = game_info["tpkds"][0]["key_type"]
                    #if "steam_app_id" in game_info["tpkds"][0]:
                    #    product_details["steam_app_id"] = game_info["tpkds"][0]["steam_app_id"]
                    #all_products_details[game_info["display_item_machine_name"]] = product_details
                #print(all_products_details)
                order_info["product"]["all_choices"] = choice_details#all_products_details
        #print(order_details)
        return order_details

    def __GetGameKeys(self):
        #Need to add in error handling
        response = self.__session.get(HUMBLE_KEYS, headers={"User-Agent": USER_AGENT})
        if not response.ok:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        user_json = soup.find(id="user-home-json-data").text 
        user_json_dict = json.loads(user_json)
        return user_json_dict["gamekeys"]

    def __QueryOrders(self, gamekeys):
        order_details = {}
        start = 0
        end = 0
        while start < len(gamekeys):
            end = start + 40 if start + 40 < len(gamekeys) else len(gamekeys)
            params = [("gamekeys", gamekey) for gamekey in gamekeys[start:end]]
            params.insert(0, ("all_tpkds", "true"))
            print(f"Requesting for {end - start} keys.")
            response = self.__session.get(HUMBLE_ORDER_API, params=params, headers={"User-Agent": USER_AGENT})
            if response.ok:
                print("Request was successful.")
                order_details.update(response.json())
            else:
                print("Request failed.")
            start = end
        
        return order_details
        
    def GetChoiceDetails(self, choice_url):
        response = self.__session.get(HUMBLE_CHOICE + choice_url, headers={"User-Agent": USER_AGENT})
        if not response.ok:
            return {}
        soup = BeautifulSoup(response.text, "html.parser")
        monthly_json = soup.find(id="webpack-monthly-product-data").text
        monthly_json_dict = json.loads(monthly_json)
        #This is also being moved into a domain class lol
        #choice_data = monthly_json_dict["contentChoiceOptions"]["contentChoiceData"]
        #print(choice_data)
        #if "game_data" in choice_data:
        #    game_data_dict = choice_data["game_data"]
        #else:
        #    game_data_dict = choice_data["initial"]["content_choices"]
        # 
        #game_data_dict = monthly_json_dict["contentChoiceOptions"]["contentChoiceData"]["game_data"]
        return monthly_json_dict
        

    def ChooseContent(self, gamekey, identifiers):
        payload = [("gamekey", gamekey),
                   ("parent_identifier", "initial"),
                   ("is_gift", "false")
                  ]
        if type(identifiers).__name__ == "list":
            print([("chosen_identifiers[]", identifier) for identifier in identifiers])
            payload += [("chosen_identifiers[]", identifier) for identifier in identifiers]
        else:
            payload.append(("chosen_identifiers[]", identifiers))
        
        conn = http.client.HTTPSConnection(HUMBLE_DOMAIN)
        
        headers = {"Csrf-Prevention-Token": self.__session.cookies["csrf_cookie"]
                   , "User-Agent": USER_AGENT
                   , "Cookie": self.__CookieString()
                   , "Content-type": "application/x-www-form-urlencoded"
                   }
        payloadStr = urllib.parse.urlencode(payload)
        #print(payload)
        #print(payloadStr)
        
        conn.request("POST", HUMBLE_CHOOSE_API, payloadStr, headers)
        res = conn.getresponse()
        data = res.read()
        responseHeaders = res.getheaders()

        morsels = SetCookieHeaderToMorsels(responseHeaders)
        for morsel in morsels.values():
            self.__session.cookies.set_cookie(morsel_to_cookie(morsel)) 
        #response = self.__session.post(HUMBLE_CHOOSE_API, data=payload, headers={"User-Agent": USER_AGENT}) 
        #print(res.status)
        
        #print(data.decode("utf-8"))
        conn.close()
        return json.loads(data.decode("utf-8"))


    def RedeemKey(self, keytype, gamekey, keyindex=0):
        payload = [("keytype", keytype),
                   ("key", gamekey),
                   ("keyindex", keyindex)
                   ]

        conn = http.client.HTTPSConnection(HUMBLE_DOMAIN)

        headers = {"Csrf-Prevention-Token": self.__session.cookies["csrf_cookie"]
                   , "User-Agent": USER_AGENT
                   , "Cookie": self.__CookieString()
                   , "Content-type": "application/x-www-form-urlencoded"
                   }
        payloadStr = urllib.parse.urlencode(payload) 
        conn.request("POST", HUMBLE_REDEEMKEY_API, payloadStr, headers)
        res = conn.getresponse()
        data = res.read()
        responseHeaders = res.getheaders()

        morsels = SetCookieHeaderToMorsels(responseHeaders)
        for morsel in morsels.values():
            self.__session.cookies.set_cookie(morsel_to_cookie(morsel))
        conn.close()
       # print(res.status)
       # print(data.decode("utf-8"))
        return json.loads(data.decode("utf-8"))

    def Set_Login(self, login):
        self.__login = login

    def Set_Password(self, password):
        self.__password = password

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

    def __ValidateLoginRequest(self, status, reason, data):
        #print(status)
        #print(reason)
        #print(data)
        match status:
            case 200:
                return LoginResult.SUCCESS
            case 401:
                json_data = json.loads(data)
                #print(json_data["errors"]["username"])
                if "humble_guard_required" in json_data.keys() and json_data["humble_guard_required"]:
                    return LoginResult.GUARD
                if "errors" in json_data.keys() and "username" in json_data["errors"].keys():
                    errors = json_data["errors"]["username"]
                    for error in errors:
                        if "can't find an account" in error:
                            return LoginResult.BAD_USERNAME
                        if "don't match" in error:
                            return LoginResult.BAD_PASSWORD
            case 403:
                return LoginResult.BLOCKED
            case 429:
                return LoginResult.TOO_MANY_REQUESTS
        raise ValueError(f"Unknown combination of status, reason, and data response from HumbleBundle Login Request:\nstatus={status}\nreason={reason}\ndata={data}")
                
            
    
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
    

