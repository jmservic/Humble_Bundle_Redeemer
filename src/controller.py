from libraries.humblelibrary import HumbleLibrary, HumbleStoreKey, HumbleBundle, HumbleChoice
from libraries.steamlibrary import SteamLibrary
import clients.humbleclient as hc
import clients.steamclient as sc
from datetime import datetime
from time import sleep

class HumbleController:

    def __init__(self, humble_client, steam_client, database, interactive=True, dry_run=False):
        self.__hb = humble_client
        self.__steam = steam_client
        self.__db = database
        self.__interactive = interactive
        self.__dry_run = dry_run
        self.__humble_library = None
        self.__steam_library = None
        self.__orders_to_update = set()
        self.__humble_auth = False
        self.__steam_auth = False

    def ChoseChoiceContent(self): #, skip_owned_games=False):
        if not self.__humble_auth and not self.HumbleLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()

        self.__choseChoiceContent()

        self.__updateAndSaveLibrary()

    def __choseChoiceContent(self):
        unchosen_content = self.__humble_library.ChoiceChooseContent()
        for order_key, contents in unchosen_content.items():
            order = self.__humble_library.GetOrder(order_key)
            print(f"Choosing Content for {order.Name()} ({order_key}):")
            choice_made = False
            for display_name, machine_names in contents.items():
                print(f"\tChoosing {display_name}...")

                if not self.__dry_run:
                    res = self.__hb.ChooseContent(order_key, display_name) 

                    if res["success"]:
                        print(f"\tSuccessfully chosen {display_name}.")
                        choice_made = True
                    else:
                        print(f"\tFailed to chose {display_name} Message: {res['error_msg']}.")

                    self.__db.Log(order_key, order.Name(), display_name, "choose", res["success"])

                else:
                    self.__db.Log(order_key, order.Name(), display_name, "choose_dry_run", True)

            print("")
            if choice_made:
                self.__orders_to_update.add(order_key)

    def RedeemChoiceContent(self, skip_owned_games=False):
        if not self.__humble_auth and not self.HumbleLogin():
            return

        if skip_owned_games and not self.__steam_auth and not self.SteamLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()
        
        if skip_owned_games and self.__steam_library is None:
            self.__steam_library = self.GetSteamLibrary()

        self.__redeemChoiceContent(skip_owned_games)

        self.__updateAndSaveLibrary()

    def __redeemChoiceContent(self, skip_owned_games=False):
        redeemable_content = self.__humble_library.ChoiceRedeemableContent()
        register_content = []

        for order_key, contents in redeemable_content.items():
            products = self.__humble_library.GetOrder(order_key).Products()
            redeemed_product = False
            for product_machine_name in contents:
                product = next(filter(lambda x: x.ProductMachineName() == product_machine_name , products))
                print(f"Redeeming {product.Name()} ({product_machine_name})")

                if skip_owned_games and not self.__proceedWithAction(product.Name(), product.KeyType(), product.PlatformId(), "redeeming"):
                    if not self.__dry_run:
                        self.__db.SaveGift(product)
                    continue

                if self.__dry_run:
                    self.__db.Log(order_key, product.Name(), product_machine_name, "redeem_dry_run", True)
                    res = {"success": True, "key": "Fake_News"}
                else:
                    attempts = 1
                    res = self.__hb.RedeemKey(order_key, product_machine_name)

                    while not res["success"] and attempts < 4:
                        res = self.__hb.RedeemKey(order_key, product_machine_name)
                        attempts += 1

                if not res["success"]:
                    print(f"\tFailed to redeem {product.Name()} ({product_machine_name}). Message: {res['error_msg']}")
                else:              
                    print(f"\tSuccessfully redeemed {product.Name()} ({product_machine_name}).")
                    redeemed_product = True
                    register_content.append({"key": res["key"],
                                 "key_type": product.KeyType(),
                                 "platform_id": product.PlatformId(),
                                 "name": product.Name(),
                                 "created": product.Created(),
                                 "expired": product.Expired(),
                                 "registered": product.Registered(),
                                 "humble_key": product.Key()
                                             })
                if not self.__dry_run:
                    self.__db.Log(order_key, product.Name(), product_machine_name, "redeem", res["success"])
                    self.__db.SaveRedeemAttempt(order_key, product.Name(), product_machine_name, datetime.now(), res["success"])

            if redeemed_product:
                self.__orders_to_update.add(order_key)
            print("")

        return register_content

    def RegisterContent(self):
        if not self.__humble_auth and not self.HumbleLogin():
            return

        if not self.__steam_auth and not self.SteamLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()
        
        if self.__steam_library is None:
            self.__steam_library = self.GetSteamLibrary()

        self.__registerContent(self.__humble_library.KeysContent(["steam"]))

        print("Saving Library to Database...")
        self.__db.SaveHumbleLibrary(self.__humble_library)

    def __registerContent(self, register_content):
        for product_dict in register_content:
            if (product_dict["expired"] or product_dict["registered"] 
            or not product_dict["key"] or "steam" not in product_dict["key_type"]):
                if self.__dry_run: 
                    print(f"""Skipping {product_dict['name']}. Key={product_dict['key']} | Expired={product_dict['expired']}
                           | Registered={product_dict['registered']} | Key Type={product_dict['key_type']}\n""")
                continue

            order = self.__humble_library.GetOrder(product_dict["humble_key"])

            if isinstance(order, HumbleStoreKey):
                product = order
            else:
                products = order.Products() 
                product = next(filter(lambda x: x.Name() == product_dict["name"] , products))

            if product.PlatformId() != product_dict["platform_id"]:
                raise Exception("Definitely didn't find the right product when registering!")

            bundle_info = None
            print(f"Registering {product.Name()} ({product.ProductMachineName()})")

            if "steam" in product_dict["key_type"] and not self.__proceedWithAction(product_dict["name"],
                                                                                    product_dict["key_type"],
                                                                                    product_dict["platform_id"],
                                                                                    "registering",
                                                                                    bundle_info):
                if bundle_info:
                    date = self.__steam_library.BundleRegisterDate(bundle_info)
                    aq_method = self.__steam_library.BundleAcquisitionMethod(bundle_info)
                else:
                    date = self.__steam_library.ProductRegisterDate(title=product_dict["name"], id=product_dict["platform_id"])
                    aq_method = self.__steam_library.ProductAcquisitionMethod(title=product_dict["name"], id=product_dict["platform_id"])

                if aq_method != "retail" or (date and (product_dict["created"].date() - date).days > 1):
                    print(f"\tacquisiton method : {aq_method} | { (product_dict['created'].date() - date).days if date else 'unknown'} day difference between order creation and steam activation dates.")
                    print(f"\tSaving {product_dict['name']} as a gift.")
                    if not self.__dry_run:
                        self.__db.SaveGift(product)
                    print("")
                    continue

                if not date:
                    print(f"\tCouldn't find an exact date for the product, assuming it has been registered.")

                print(f"\tSetting {product.Name()}'s Registered flag")
                
                if not self.__dry_run:
                    self.__humble_library.SetProductRegistered(product_dict["humble_key"], product.ProductMachineName()) 

                print("")
                continue

            if self.__dry_run:
                print("")
                continue

            res = self.__steam.RegisterKey(product_dict["key"])

            if res["success"] == 1:
                print(f"\tRegistered {product.Name()} ({product.ProductMachineName()}")
                self.__humble_library.SetProductRegistered(product_dict["humble_key"], product.ProductMachineName()) 
                self.__db.Log(product.Key(), product.Name(), product.ProductMachineName(), "register", True)
            else:
                error_code = res["\tpurchase_receipt_info"]["result_detail"]
                match error_code:
                    case 9:
                        print(f"\tThis Steam account already owns the product. Assuming the key was used.")
                        self.__humble_library.SetProductRegistered(product_dict["humble_key"], product.ProductMachineName()) 
                    case 14:
                        print(f"\tKey is not valid or is not a product code.")
                    case 15:
                        print(f"\tKey has already been activated by another account.")
                        self.__humble_library.SetProductRegistered(product_dict["humble_key"], product.ProductMachineName()) 
                    case 53:
                        print(f"\tThere have been too many recent activation attempts from this account or Internet address.")


                self.__db.Log(product.Key(), product.Name(), product.ProductMachineName(), "register", error_code)
                if error_code == 53:
                    return
            print("")

    def FullyProcessChoiceContent(self, skip_owned_games=False, all_keys=False):
        if not self.__humble_auth and not self.HumbleLogin():
            return

        if not self.__steam_auth and not self.SteamLogin():
            return

        if self.__humble_library is None: 
            self.__humble_library = self.GetHumbleLibrary()
        
        if self.__steam_library is None:
            self.__steam_library = self.GetSteamLibrary()

        self.ChoseChoiceContent()
        register_content = self.__redeemChoiceContent(skip_owned_games)
        self.UpdateOrders(self.__humble_library)

        if all_keys:
            register_content.extend(self.__humble_library.ChoiceKeyContent(["steam"]))

        self.__registerContent(register_content)
        self.__updateAndSaveLibrary()


    def __updateAndSaveLibrary(self):
        print("Updating Orders in Library...")
        self.UpdateOrders(self.__humble_library)

        print("Saving Library to Database...")
        self.__db.SaveHumbleLibrary(self.__humble_library)

    def __proceedWithAction(self, name, key_type, platform_id, action, bundle_info=None):
        if "steam" not in key_type:
            return True

        contains, exact_match = self.__steam_library.ContainsProduct(name, platform_id)

        if exact_match:
            print(f"\tFound product in steam library, skipping.")
            return False

        if not platform_id:
            print(f"\tDid not not find in steam library. Product is missing steam Id to check for bundles.")
            return True

        print(f"\tChecking if {name} is a bundle...")
        bundle_info = self.__steam.GetBundleInfo(platform_id)
        if bundle_info:
            print(f"\t{name} is a bundle. Checking if all ids are owned.")
            if not self.__steam_library.ContainsBundle(bundle_info):
                print(f"\tMissing ids from the bundle, {action}.")
                return True
            else:
                print("\tFully owned bundle, skipping.")
                return False
        else:
            print(f"\t{name} is not a bundle, {action}.")
            return True

    def RefreshLibrary(self):
        self.__humble_library = HumbleLibrary.FromOrderRecords(self.__db.GetOrders())
        self.__orders_to_update.update(self.__hb.GetGameKeys())
        self.__updateAndSaveLibrary()

    def GetHumbleLibrary(self):
        humble_library = HumbleLibrary.FromOrderRecords(self.__db.GetOrders())

        orders = set(humble_library.GetOrderKeys())
        all_orders = set(self.__hb.GetGameKeys())

        if not orders:
            return HumbleLibrary(self.__hb.GetOrdersDetails(list(all_orders)))

        new_orders = all_orders - orders
        self.__orders_to_update.update(new_orders)
        self.UpdateOrders(humble_library)

        return humble_library

    def GetSteamLibrary(self):
        gameslist_config = self.__steam.GetLibraryDetails()
        licenses_info = self.__steam.GetLicenses()
        steam_library = SteamLibrary(gameslist_config, licenses_info)
        return steam_library

    def HumbleLogin(self):
        print("Logging into Humble Bundle.")
        login_result = self.__hb.Login()
        if not self.__interactive and login_result != hc.LoginResult.SUCCESS:
            return False

        counter = 0
        limit = 5
        while login_result != hc.LoginResult.SUCCESS and counter < limit:
            match login_result:
                case hc.LoginResult.GUARD:
                    guard = input("Please enter the humble bundle guard code from your email: ")
                    payload = {"guard": guard}
                    login_result = self.__hb.Login(payload)
                case hc.LoginResult.BAD_USERNAME:
                    hb_account = input("Cannot find an account with that name, please enter a new account name: ")
                    hb.Set_Login(hb_account)
                    login_result = self.__hb.Login()
                case hc.LoginResult.BAD_PASSWORD:
                    hb_password = input("Password does not match, please enter a new password: ")
                    hb.Set_Password(hb_password)
                    login_result = self.__hb.Login()
                case hc.LoginResult.BLOCKED:
                    print("Yeah... Cloudflare doesn't like us. Shutting down!")
                    return False
                case hc.LoginResult.TOO_MANY_REQUESTS:
                    print("Too many requests...")
                    return False
            counter += 1
        
        if counter == limit:
            return False

        self.__humble_auth = True
        return True

    def SteamLogin(self):
        print("Logging into Steam.")
        self.__steam.Login()
        login_result = self.__steam.GetLoginResult()

        if not self.__interactive and login_result != sc.LoginResult.SUCCESS:
            self.__steam.EndPolling()
            return False

        while self.__steam.Polling():
            print("Waiting Steam to authenticate.")
            sleep(5)
        
        if self.__steam.GetLoginResult() == sc.LoginResult.SUCCESS:
            self.__steam_auth = True
        
        return self.__steam_auth

    def UpdateOrders(self, humble_library):
        update_order_dicts = self.__hb.GetOrdersDetails(list(self.__orders_to_update))
        
        for update_order_dict in update_order_dicts.values():
            humble_library.UpdateOrder(update_order_dict)

        self.__orders_to_update.clear()
