

class OrderFactory():
    
    def CreateOrder(self, order_dict):
        category = order_dict["product"]["category"]
        match category:
            case "storefront":
                order_info_dict = {"gamekey": order_dict["gamekey"], "created": order_dict["created"], "subproducts": order_dict["subproducts"]}
                order_info_dict.update(order_dict["product"])
                order = self.CreateStoreKeyOrder(order_info_dict, order_dict["tpkd_dict"]["all_tpks"][0])
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

    def CreateStoreKeyOrder(self, order_dict, product_dict):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": product_dict["human_name"],
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "subproducts": order_dict["subproducts"],
                     "product_machine_name": product_dict["machine_name"],
                     "redeem_key": product_dict.get("redeemed_key_val", None),
                     "key_type": product_dict.get("key_type", None),
                     "platform_id": product_dict.get("steam_app_id", None),
                     "is_expired": product_dict["is_expired"]
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
        products = [self.CreateStoreKeyOrder(order_dict, product_dict) for product_dict in product_dicts]
        return HumbleChoice(init_dict, products)

    def CreateBundleOrder(self, order_dict, product_dicts):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": order_dict["human_name"],
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "subproducts": order_dict["subproducts"]
                    }
        products = [self.CreateStoreKeyOrder(order_dict, product_dict) for product_dict in product_dicts]
        return HumbleBundle(init_dict, products)

class HumbleLibrary():

    def __init__(self, orders_dict):
        self.__orders = {}
        order_factory = OrderFactory
        for (key, order) in orders_dict.item():
            self.__orders[key] = order_factory.CreateOrder(order)

    def ChoiceChooseContent(self):
        pass
    
    def ChoiceRedeemContent(self):
        pass

    def GiftableContent(self):
        pass

class Order():
    def __init__(self, init_dict):
        self._order_machine_name = init_dict["order_machine_name"]
        self._humblekey = init_dict["humblekey"]
        self._created = init_dict["created"]
        self._name = init_dict["name"]
        self._subproducts = init_dict["subproducts"]

class HumbleBundle(Order):

    def __init__(self, init_dict, products):
        super().__init__(init_dict)
        self._products = products

    def ProductInfo(self, platforms = []): #Just use this function instead of the others.
        pass

    def ProductMachineNames(self, platforms = []):
        products = self.__getGamesByPlatform(platforms)

    def ProductRegisterKeys(self, platforms = []):
        pass

    def ProductNames(self, platforms = []):
        pass

    def Products(self, platform = []):
        pass

    def _getGamesByPlatform(platforms):
        pass


class HumbleChoice(HumbleBundle):

    def __init__(self, init_dict, products):
        super().__init__(init_dict, products)
        self.__chosen = True
        self.__choices_remaining = init_dict["choices_remaining"]

        if init_dict["all_choices"] is None:
            self.__chosen = self.__choices_remaining == 0 and len(self._products) > 0
            self.__all_choices = []
            return

        self.__choiceless = init_dict["all_choices"]["productIsChoiceless"]
        self.__all_choices = self.__getAllChoices(init_dict["all_choices"]["contentChoiceOptions"]["contentChoiceData"])

        #limited Choice bundle
        if not self.__choiceless:
            self.__chosen = self.__choices_remaining == 0
            return
        
        #Choiceless bundle
        choice_names = []
        for choice in self.__all_choices:
            choice_names += choice.ProductMachineNames()
        product_names = [product.MachineName() for product in self._products]
        self.__chosen = len(choice_names) == len(product_names)
            
    def __getAllChoices(self, contentChoiceData):
        choice_info = self.__getGameData(contentChoiceData)
        return [ChoiceContent(machine_name, tpkds) for machine_name, tpkds in choice_info.items()]

    def __getGameData(self, contentChoiceData):
        if "game_data" in contentChoiceData:
            return self.__getChoiceTpkds(contentChoiceData["game_data"])
        if "initial" in contentChoiceData:
            return self.__getChoiceTpkds(contentChoiceData["initial"]["content_choices"])
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

    def Contains(self, product):
        return product in self._products 

    def FullyChosen(self):
        return self.__chosen

    def AllProductsRedeemed(self):
        for product in self._products:
            if product.RedeemKey() is None:
                return False
        return True

    def UnChosenChoices(self):
        if self.__chosen:
            return []

    def RedeemableProducts(self):
        pass

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


class HumbleStoreKey(Order):

    def __init__(self, init_dict):
        super().__init__(init_dict)
        self.__product_machine_name = init_dict["product_machine_name"]
        self.__redeem_key = init_dict["redeem_key"]
        self.__key_type = init_dict["key_type"]
        self.__platform_id = init_dict["platform_id"]
        self.__is_expired = init_dict["is_expired"]

    def MachineName(self):
        return self.__product_machine_name

    def RedeemKey(self):
        return self.__redeem_key

    def __eq__(self, other):
        return (self._order_machine_name == other._order_machine_name and self._name == other._name
                and self._humblekey == other._humblekey and self._created == other._created
                and self.__redeem_key == other.__redeem_key and self.__key_type == other.__key_type
                and self.__platform_id == other.__platform_id and self.__is_expired == other.__is_expired
                and self.__product_machine_name == other.__product_machine_name)
        
        
    

