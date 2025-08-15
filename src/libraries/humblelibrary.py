from datetime import datetime
import json

PLATFORMS = ["steam", "epic", "uplay", "origin", "generic"]

class OrderFactory():
    
    def CreateOrder(self, order_dict):
        category = order_dict["product"]["category"]
        match category:
            case "storefront":
                order_info_dict = {"gamekey": order_dict["gamekey"], "created": order_dict["created"], "subproducts": order_dict["subproducts"]}
                order_info_dict.update(order_dict["product"])
                product_dict = order_dict["tpkd_dict"]["all_tpks"][0] if order_dict["tpkd_dict"]["all_tpks"] else {}
                order = self.CreateStoreKeyOrder(order_info_dict, product_dict)
            case "subscriptionplan" | "subscriptioncontent":
                order_info_dict = {"gamekey": order_dict["gamekey"], 
                                   "created": order_dict["created"],
                                   "choices_remaining": order_dict["choices_remaining"],
                                   "subproducts": order_dict["subproducts"],
                                   "total_choices": order_dict["total_choices"]
                                   }
                order_info_dict.update(order_dict["product"])
                order = self.CreateChoiceOrder(order_info_dict, order_dict["tpkd_dict"]["all_tpks"])
            case "bundle":
                order_info_dict = {"gamekey": order_dict["gamekey"],
                                   "created": order_dict["created"],
                                   "subproducts": order_dict["subproducts"]                                  
                                   }
                order_info_dict.update(order_dict["product"])
                order = self.CreateBundleOrder(order_info_dict, order_dict["tpkd_dict"]["all_tpks"])
            case _:
                raise ValueError(f"HumbleBundle order category '{category}' is an unknown category type.")
        return order
    
    def CreateOrderFromRecords(self, records_dict):
        product_dicts = []
        storekey_order_dict = None
        for storekey_row in records_dict["StoreKeys"]:
            storekey_order_dict = {"gamekey": storekey_row[0],
                                  "machine_name": storekey_row[2],
                                  "created": storekey_row[3],
                                  "subproducts": storekey_row[5],
                                   "human_name": storekey_row[1]
                                   }
            storekey_product_dict = {"human_name": storekey_row[1],
                                     "machine_name": storekey_row[4],
                                     "redeemed_key_val": storekey_row[6],
                                     "key_type": storekey_row[7],
                                     "key_index": storekey_row[8],
                                     "steam_app_id": storekey_row[9],
                                     "expiration_date": storekey_row[10],
                                     "registered": bool(storekey_row[11])
                                     }
            product_dicts.append(storekey_product_dict)
        
        if records_dict["HumbleChoice"]:
            choice_row = records_dict["HumbleChoice"]
            choice_order_dict = {"gamekey": choice_row[0],
                                 "human_name": choice_row[1],
                                 "machine_name": choice_row[2],
                                 "created": choice_row[3],
                                 "subproducts": json.loads(choice_row[4]),
                                 "choices_remaining": choice_row[5],
                                 "all_choices": json.loads(choice_row[6]),
                                 "total_choices": 0
                                 }
            return self.CreateChoiceOrder(choice_order_dict, product_dicts)

        if records_dict["HumbleBundle"]:
            bundle_row = records_dict["HumbleBundle"]
            bundle_order_dict = {"gamekey": bundle_row[0],
                                 "human_name": bundle_row[1],
                                 "machine_name": bundle_row[2],
                                 "created": bundle_row[3],
                                 "subproducts": json.loads(bundle_row[4])
                                 }
            return self.CreateBundleOrder(bundle_order_dict, product_dicts)


        return self.CreateStoreKeyOrder(storekey_order_dict, product_dicts[0])

    def CreateStoreKeyOrder(self, order_dict, product_dict):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": product_dict.get("human_name", order_dict["human_name"]),
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "subproducts": order_dict["subproducts"],
                     "product_machine_name": product_dict.get("machine_name", order_dict["machine_name"]),
                     "redeem_key": product_dict.get("redeemed_key_val", None),
                     "key_type": product_dict.get("key_type", None),
                     "platform_id": product_dict.get("steam_app_id", None),
                     "keyindex": product_dict.get("keyindex", None),
                     "expiration_date": product_dict.get("expiration_date", None),
                     "registered": product_dict.get("registered", False)
                     }
        return HumbleStoreKey(init_dict)

    def CreateChoiceOrder(self, order_dict, product_dicts):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": order_dict["human_name"],
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "choices_remaining": order_dict["choices_remaining"],
                     "total_choices": order_dict["total_choices"],
                     "subproducts": order_dict["subproducts"],
                     "all_choices": order_dict.get("all_choices", None)
                     }
        product_order_dict = {}
        product_order_dict.update(order_dict)
        product_order_dict["subproducts"] = []
        products = [self.CreateStoreKeyOrder(product_order_dict, product_dict) for product_dict in product_dicts]
        return HumbleChoice(init_dict, products)

    def CreateBundleOrder(self, order_dict, product_dicts):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": order_dict["human_name"],
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "subproducts": order_dict["subproducts"]
                    }
        product_order_dict = {}
        product_order_dict.update(order_dict)
        product_order_dict["subproducts"] = []
        products = [self.CreateStoreKeyOrder(product_order_dict, product_dict) for product_dict in product_dicts]
        return HumbleBundle(init_dict, products)

