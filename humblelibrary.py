

class OrderFactory():
    
    def CreateOrder(self, order_dict):
        category = order_dict["product"]["category"]
        match category:
            case "storefront":
                order_info_dict = {"gamekey": order_dict["gamekey"], "created": order_dict["created"]}
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
                order = self.CreateBundleOrder(order_dict)
            case _:
                raise ValueError(f"HumbleBundle order category '{category}' is an unknown category type.")
        return order

    def CreateStoreKeyOrder(self, order_dict, product_dict):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": product_dict["human_name"],
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
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
                     "total_choices": order_dict["total_choices"]
                     }
        products = [self.CreateStoreKeyOrder(order_dict, product_dict) for product_dict in product_dicts]
        return HumbleChoice(init_dict, products)

    def CreateBundleOrder(self, order_dict):
        return HumbleBundle()

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

class HumbleChoice():

    def __init__(self, init_dict, products):
        self.__products = products

    def contains(self, product):
        return product in self.__products 

class HumbleBundle():

    def __init__(self):
        pass

class HumbleStoreKey():

    def __init__(self, init_dict):
        self.__order_machine_name = init_dict["order_machine_name"]
        self.__name = init_dict["name"]
        self.__humblekey = init_dict["humblekey"]
        self.__product_machine_name = init_dict["product_machine_name"]
        self.__created = init_dict["created"]
        self.__redeem_key = init_dict["redeem_key"]
        self.__key_type = init_dict["key_type"]
        self.__platform_id = init_dict["platform_id"]
        self.__is_expired = init_dict["is_expired"]

    def __eq__(self, other):
        return (self.__order_machine_name == other.__order_machine_name and self.__name == other.__name
                and self.__humblekey == other.__humblekey and self.__created == other.__created
                and self.__redeem_key == other.__redeem_key and self.__key_type == other.__key_type
                and self.__platform_id == other.__platform_id and self.__is_expired == other.__is_expired
                and self.__product_machine_name == other.__product_machine_name)
        
        
    

