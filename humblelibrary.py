

class OrderFactory():
    
    def CreateOrder(self, order_dict):
        category = order_dict["product"]["category"]
        match category:
            case "storefront":
                order = self.CreateStoreKeyOrder(order_dict)
            case "subscriptionplan" | "subscriptioncontent":
                order = self.CreateChoiceOrder(order_dict)
            case "bundle":
                order = self.CreateBundleOrder(order_dict)
            case _:
                raise ValueError(f"HumbleBundle order category '{category}' is an unknown category type.")
        return order

    def CreateStoreKeyOrder(self, order_dict):
        pass

    def CreateChoiceOrder(self, order_dict):
        pass

    def CreateBundleOrder(order_dict):
        pass

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

    def __init__(self):
        pass

class HumbleBundle():

    def __init__(self):
        pass

class HumbleStoreKey():

    def __init__(self):
        pass
    