class HumbleLibrary():

    def __init__(self, orders_dict):
        self.__store_keys = {}
        self.__bundles = {}
        self.__choice_bundles = {}
        self.__platforms = PLATFORMS

        order_factory = OrderFactory()
        for (key, order_dict) in orders_dict.items():
            order = order_factory.CreateOrder(order_dict)
            self.__insertOrder(key, order)

    @classmethod
    def FromOrderRecords(cls, order_records):
        library = HumbleLibrary({})
        order_factory = OrderFactory()
        for key, records_dict in order_records.items():
            library.__insertOrder(key, order_factory.CreateOrderFromRecords(records_dict))

        return library

    def ChoiceChooseContent(self):
        unchosen_content_dict = {}

        for humblekey, choice_bundle in self.__choice_bundles.items():
            unchosen_content = choice_bundle.UnChosenChoices(self.__platforms)
            if unchosen_content:
                unchosen_content_dict[humblekey] = unchosen_content
        
        return unchosen_content_dict
    
    def ChoiceRedeemableContent(self):
        redeemable_content_dict = {}

        for humblekey, choice_bundle in self.__choice_bundles.items():
            redeemable_content = choice_bundle.RedeemableProducts()
            if redeemable_content:
                redeemable_content_dict[humblekey] = redeemable_content

        return redeemable_content_dict

    def ChoiceRegisterContent(self):
        key_content = []
        for choice in self.__choice_bundles.values():
            content = choice.Products(platforms)
            key_content.extend([{"key": product.RedeemKey(),
                                 "key_type": product.KeyType(),
                                 "platform_id": product.PlatformId(),
                                 "name": product.Name(),
                                 "created": product.Created(),
                                 "humble_key": product.Key()
                                }
                               for product in content
                                if not product.Registered() and not product.Expired()
                               ])
        return key_content

    def ChoiceKeyContent(self, platforms=[]):
        key_content = []
        for choice in self.__choice_bundles.values():
            content = choice.Products(platforms)
            key_content.extend([{"key": product.RedeemKey(),
                                 "key_type": product.KeyType(),
                                 "platform_id": product.PlatformId(),
                                 "name": product.Name(),
                                 "created": product.Created(),
                                 "expired": product.Expired(),
                                 "registered": product.Registered(),
                                 "humble_key": product.Key()
                                }
                               for product in content
                               ])
        return key_content

    def GiftableContent(self):
        pass
    
    def KeysContent(self, platforms=[]):
        key_content = self.ChoiceKeyContent(platforms)

        for bundle in self.__bundles.values():
            content = bundle.Products(platforms)
            key_content.extend([{"key": product.RedeemKey(),
                                 "key_type": product.KeyType(),
                                 "platform_id": product.PlatformId(),
                                 "name": product.Name(),
                                 "created": product.Created(),
                                 "expired": product.Expired(),
                                 "registered": product.Registered(),
                                 "humble_key": product.Key()
                                }
                               for product in content
                               ])

        for product in self.__store_keys.values():
            if not platforms or product.KeyType() in platforms: 
                key_content.append({"key": product.RedeemKey(),
                                    "key_type": product.KeyType(),
                                    "platform_id": product.PlatformId(),
                                    "name": product.Name(),
                                    "created": product.Created(),
                                    "expired": product.Expired(),
                                    "registered": product.Registered(),
                                    "humble_key": product.Key()
                                    })

        return key_content

    def AllKeys(self):
        return self.KeysContent()

    def GetOrder(self, humblekey):
        if humblekey in self.__store_keys:
            return self.__store_keys[humblekey]

        if humblekey in self.__bundles:
            return self.__bundles[humblekey]

        if humblekey in self.__choice_bundles:
            return self.__choice_bundles[humblekey]

        return None

    def GetOrderKeys(self):
        keys = []
        keys.extend([key for key in self.__store_keys])
        keys.extend([key for key in self.__bundles])
        keys.extend([key for key in self.__choice_bundles])
        return keys

    def GetStoreKeys(self):
        return {key: value for key, value in self.__store_keys.items()}

    def GetHumbleBundles(self):
        return {key: value for key, value in self.__bundles.items()}

    def GetChoiceBundles(self):
        return {key: value for key, value in self.__choice_bundles.items()}

    def UpdateOrder(self, order_dict):
        order_factory = OrderFactory()
        updated_order = order_factory.CreateOrder(order_dict)

        order = self.GetOrder(order_dict["gamekey"])
        if order is None:
            self.__insertOrder(order_dict["gamekey"], updated_order)
            return

        order.Update(updated_order)

    def SetProductRegistered(self, humblekey, product_machine_name):
        order = self.GetOrder(humblekey)

        if order is None:
            return

        order.SetRegistered(product_machine_name)

    def __insertOrder(self, key, new_order):
        if isinstance(new_order, HumbleStoreKey):
            self.__store_keys[key] = new_order
        elif isinstance(new_order, HumbleChoice):
            self.__choice_bundles[key] = new_order
        else:
            self.__bundles[key] = new_order

        

