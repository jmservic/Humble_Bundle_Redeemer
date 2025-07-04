from requests import Request, Session
from http.cookiejar import MozillaCookieJar
from humbleclient import HUMBLE_MAIN, HumbleClient, LoginResult
import os
from dotenv import load_dotenv
#We're going to use the pickle module to save and load the cookies.
load_dotenv()
hb_account = os.getenv("HB_ACCOUNT")
hb_password = os.getenv("HB_PASSWORD")

if not os.path.exists("./cookies"):
    os.mkdir("./cookies")
hb = HumbleClient(login=hb_account,password=hb_password)

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

#hb.GetOrdersDetail()
game_data_dict = hb.GetChoiceDetails("april-2025")
for key in game_data_dict.keys():
    print(key)
print()

for key in game_data_dict["dredge"].keys():
    print(key)
    
print()

for key in game_data_dict["novalands"]["tpkds"][0].keys():
    print(key)

print( game_data_dict["novalands"]["tpkds"])
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
