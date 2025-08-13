from libraries.humblelibrary import HumbleLibrary
from libraries.steamlibrary import SteamLibrary
import clients.humbleclient as hc
import clients.steamclient as sc

class HumbleController:

    def __init__(self, humble_client, steam_client, database, interactive=True, dry_run=False):
        self.__hb = humble_client
        self.__steam = steam_client
        self.__db = database
        self.__interactive = interactive
        self.__dry_run = dry_run
        self.__humble_library = None
        self.__steam_library = None

    def ChoseChoiceContent(self): #, skip_owned_games=False):
        if not self.HumbleLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()

        unchosen_content = self.__humble_library.ChoiceChoseContent()
        orders_to_update = []

        for order_key, contents in unchosen_content.items():
            order = humble_library.GetOrder(order_key)
            print(f"Choosing Content for {order.Name()} ({order_key}):")
            choice_made = False

            for content in contents:
                print(f"Choosing {content}...")

                if not self.__dry_run:
                    res = self.__hb.ChooseContent(order_key, content) 

                    if res["success"]:
                        print(f"Successfully chosen {content}.")
                        choice_made = True
                    else:
                        print(f"Failed to chose {content} Message: {res['error_msg]}.")
                    self.__db.Log(order_key, order.Name(), content, "choose", res["success"])

            if choice_made:
                orders_to_update.append(order_key)

        self.UpdateOrders(self.__humble_library, orders_to_update)
        self.__db.SaveHumbleLibrary(self.__humble_library)

    def RedeemChoiceContent(self, skip_owned_games=False):
        if not self.HumbleLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()
        
        if self.__steam_library is None:
            self.__steam_library = self.GetSteamLibrary()

        redeemable_content = self.__humble_library.ChoiceRedeemableContent()
        orders_to_update = []

    def RegisterContent(self):
        pass

    def FullyProcessChoiceContent(self, skip_owned_games=False):
        self.RegisterContent(self.RedeemChoiceContent(skip_owned_games, self.ChoseChoiceContent()))

    def GetHumbleLibrary():
        humble_library = HumbleLibrary.FromOrderRecords(self.__db.GetOrders())

        orders = set(humble_library.GetOrderKeys())
        all_orders = set(self.__hb.GetGameKeys())

        if not orders:
            return HumbleLibrary(self.__hb.GetOrderDetails(all_orders))

        new_orders = all_orders - orders
        self.UpdateOrders(humble_library, orders_to_update)

        return humble_library

    def GetSteamLibrary():
        gameslist_config = self.__steam.GetLibraryDetails()
        licenses_info = self.__steam.GetLicenses()
        steam_library = SteamLibrary(gameslist_config, licenses_info)
        return steam_library

    def HumbleLogin(self):
        login_result = self.__hb.Login()
        counter = 0
        limit = 5 if interactive else 1
        while login_result != LoginResult.SUCCESS and counter < limit:
            match login_result:
                case hc.LoginResult.GUARD:
                    guard = input("Please enter the humble bundle guard code from your email: ")
                    payload = {"guard": guard}
                    login_result = hb.Login(payload)
                case hc.LoginResult.BAD_USERNAME:
                    hb_account = input("Cannot find an account with that name, please enter a new account name: ")
                    hb.Set_Login(hb_account)
                    login_result = hb.Login()
                case hc.LoginResult.BAD_PASSWORD:
                    hb_password = input("Password does not match, please enter a new password: ")
                    hb.Set_Password(hb_password)
                    login_result = hb.Login()
                case hc.LoginResult.BLOCKED:
                    print("Yeah... Cloudflare doesn't like us. Shutting down!")
                    return False
                case hc.LoginResult.TOO_MANY_REQUESTS:
                    print("Too many requests...")
                    return False
            counter += 1
        
        if counter == limit:
            return False

        return True

    def SteamLogin(self):
        self.__steam.Login()
        login_result = self.__steam.GetLoginResult()

        if not interactive and login_result != sc.LoginResult.SUCCESS:
            return False

        while self.__steam.Polling():
            print("Waiting for steam authentication login.")
            sleep(5)

        return self.__steam.GetLoginResult() == sc.LoginResult.SUCCESS

    def UpdateOrders(self, humble_library, orders_to_update):
        update_order_dicts = self.__hb.GetOrderDetails(orders_to_update)
        
        for update_order_dict in update_order_dicts.values():
            humble_library.UpdateOrder(update_order_dict)

        
