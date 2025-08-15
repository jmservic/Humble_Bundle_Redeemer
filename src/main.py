from database import Database
from clients.humbleclient import HumbleClient
from clients.steamclient import SteamClient
import os
import argparse
from dotenv import load_dotenv
from controller import HumbleController

def App():
    load_dotenv()
    hb_account = os.getenv("HB_ACCOUNT")
    hb_password = os.getenv("HB_PASSWORD")
    steam_account = os.getenv("STEAM_ACCOUNT")
    steam_password = os.getenv("STEAM_PASSWORD")

    if not os.path.exists("./cookies"):
        os.mkdir("./cookies")

    if not os.path.exists("./data"):
        os.mkdir("./data")

    parser = argparse.ArgumentParser(
                        prog="hbredeemer",
            description="This program automatically chooses, redeems, and register steam keys from Humble Bundle.",
            epilog="""The redeem, register, and run actions will also save any already owned games to the Giftable table
            in the sqlite database located in the data directory.""")
    parser.add_argument("action",
                        default="",
                        choices=["choose", "redeem", "register", "refresh", "run"],
                        help="""The action that %(prog)s will perform. 
                        choose: Checks all Choice Bundles for unclaimed products and claims them.
                        redeem: Checks all Choice Bundles for redeemable claimed products and redeems them. 
                        When the [-s | --skip-owned-games] flag is set. It will skip any products that 
                        are already in your Steam library.
                        register: Checks All Orders for unregistered Steam Keys and redeems them. 
                        **Work in Progress: Improvement to the Steam Library Matching Logic**
                        run: chooses, redeems, and registers Choice products.""")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Allows interaction with User. This is necessary to log into Humble Bundle and Steam.")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="""Performs a dry-run of the action. The application will not attempt to choose, redeem, 
                        or register products.""")
    parser.add_argument("-s", "--skip-owned-games", action="store_true",
                        help="When Redeeming skips games that it finds in the your Steam library.")
    parser.add_argument("-a", "--all-keys", action="store_true",
                        help="""When performing the 'run' action, %(prog)s additionally pulls all Steam Keys
                        from your Humble library and registers any that aren't expired, registered, or in your Steam library.
                        """)
    namespace = parser.parse_args()

    hb = HumbleClient(login=hb_account,password=hb_password)
    steam = SteamClient(login=steam_account,password=steam_password)
    db = Database("./data/humble.db")
    db.Initialize()
    controller = HumbleController(hb, steam, db, namespace.interactive, namespace.dry_run)

    match namespace.action:
        case "run":
            controller.FullyProcessChoiceContent(namespace.skip_owned_games, namespace.all_keys)
        case "choose":
            controller.ChoseChoiceContent()
        case "redeem":
            controller.RedeemChoiceContent(namespace.skip_owned_games)
        case "register": 
            controller.RegisterContent()
        case "refresh":
            controller.RefreshLibrary()

if __name__ == "__main__":
    App()
