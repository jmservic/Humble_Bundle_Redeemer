import string
import re

punctuation = "".join({char for char in string.punctuation} - {"[","]","(",")","&",";"})

class SteamLibrary():

    def __init__(self, library_info, licenses_info):
        self.__library_dict = { game_info["appid"]: {"name": SanitizeText(game_info["name"]),#.lower().translate(str.maketrans("", "", string.punctuation)), 
                                                      "sort_as": game_info.get("sort_as", None)}
                               for game_info in library_info["rgGames"]}

        for license_info in licenses_info:
            license_info["title"] = SanitizeText(license_info["title"]) #.lower().translate(str.maketrans("", "", string.punctuation))
            print(license_info["title"])

        for game_dict in self.__library_dict.values():
            for license_info in licenses_info:
                if game_dict["name"] in license_info["title"] or license_info["title"] in game_dict["name"]:
                    game_dict["date"] = license_info["date"]
                    game_dict["aq_method"] = license_info["aq_method"]
            print(game_dict)

    def ContainsProduct(self, title=None, id=None):
        product, exact_match = self.__FindProduct(title, id)
        return product is not None, exact_match

    def ContainsBundle(self, bundle_info):
        pass

    def ProductRegisterDate(self, title=None, id=None):
        pass
    
    def BundleRegisterDate(self, bundle_info):
        pass

    def __FindProduct(self, title=None, id=None):
        match = (None, False)
        if id:
            return (self.__library_dict[id], True)

        if title:
            title = SanitizeText(title) #.lower().translate(str.maketrans("", "", string.punctuation))
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

def SanitizeText(text):
    lower_and_removed_punc = re.sub("&.*;|;", "", text.lower().translate(str.maketrans("", "", punctuation)))
    return re.sub("  +|[([].*[])]"," ","".join([char for char in lower_and_removed_punc if str.isascii(char)])).strip()