class Order():
    def __init__(self, init_dict):
        self._order_machine_name = init_dict["order_machine_name"]
        self._humblekey = init_dict["humblekey"]
        self._created = datetime.fromisoformat(init_dict["created"])
        self._name = init_dict["name"]
        self._subproducts = init_dict["subproducts"]
        self._updated = False

    def MachineName(self):
        return self._order_machine_name

    def Subproducts(self):
        return self._subproducts

    def Key(self):
        return self._humblekey

    def Created(self):
        return self._created

    def Name(self):
        return self._name

    def Updated(self):
        return self._updated

class HumbleBundle(Order):

    def __init__(self, init_dict, products):
        super().__init__(init_dict)
        self._products = products

    def ProductMachineNames(self, platforms = []):
        return[product.ProductMachineName() for product in self._getProductsByPlatform(platforms)]
        

    def ProductRedeemKeys(self, platforms = []):
        return[product.RedeemKey() for product in self._getProductsByPlatform(platforms)]

    def ProductNames(self, platforms = []):
        return[product.Name() for product in self._getProductsByPlatform(platforms)]

    def Products(self, platforms = []):
        return self._getProductsByPlatform(platforms)

    def SetRegistered(self, product_machine_name):
        for product in self.Products():
            if product.ProductMachineName() == product_machine_name:
                product.SetRegistered(product_machine_name)

    def _getProductsByPlatform(self, platforms):
        return [product for product in self._products if not platforms or product.KeyType() in platforms]

    def Update(self, other):
        if self._order_machine_name != other._order_machine_name or self._created != other._created \
                or not isinstance(other, HumbleBundle) or self._humblekey != other._humblekey:
            return

        product_machine_names = set(self.ProductMachineNames())
        products_dict = {product.ProductMachineName(): product for product in self.Products()}

        for product in other.Products():
            if product.ProductMachineName() not in product_machine_names:
                self._products.append(product)
                self._updated = True
            else:
                products_dict[product.ProductMachineName()].Update(product)

