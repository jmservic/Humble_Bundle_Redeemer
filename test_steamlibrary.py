import unittest
from steamlibrary import SteamLibrary
from datetime import datetime
class TestSteamLibrary(unittest.TestCase):
#Sir Whoopass™: Immortal Death
#Tom Clancy&amp;amp;amp;rsquo;s The Division&amp;amp;amp;trade;
    def test_ContainsProduct_returns_true_for_owned_game_by_title(self):
        library_info = {"rgGames": [
            {"appid": 1150530,
             "name": "Wizard with a Gun",
                }
            ]}
        license_info = [
                {"date": datetime(2023, 10, 31),
                 "title": "wizard with a gun",
                 "aq_method": "retail"
                    }
                ]
        sut = SteamLibrary(library_info, license_info)
        game_title = "Wizard with a Gun"
        self.assertEqual(sut.ContainsProduct(game_title), (True, True))
        
    def test_ContainsProduct_returns_true_for_owned_game_by_title(self):
        library_info = {"rgGames": [
            {"appid": 1150530,
             "name": "Wizard with a Gun",
                }
            ]}
        license_info = [
                {"date": datetime(2023, 10, 31),
                 "title": "wizard with a gun",
                 "aq_method": "retail"
                    }
                ]
        sut = SteamLibrary(library_info, license_info)
        game_id = 1150530
        self.assertEqual(sut.ContainsProduct(id=game_id), (True, True))


