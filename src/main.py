from database import Database
from clients.humbleclient import HumbleClient
from clients.steamclient import SteamClient
import os
from dotenv import load_dotenv
from controller import HumbleController

load_dotenv()
hb_account = os.getenv("HB_ACCOUNT")
hb_password = os.getenv("HB_PASSWORD")
steam_account = os.getenv("STEAM_ACCOUNT")
steam_password = os.getenv("STEAM_PASSWORD")

if not os.path.exists("../cookies"):
    os.mkdir("../cookies")

hb = HumbleClient(login=hb_account,password=hb_password)
steam = SteamClient(login=steam_account,password=steam_password)
db = Database("./humble.db")
db.Initialize()

#try:
controller = HumbleController(hb, steam, db, True, True)
#controller.RegisterContent()
controller.FullyProcessChoiceContent()
#except Exception as e:
#    print(e)
#finally:
#    db.close()

