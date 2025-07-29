from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN, HumbleClient, LoginResult
import os
from dotenv import load_dotenv
import Steam_RSA_Public_Key_Request_pb2 
from steam_utils import *
from steamclient import SteamClient
import base64
from time import sleep
#We're going to use the pickle module to save and load the cookies.
load_dotenv()
hb_account = os.getenv("HB_ACCOUNT")
hb_password = os.getenv("HB_PASSWORD")
steam_account = os.getenv("STEAM_ACCOUNT")
steam_password = os.getenv("STEAM_PASSWORD")

if not os.path.exists("./cookies"):
    os.mkdir("./cookies")
hb = HumbleClient(login=hb_account,password=hb_password)
steam = SteamClient(login=steam_account,password=steam_password)
#print(f"Cookies before request to humble bundle main page:")
#hb_cookies = hb.GetSessionCookies()
#for cookie in hb_cookies:
#    print(cookie)

#hb.VisitHomePage()
#hb_cookies = hb.GetSessionCookies()
#print(f"Cookies after request to humble bundle main page:")
#for (cookie_name, cookie_value) in dict(hb_cookies).items():
#    print(cookie_name, cookie_value)
#print("")
#print(hb_cookies.get("_simpleauth_sess"))
#for cookie in hb_cookies:
#    print(cookie.domain)

login_result = hb.Login()
counter = 0

while login_result != LoginResult.SUCCESS and counter < 5:
    match login_result:
        case LoginResult.GUARD:
            guard = input("Please enter the humble bundle guard code from your email: ")
            payload = {"guard": guard}
            login_result = hb.Login(payload)
        case LoginResult.BAD_USERNAME:
            hb_account = input("Cannot find an account with that name, please enter a new account name: ")
            hb.Set_Login(hb_account)
            login_result = hb.Login()
        case LoginResult.BAD_PASSWORD:
            hb_password = input("Password does not match, please enter a new password: ")
            hb.Set_Password(hb_password)
            login_result = hb.Login()
        case LoginResult.BLOCKED:
            print("Yeah... Cloudflare doesn't like us. Shutting down!")
            exit(1)
        case LoginResult.TOO_MANY_REQUESTS:
            print("Too many requests...")
            exit(1)
    counter += 1

#hb_orders = hb.GetOrdersDetail()
#category_set = set()
#for order in hb_orders.values():
#    category_set.add(order["product"]["category"])

#print(category_set)
#exit(0)
#print(hb.ChooseContent("rw3m6TUnb3eqmHzM", "tchia"))#["nobodywantstodie", "dungeonsofhinterberg"]))
#print(hb.RedeemKey("dungeonsofhinterberg_choice_steam", "rw3m6TUnb3eqmHzM"))
print(hb.RedeemKey("fashionpolicesquad_choice_steam", "Z8KftUKAEf8zG7zY"))
#print(hb.RedeemKey("tchia_row_choice_steam", "rw3m6TUnb3eqmHzM"))

#Out of choices
#print(hb.ChooseContent("qdxHRf4bHywuMfd2", "sigmatheory_globalcoldwar"))
#rsa_pk_request = Steam_RSA_Public_Key_Request_pb2.SteamRSAPublicKeyRequest()
#rsa_pk_request.account_name = "Jmarcus2004"
#rsa_pk_serialized = rsa_pk_request.SerializeToString()
#print(rsa_pk_serialized)
#print(" ".join([str(b_val) for b_val in rsa_pk_serialized]))
#print(EncodeProtoBuff(rsa_pk_serialized))
#print(f"Steam RSA Public Key Request return: {steam.GetRSAPublicKey()}") 
print(f"Steam Login Request return: {steam.Login()}") 
while steam.Polling():
    print("Waiting for steam authentication login")
    sleep(5)
#steam_cookies = steam.GetSessionCookies()
#for cookie in steam_cookies.items():
#    print(cookie)
gameslist_config = steam.GetLibraryDetails()
exit(0)
print(f"Number of games in library: {len(gameslist_config['rgGames'])}")
print("Keys in gameslist_config:")
for key in gameslist_config:
    print(key)
print("\nKeys in a game item:")
gameslist = gameslist_config["rgGames"]
for key in gameslist[0]:
    print(key)

for game in gameslist:
    print(f"\nApp ID: {game['appid']} | Name: {game['name']} | Playtime: {game['playtime_forever']}")
#print(f"Steam cookies {steam.GetSessionCookies()}")
#steam.RegisterKey("LDGZQ-WPB90-KDAPG")
#{base64.b64encode(steam.GetRSAPublicKey().encode('utf-8')).decode('utf-8')}")
#print(f"Steam PollAuthSession return: {steam.PollAuthSessionStatus(10453852608360995313, bytes([86, 83, 229, 143, 204, 46, 235, 192, 31, 128, 168, 124,234, 8, 150, 66]) )}")
exit(0)
game_data_dict = hb.GetChoiceDetails("june-2025")
for key in game_data_dict["contentChoiceOptions"]["contentChoiceData"]["game_data"]:
    print(key)
print()

for key in game_data_dict["dredge"].keys():
    print(key)
    
print()

for key in game_data_dict["novalands"]["tpkds"][0].keys():
    print(key)
print( game_data_dict["novalands"]["tpkds"])
print()
print(hb.GetChoiceDetails("may-2022")["commandconquerremasteredcollection"]["tpkds"])
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