class HumbleChoice(HumbleBundle):

    def __init__(self, init_dict, products):
        super().__init__(init_dict, products)
        self.__chosen = True
        self.__choices_remaining = init_dict["choices_remaining"]
        self.__all_choices_dict = init_dict["all_choices"]

        if self.__all_choices_dict is None:
            self.__chosen = self.__choices_remaining == 0 and len(self._products) > 0
            self.__all_choices = []
            self.__choiceless = True
            return

        self.__choiceless = self.__all_choices_dict["productIsChoiceless"]
        self.__all_choices = self.__getAllChoices(self.__all_choices_dict)
        
        self.__setChosenFlag()

    def ChoicesRemaining(self):
        return self.__choices_remaining

    def AllChoices(self):
        return self.__all_choices_dict
            
    def __getAllChoices(self, all_choices):
        choice_info = self.__getGameData(all_choices["contentChoiceOptions"]["contentChoiceData"])
        return [ChoiceContent(machine_name, tpkds) for machine_name, tpkds in choice_info.items()]

    def __getGameData(self, contentChoiceData):
        if "game_data" in contentChoiceData:
            return self.__getChoiceTpkds(contentChoiceData["game_data"])
        if "initial" in contentChoiceData:
            return self.__getChoiceTpkds(contentChoiceData["initial"]["content_choices"])
        if "initial-get-all-games" in contentChoiceData:
            return self.__getChoiceTpkds(contentChoiceData["initial-get-all-games"]["content_choices"])
        raise KeyError("Unable to find choice game data in all_choices dictionary")

    def __getChoiceTpkds(self, game_data_dicts):
        tpkds = {}
        for display_machine_name, game_data_dict in game_data_dicts.items():
            if "tpkds" in game_data_dict:
                tpkds[display_machine_name] = game_data_dict["tpkds"]
            elif "nested_choice_tpkds" in game_data_dict:
                tpkds[display_machine_name] = [game_data_dict["nested_choice_tpkds"]]
            else: 
                raise KeyError(f"Unable to find tpkds for {display_machine_name} in all_choices")
        return tpkds

    def __setChosenFlag(self):

        #limited Choice bundle
        if not self.__choiceless:
            self.__chosen = self.__choices_remaining == 0
            return
        
        #Choiceless bundle
        choice_names = []
        for choice in self.__all_choices:
            choice_names += choice.ProductMachineNames()
        product_names = [product.ProductMachineName() for product in self._products]
        self.__chosen = len(choice_names) == len(product_names)

    def Contains(self, product):
        return product in self._products 

    def FullyChosen(self):
        return self.__chosen

    def AllProductsRedeemed(self):
        for product in self._products:
            if not product.Expired() and product.RedeemKey() is None:
                return False
        return True

    def UnChosenChoices(self, platform_preference = []):
        if self.FullyChosen():
            return {}
        choices = {}
        product_names = [product.ProductMachineName() for product in self._products]
        for choice in self.__all_choices:
            choice_products = choice.AllProductMachineNames()
            chosen = False
            for product_name in choice_products:
                if product_name in product_names:
                    chosen = True
                    break
            if chosen:
                continue
            choices[choice.MachineName()] = choice.ProductMachineNames(platform_preference)

        return choices

    def RedeemableProducts(self):
        return [product.ProductMachineName() for product in self._products if product.RedeemKey() == None and not product.Expired()]

    def Update(self, other):
        if self._order_machine_name != other._order_machine_name or self._created != other._created \
                or not isinstance(other, HumbleChoice) or self._humblekey != other._humblekey:
            return
        
        #Update products through HumbleBundle's update method
        super().Update(other)
                    
        if other.__all_choices_dict and self.__all_choices_dict != other.__all_choices_dict:
            self.__all_choices_dict = other.__all_choices_dict
            self.__all_choices = self.__getAllChoices(self.__all_choices_dict)
            self._updated = True

        if self.__choices_remaining != other.__choices_remaining:
            self.__choices_remaining = other.__choices_remaining
            self._updated = True

        self.__setChosenFlag()

