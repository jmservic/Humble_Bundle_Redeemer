

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

    def CreateStoreKeyOrder(self, order_dict, product_dict):
        init_dict = {"order_machine_name": order_dict["machine_name"],
                     "name": product_dict.get("human_name", None),
                     "humblekey": order_dict["gamekey"],
                     "created": order_dict["created"],
                     "subproducts": order_dict["subproducts"],
                     "product_machine_name": product_dict.get("machine_name",None),
                     "redeem_key": product_dict.get("redeemed_key_val", None),
                     "key_type": product_dict.get("key_type", None),
                     "platform_id": product_dict.get("steam_app_id", None),
                     "keyindex": product_dict.get("keyindex", None),
                     "is_expired": product_dict.get("is_expired", None)
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
        self.__store_keys = {}
        self.__bundles = {}
        self.__choice_bundles = {}
        self.__platforms = ["steam", "epic", "uplay", "origin"]

        order_factory = OrderFactory()
        for (key, order_dict) in orders_dict.items():
            order = order_factory.CreateOrder(order_dict)
            if isinstance(order, HumbleStoreKey):
                self.__store_keys[key] = order
            elif isinstance(order, HumbleChoice):
                self.__choice_bundles[key] = order
            else:
                self.__bundles[key] = order

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

    def GiftableContent(self):
        pass
    
    def RedeemContent(self):
        pass

class Order():
    def __init__(self, init_dict):
        self._order_machine_name = init_dict["order_machine_name"]
        self._humblekey = init_dict["humblekey"]
        self._created = init_dict["created"]
        self._name = init_dict["name"]
        self._subproducts = init_dict["subproducts"]

    def MachineName(self):
        return self._order_machine_name

    def Key(self):
        return self._humblekey

    def Created(self):
        return self._created

    def Name(self):
        return self._name

class HumbleBundle(Order):

    def __init__(self, init_dict, products):
        super().__init__(init_dict)
        self._products = products

    #def ProductInfo(self, platforms = []): #Just use this function instead of the others.
    #    products = self._getProductsByPlatform(platforms)
    #    product_info = []
    #    for product in products:
    #        info_dict = {"machine_name": product.ProductMachineName(),
    #                     "name": product.Name(),
    #                     "redeem_key": product.RedeemKey(),
    #                     }
    #        product_info.append(info_dict)
    #    return product_info

    def ProductMachineNames(self, platforms = []):
        return[product.ProductMachineName() for product in self._getProductsByPlatform(platforms)]
        

    def ProductRedeemKeys(self, platforms = []):
        return[product.RedeemKey() for product in self._getProductsByPlatform(platforms)]

    def ProductNames(self, platforms = []):
        return[product.Name() for product in self._getProductsByPlatform(platforms)]

    def Products(self, platforms = []):
        return self._getProductsByPlatform(platforms)

    def _getProductsByPlatform(self, platforms):
        return [product for product in self._products if not platforms or product.KeyType() in platforms]

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
        product_names = [product.ProductMachineName() for product in self._products]
        self.__chosen = len(choice_names) == len(product_names)
            
    def __getAllChoices(self, contentChoiceData):
        choice_info = self.__getGameData(contentChoiceData)
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

    def Contains(self, product):
        return product in self._products 

    def FullyChosen(self):
        return self.__chosen

    def AllProductsRedeemed(self):
        for product in self._products:
            if product.RedeemKey() is None:
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
        return [product.ProductMachineName() for product in self._products if product.RedeemKey() == None]

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
        self.__is_expired = init_dict["is_expired"]

    def ProductMachineName(self):
        return self.__product_machine_name

    def RedeemKey(self):
        return self.__redeem_key

    def KeyType(self):
        return self.__key_type

    def PlatformId(self):
        return self.__platform_id

    def Expired(self):
        return self.__is_expired
    
    def KeyIndex(self):
        return self.__key_index

    def __eq__(self, other):
        return (self._order_machine_name == other._order_machine_name and self._name == other._name
                and self._humblekey == other._humblekey and self._created == other._created
                and self.__redeem_key == other.__redeem_key and self.__key_type == other.__key_type
                and self.__platform_id == other.__platform_id and self.__is_expired == other.__is_expired
                and self.__product_machine_name == other.__product_machine_name)
        
        
    

