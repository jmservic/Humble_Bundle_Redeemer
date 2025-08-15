from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN, HumbleClient, LoginResult
import os
from dotenv import load_dotenv
import Steam_RSA_Public_Key_Request_pb2 
from steam_utils import *
from steamclient import SteamClient
from steamlibrary import SteamLibrary
import base64
from time import sleep
from humblelibrary import HumbleLibrary
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

#print(hb.ChooseContent("qqnZwGv4YXWAvdGm", "dcuniverseinfinite_onemonthfreetrial"))
#print(hb.RedeemKey("dccomicsfreetrial_november2023choice_coupon","qqnZwGv4YXWAvdGm"))
#print(steam.GetBundleInfo(38150))#(15367))
#exit(0)
print("Obtaining Order Details")
hb_orders = hb.GetOrdersDetail()
print("Creating the Humble Library Object")
humble_library = HumbleLibrary(hb_orders)
print("Obtaining Unchosen Content")
unchosen_content = humble_library.ChoiceChooseContent()
print("Obtaining Redeemable Content")
redeemable_content = humble_library.ChoiceRedeemableContent()

for order, choose_content in unchosen_content.items():
    print(f"Unchosen Content for {order}")
    for display_name, product_machine_name in choose_content.items():
        print(f"{display_name}, {product_machine_name}")
    print("\n")

for order, redeemable_content in redeemable_content.items():
    print(f"Redeemable Content for {order}")
    for content in redeemable_content:
        print(content)
    print("\n")

steam_keys_on_humble = humble_library.KeysContent(platforms=["steam"])
#exit(0)
#for key, value in hb_orders.items():
#    if value["product"]["category"] == "storefront" and len(value["subproducts"]) > 0:
#        print(key, value["subproducts"])
#exit(0)
#for key, value in hb_orders.items():
#    if "machine_name" not in value["product"].keys():
#        print(key, "\n")
#        continue

#    if value["product"]["machine_name"] == "assassinscreed_bundle": #"april_2021_choice": #in  ["april_2024_choice", "june_2025_choice", "june_2020_choice", "january_2019_monthly", "april_2021_choce"]:
#        print(f'\n{value["product"]["machine_name"]} = {value}\n')

#exit(0)
        
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
#steam_store_cookies = steam.GetSessionCookies().get_dict(domain="store.steampowered.com")
#for cookie in steam_store_cookies.items():
#    print(cookie)
#steam.VisitRegisterKeyPage()
gameslist_config = steam.GetLibraryDetails()
#print(gameslist_config)
licenses_info = steam.GetLicenses()
print(f"Number of games in library: {len(gameslist_config['rgGames'])}")
steam_library = SteamLibrary(gameslist_config, licenses_info)

print(f"Seeing if any keys are possibly unregistered")
unregistered_keys = []
for key_info in steam_keys_on_humble:
    if key_info["platform_id"]:
        found_product = steam_library.ContainsProduct(id=key_info["platform_id"])
        if found_product:
            print(f"Found {key_info['name']} by id in library")
            product_date = steam_library.ProductRegisterDate(id=key_info["platform_id"])
            if not product_date or (key_info["created"].date() - product_date).days > 1:
                print(f"Created after the steam acquisition date, probably not registered steam_date: {product_date} | humble_date: {key_info['created'].date()}")
                unregistered_keys.append(key_info)
        else:
            print(f"Checking if {key_info['name']} is a bundle")
            bundle_data = steam.GetBundleInfo(key_info["platform_id"])
            if bundle_data:
                print(f"{key_info['name']} is a bundle.")
                if steam_library.ContainsBundle(bundle_data):
                    bundle_date = steam_library.BundleRegisterDate(bundle_data)
                    print(f"All bundle products are owned.")
                    if not bundle_date or (key_info["created"] - bundle_date).days > 1:
                        print(f"Most likely used to obtain the bundle.")
                    else:
                        print(f"{key_info['name']} is most likely unregistered")
                        unregistered_keys.append(key_info)
                else:
                    print(f"Not all products of the bundle are owned.")
                    unregistered_keys.append(key_info)
            else:
                print(f"{key_info['name']} is not a bundle. Checking by name.")
                found_product , exact_match = steam_library.ContainsProduct(key_info["name"])
                if found_product:
                    print(f"Found {key_info['name']} with an exact match value of: {exact_match}")
                else:
                    print(f"Didn't Find {key_info['name']}")
                    unregistered_keys.append(key_info)
    else:
        print(f"No steam id for {key_info['name']}, checking by name")
        found_product , exact_match = steam_library.ContainsProduct(key_info["name"])
        if found_product:
            print(f"Found {key_info['name']} with an exact match value of: {exact_match}")
            product_date = steam_library.ProductRegisterDate(key_info["name"])
            if  not product_date or (key_info["created"].date() - product_date).days > 1:
                print(f"Created after the steam acquisition date, probably not registered steam_date: {product_date} | humble_date: {key_info['created'].date()}")
                unregistered_keys.append(key_info)
        else:
            print(f"Didn't Find {key_info['name']}")
            unregistered_keys.append(key_info)
for key_info in unregistered_keys:
    print(key_info)
#print("Keys in gameslist_config:")
#for key in gameslist_config:
#    print(key)
#print("\nKeys in a game item:")
#gameslist = gameslist_config["rgGames"]
#for key in gameslist[0]:
#    print(key)

#for game in gameslist:
#    print(f"\nApp ID: {game['appid']} | Name: {game['name']} | Playtime: {game['playtime_forever']}")
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