class ChoiceContent():

    def __init__(self, machine_name, tpkds):
        if machine_name is None:
            raise ValueError("Choice Content must have a machine_name.")
        if tpkds is None:
            raise ValueError("Choice Content must have tpkds.")
        self.__machine_name = machine_name
        self.__items = tpkds

    def MachineName(self):
        return self.__machine_name

    def ProductMachineNames(self, platform_preference = []):
        return self.__productMachineNamesRecur(self.__items, platform_preference)
    
    def __productMachineNamesRecur(self, items, platform_preference):
        machine_names = []
        for item in items:
            if "machine_name" in item:
                machine_names.append(item["machine_name"])
                continue
            
            #nested_choice_tpkds
            platform_nested_item = None
            for platform in platform_preference:
                for nested_item in item.values():
                    if platform in nested_item[0]["key_type"]:
                        platform_nested_item = nested_item
                        break
                if platform_nested_item:
                    break

            if platform_nested_item is None:
                platform_nested_item = list(item.values())[0]
            machine_names += self.__productMachineNamesRecur(platform_nested_item, platform_preference)                
        return machine_names

    def AllProductMachineNames(self):
        return self.__allProductMachineNamesRecur(self.__items)

    def __allProductMachineNamesRecur(self, items):
        machine_names = []
        for item in items:
            if "machine_name" in item:
                machine_names.append(item["machine_name"])
                continue
            
            #nested_choice_tpkds
            for nested_item in item.values():
                machine_names += self.__allProductMachineNamesRecur(nested_item)                
        return machine_names


class HumbleStoreKey(Order):

    def __init__(self, init_dict):
        super().__init__(init_dict)
        self.__product_machine_name = init_dict["product_machine_name"]
        self.__redeem_key = init_dict["redeem_key"]
        self.__key_type = init_dict["key_type"]
        self.__key_index = init_dict["keyindex"]
        self.__platform_id = init_dict["platform_id"]
        self.__expiration_date = datetime.fromisoformat(init_dict["expiration_date"]) if init_dict.get("expiration_date", None) else None  
        self.__registered = False

        if self.__key_type and self.__key_type not in PLATFORMS:
            for platform in PLATFORMS:
                if platform in self.__key_type:
                    self.__key_type = platform
                    return

    def ProductMachineName(self):
        return self.__product_machine_name

    def RedeemKey(self):
        return self.__redeem_key

    def KeyType(self):
        return self.__key_type

    def PlatformId(self):
        return self.__platform_id

    def ExpirationDate(self):
        return self.__expiration_date

    def Expired(self):
        if self.__expiration_date is None:
            return False
        return self.__expiration_date < datetime.now()

    def Registered(self):
        return self.__registered

    def SetRegistered(self, product_machine_name):
        if self.__product_machine_name == product_machine_name:
            self.__registered = True
            self._updated = True
    
    def KeyIndex(self):
        return self.__key_index

    def Update(self, other):
        if not isinstance(other, HumbleStoreKey) or self._humblekey != other._humblekey \
        or self._order_machine_name != other._order_machine_name or self._created != other._created \
        or self.__product_machine_name != other.__product_machine_name:
            return

        if self.__redeem_key is None and other.__redeem_key is not None:
            self.__redeem_key = other.__redeem_key
            self.__key_type = other.__key_type
            self.__key_index = other.__key_index
            self._updated = True

        if self.__platform_id != other.__platform_id:
            self.__platform_id = other.__platform_id
            self._updated = True

        if self.__expiration_date != other.__expiration_date:
            self.__expiration_date = other.__expiration_date
            self._updated = True

    def __eq__(self, other):
        return (self._order_machine_name == other._order_machine_name and self._name == other._name
                and self._humblekey == other._humblekey and self._created == other._created
                and self.__redeem_key == other.__redeem_key and self.__key_type == other.__key_type
                and self.__platform_id == other.__platform_id and self.__expiration_date == other.__expiration_date
                and self.__product_machine_name == other.__product_machine_name)
