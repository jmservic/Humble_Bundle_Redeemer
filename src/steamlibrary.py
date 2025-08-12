import string
import re

punctuation = "".join({char for char in string.punctuation} - {"[","]","(",")","&",";"})

def SanitizeText(text):
    lower_and_removed_punc = re.sub(r"&[\S]*;|;", "", text.lower().translate(str.maketrans("", "", punctuation)))
    return re.sub(r"  +|[([].*[])]"," ","".join([char for char in lower_and_removed_punc if str.isascii(char)])).strip()

class SteamLibrary():

    def __init__(self, library_info, licenses_info):
        self.__library_dict = { game_info["appid"]: {"name": SanitizeText(game_info["name"]),
                                                      "sort_as": game_info.get("sort_as", None)}
                               for game_info in library_info["rgGames"]}

        for license_info in licenses_info:
            license_info["title"] = SanitizeText(license_info["title"]) 
            #print(license_info["title"])

        for game_dict in self.__library_dict.values():
            for license_info in licenses_info:
                if game_dict["name"] in license_info["title"] or license_info["title"] in game_dict["name"]:
                    game_dict["date"] = license_info["date"]
                    game_dict["aq_method"] = license_info["aq_method"].lower()
                if game_dict["name"] == license_info["title"]:
                    break
            #print(game_dict)

    def ContainsProduct(self, title=None, id=None):
        product, exact_match = self.__FindProduct(title, id)
        return product is not None, exact_match

    def ContainsBundle(self, bundle_info):
        for package_info in bundle_info["m_rgItems"]:
            for app_id in package_info["m_rgIncludedAppIDs"]:
                found, _ = self.ContainsProduct(id=app_id)
                base_price = package_info["m_nBasePriceInCents"]
                if not found and base_price and base_price > 0:
                    return False
        return True

    def ProductRegisterDate(self, title=None, id=None):
        product, _ = self.__FindProduct(title, id)
        if product:
            return product.get("date", None)
    
    def BundleRegisterDate(self, bundle_info):
        acquisition_date = None
        for package_info in bundle_info["m_rgItems"]:
            for app_id in package_info["m_rgIncludedAppIDs"]:
                product, _ = self.__FindProduct(id=app_id)
                base_price = package_info["m_nBasePriceInCents"]
                if not product:
                    if base_price and base_price > 0:
                        return
                    continue
                product_date = product.get("date", None)
                if product_date:
                    if not acquisition_date:
                        acquisition_date = product_date
                    elif product_date > acquisition_date:
                        acquisition_date = product_date
        return acquisition_date
                    
    def ProductAcquisitionMethod(self, title=None, id=None):
        product, _ = self.__FindProduct(title, id)
        if product:
            return product.get("aq_method", None)

    def BundleAcquisitionMethod(self, bundle_info):
        acquisition_method = None
        for package_info in bundle_info["m_rgItems"]:
            for app_id in package_info["m_rgIncludedAppIDs"]:
                product, _ = self.__FindProduct(id=app_id)
                base_price = package_info["m_nBasePriceInCents"]
                if not product:
                    if base_price and base_price > 0:
                        return
                    continue
                product_method = product.get("aq_method", None)
                if product_method:
                    if not acquisition_method:
                        acquisition_method = product_method
                    elif product_method != acquisition_method:
                        acquisition_method = "mixed"
        return acquisition_method

    def __FindProduct(self, title=None, id=None):
        match = (None, False)

        if id in self.__library_dict:
            return (self.__library_dict[id], True)

        if title:
            title = SanitizeText(title)
            matches = [game_dict for game_dict in self.__library_dict.values() if game_dict["name"] in title]
            if matches:
                match = (matches[0], False)
                for possible_match in matches:
                    if possible_match["name"] == title:
                        match = (possible_match, True)
                        break
            else:
                matches = [game_dict for game_dict in self.__library_dict.values() if title in game_dict["name"]]
                match = (matches[0], False) if matches else (None, False)

        return match

