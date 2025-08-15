import unittest
import sqlite3
from database import Database
from libraries.humblelibrary import OrderFactory, HumbleLibrary, HumbleChoice, HumbleBundle, HumbleStoreKey
from tests.humble_ref_data import enshrouded, assassinscreed_bundle, june_2025_choice, wizardwithagun, wizardwithagun_missing_info, april_2024_choice
import os
import json
from datetime import datetime

temp_db_path = "temp.db"

def tearDownModule():
    if not os.path.exists(temp_db_path):
        return

    os.remove(temp_db_path)

class TestDBCreateDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._database = Database(temp_db_path)
        cls._con = sqlite3.connect(temp_db_path) 

    @classmethod
    def tearDownClass(cls):
        cur = cls._con.cursor()
        cur.execute("DROP TABLE Giftable")
        cur.execute("DROP TABLE Log")
        cur.execute("DROP TABLE Redeemable")
        cur.execute("DROP TABLE HumbleChoice")
        cur.execute("DROP TABLE HumbleBundle")
        cur.execute("DROP TABLE HumbleStoreKey")
        cls._con.close()

    def test_Initialize_creates_correct_tables(self):
        sut = TestDBCreateDB._database
        sut.Initialize()

        cur = TestDBCreateDB._con.cursor()
        res = cur.execute("SELECT name FROM sqlite_schema WHERE type='table'")
        table_names = set([col[0] for col in res.fetchall()])
        expected_names = set(["HumbleStoreKey", "HumbleBundle", "HumbleChoice", "Redeemable", "Log", "Giftable"])  

        self.assertEqual(table_names, expected_names)

class TestDBCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._database = Database(temp_db_path)
        cls._database.Initialize()
        cls._con = sqlite3.connect(temp_db_path) 

    @classmethod
    def tearDownClass(cls):
        cls._con.close()

    def test_SaveHumbleLibrary_persists_library_HumbleStoreKeys_in_HumbleStoreKey_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"TSskvEHeqSfUbZAs": enshrouded})
        store_key_row = ("TSskvEHeqSfUbZAs", "Enshrouded", "enshrouded_storefront", "2025-02-14T01:51:25.738781",
                         "enshrouded_steam", "[]", "TMQTG-FRRFB-NY4EZ", "steam", 0, None, None, False)
        sut.SaveHumbleLibrary(humble_library)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created,
        ProductMachineName, Subproducts, RedeemKey, KeyType, KeyIndex,
        PlatformId, ExpirationDate, Registered FROM HumbleStoreKey WHERE HumbleKey = 'TSskvEHeqSfUbZAs'""")
        self.assertEqual(res.fetchone(), store_key_row)

    def test_SaveHumbleLibrary_persists_library_HumbleBundles_in_HumbleBundle_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"Yv8pEek2ehcSppPk": assassinscreed_bundle})
        bundle_row = ("Yv8pEek2ehcSppPk", "Humble Assassin's Creed Bundle", "assassinscreed_bundle", 
                      "2017-01-16T15:38:08.924170", "[]")
        sut.SaveHumbleLibrary(humble_library)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created, Subproducts
        FROM HumbleBundle WHERE HumbleKey = 'Yv8pEek2ehcSppPk'""")
        self.assertEqual(res.fetchone(), bundle_row)

    def test_SaveHumbleChoice_persists_library_HumbleChoiceBundles_in_HumbleChoice_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"rw3m6TUnb3eqmHzM": june_2025_choice})
        choice_row = ("rw3m6TUnb3eqmHzM", "June 2025 Humble Choice", "june_2025_choice",
                      "2025-06-24T19:47:30.260778", "[]", 0, json.dumps(june_2025_choice["product"]["all_choices"]))
        sut.SaveHumbleLibrary(humble_library)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created, Subproducts,
        ChoicesRemaining, AllChoices FROM HumbleChoice WHERE HumbleKey = 'rw3m6TUnb3eqmHzM'""")
        self.assertEqual(res.fetchone(), choice_row)

    def test_SaveHumbleLibrary_persists_library_Bundle_Products_in_HumbleStoreKey_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"rw3m6TUnb3eqmHzM": june_2025_choice})
        product_rows = set([
            ("rw3m6TUnb3eqmHzM", "Nobody Wants to Die","june_2025_choice", "2025-06-24T19:47:30.260778",
             "nobodywantstodie_tier1_choice_steam", "[]", "LDGZQ-WPB90-KDAPG", "steam", 0, 1939970, None, False),
            ("rw3m6TUnb3eqmHzM", "Dungeons of Hinterberg","june_2025_choice", "2025-06-24T19:47:30.260778",
             "dungeonsofhinterberg_choice_steam", "[]", "IFZM9-2RFVD-PTKQT", "steam", 0, 1983260, None, False),
            ("rw3m6TUnb3eqmHzM", "Tchia","june_2025_choice", "2025-06-24T19:47:30.260778",
             "tchia_row_choice_steam", "[]", "IE8AA-89R24-GGLHZ", "steam", 0, 1496590, "2026-01-05T18:00:00.000000", False),
            ("rw3m6TUnb3eqmHzM", "One Month of IGN Plus","june_2025_choice", "2025-06-24T19:47:30.260778",
             "ignplus_june_choicecoupon_2025", "[]", "HUMBLESUR0PVW94PLV", "generic", 0, None, "2025-07-06T07:00:00.000000", False)
            ])
        sut.SaveHumbleLibrary(humble_library)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created,
        ProductMachineName, Subproducts, RedeemKey, KeyType, KeyIndex,
        PlatformId, ExpirationDate, Registered FROM HumbleStoreKey WHERE HumbleKey = 'rw3m6TUnb3eqmHzM'""")
        self.assertEqual(set(res.fetchall()), product_rows)

    def test_SaveRedeemAttempt_persists_attempt_in_Redeemable_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"Z8KftUKAEf8zG7zY": april_2024_choice})
        attempt_time = datetime.now()
        attempt_time_str = attempt_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        redeem_row = ("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "fashionpolicesquad_choice_steam",
                      attempt_time_str, attempt_time_str, 1, False)

        sut.SaveHumbleLibrary(humble_library)
        sut.SaveRedeemAttempt("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "fashionpolicesquad_choice_steam", attempt_time, False)
        
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, ProductMachineName, FirstAttempt, LastAttempt,
                          Attempts, Redeemed FROM Redeemable 
                          WHERE HumbleKey = 'Z8KftUKAEf8zG7zY' and ProductMachineName = 'fashionpolicesquad_choice_steam'""")
        self.assertEqual(res.fetchone(), redeem_row)

    def test_Log_persists_record_in_Log_table(self):
        sut = TestDBCreate._database
        log_record = ("HK_Key", "Fashion", "fashion_steam", "chose", True)
        sut.Log("HK_Key", "Fashion", "fashion_steam", "chose", True)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, ProductMachineName, Action, Success FROM Log""")
        self.assertEqual(res.fetchone(), log_record)

    def test_SaveGift_persists_giftkey_in_Giftable_table(self):
        sut = TestDBCreate._database
        humble_library = HumbleLibrary({"TSskvEHeqSfUbZAs": enshrouded})
        gift_record = ("TSskvEHeqSfUbZAs", "Enshrouded", "enshrouded_steam", "TMQTG-FRRFB-NY4EZ", "steam", None)
        order_factory = OrderFactory()
        order = order_factory.CreateOrder(enshrouded)
        sut.SaveHumbleLibrary(humble_library)
        sut.SaveGift(order)
        cur = TestDBCreate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, ProductMachineName, RedeemKey, KeyType, ExpirationDate
                          FROM Giftable WHERE HumbleKey = 'TSskvEHeqSfUbZAs' and ProductMachineName = 'enshrouded_steam'""")
        self.assertEqual(res.fetchone(), gift_record)

class TestDBUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._database = Database(temp_db_path)
        cls._database.Initialize()
        cls._con = sqlite3.connect(temp_db_path) 

    @classmethod
    def tearDownClass(cls):
        cur = cls._con.cursor()
        cur.execute("DROP TABLE Giftable")
        cur.execute("DROP TABLE Log")
        cur.execute("DROP TABLE Redeemable")
        cur.execute("DROP TABLE HumbleChoice")
        cur.execute("DROP TABLE HumbleBundle")
        cur.execute("DROP TABLE HumbleStoreKey")
        cls._con.close()

    def test_SaveHumbleLibrary_updates_updated_HumbleStoreKeys(self):
        sut = TestDBUpdate._database
        humble_library = HumbleLibrary({"mNUwXmdxFqwZpNPZ": wizardwithagun_missing_info})
        store_key_row = ("mNUwXmdxFqwZpNPZ", "Wizard with a Gun (Steam)", "wizardwithagun_storefront", "2023-11-01T00:55:38.697741",
                         "wizardwithagun_storefront_steam_rlq7w", "[]", "BL603-ZYX0H-LG8A4",
                         "steam", 0, 1150530, "2026-01-05T18:00:00.000000", True)
        sut.SaveHumbleLibrary(humble_library)

        humble_library.UpdateOrder(wizardwithagun)
        humble_library.SetProductRegistered("mNUwXmdxFqwZpNPZ", "wizardwithagun_storefront_steam_rlq7w")
        sut.SaveHumbleLibrary(humble_library)
        cur = TestDBUpdate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created,
        ProductMachineName, Subproducts, RedeemKey, KeyType, KeyIndex,
        PlatformId, ExpirationDate, Registered FROM HumbleStoreKey WHERE HumbleKey = 'mNUwXmdxFqwZpNPZ'""")
        self.assertEqual(res.fetchone(), store_key_row)

    def test_SaveHumbleLibrary_updates_updated_Bundle(self):
        sut = TestDBUpdate._database
        humble_library = HumbleLibrary({"rw3m6TUnb3eqmHzM": june_2025_choice})
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["product"] = {}
        order_dict["product"].update(june_2025_choice["product"])
        order_dict["product"]["all_choices"] = {"contentChoiceOptions": {"contentChoiceData": {"game_data": {"amnesia_thebunker": {
                        "title": "Amnesia: The Bunker",
                        "display_item_machine_name": "amnesia_thebunker",
                        "tpkds": [
                            {
                                "machine_name": "amnesia_thebunker_choice_steam",
                                "show_custom_instructions_in_user_libraries": False,
                                "key_type": "steam",
                                "visible": True,
                                "sold_out": False,
                                "is_partial_gift": False,
                                "display_separately": False,
                                "steam_app_id": 1944430,
                                "exclusive_countries": [
                                ],
                                "class": "steambutton",
                                "num_days_until_expired": -1,
                                "gamekey": "rw3m6TUnb3eqmHzM",
                                "disallowed_countries": [
                                ],
                                "direct_redeem": False,
                                "instructions_html": "\u003ca href\u003d\u0027https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys\u0027 target\u003d\u0027_blank\u0027\u003eSteam Instructions\u003c/a\u003e",
                                "key_type_human_name": "Steam",
                                "human_name": "Amnesia: The Bunker",
                                "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                "auto_expand": True,
                                "is_expired": False,
                                "partial_gift_enabled": True,
                                "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                            }
                        ],
                        "user_rating": {
                            "steam_percent|decimal": 0.93,
                            "display_user_ratings": "steam_overall",
                            "review_text": "very_positive",
                            "steam_count": 7629
                        },
                        "platforms": [
                            "windows"
                        ],
                        "more_information": None,
                        "msrp|money": {
                            "currency": "USD",
                            "amount": 24.99
                        },
                        "developers": [
                            "Frictional Games"
                        ],
                        "genres": [
                            "Action",
                            "Indie",
                            "Adventure"
                        ]
                    }}}}}
        order_dict["product"]["all_choices"]["contentChoiceOptions"]["contentChoiceData"]["game_data"].update(
                june_2025_choice["product"]["all_choices"]["contentChoiceOptions"]["contentChoiceData"]["game_data"])
        order_dict["product"]["all_choices"]["productIsChoiceless"] = True

        choice_row = ("rw3m6TUnb3eqmHzM", "June 2025 Humble Choice", "june_2025_choice",
                      "2025-06-24T19:47:30.260778", "[]", 0, json.dumps(order_dict["product"]["all_choices"]))

        sut.SaveHumbleLibrary(humble_library)
        humble_library.UpdateOrder(order_dict)
        sut.SaveHumbleLibrary(humble_library)

        cur = TestDBUpdate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, OrderMachineName, Created, Subproducts,
        ChoicesRemaining, AllChoices FROM HumbleChoice WHERE HumbleKey = 'rw3m6TUnb3eqmHzM'""")
        self.assertEqual(res.fetchone(), choice_row)


    def test_SaveRedeemAttempt_updates_attempt_in_Redeemable_table(self):
        sut = TestDBUpdate._database
        humble_library = HumbleLibrary({"Z8KftUKAEf8zG7zY": april_2024_choice})
        attempt_time_1 = datetime.now()
        attempt_time_1_str = attempt_time_1.strftime("%Y-%m-%dT%H:%M:%S.%f")

        sut.SaveHumbleLibrary(humble_library)
        sut.SaveRedeemAttempt("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "fashionpolicesquad_choice_steam", attempt_time_1, False)
        
        attempt_time_2 = datetime.now()
        attempt_time_2_str = attempt_time_2.strftime("%Y-%m-%dT%H:%M:%S.%f")
        redeem_row = ("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "fashionpolicesquad_choice_steam",
                      attempt_time_1_str, attempt_time_2_str, 2, True)

        sut.SaveRedeemAttempt("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "fashionpolicesquad_choice_steam", attempt_time_2, True)
        cur = TestDBUpdate._con.cursor()
        res = cur.execute("""SELECT HumbleKey, Name, ProductMachineName, FirstAttempt, LastAttempt,
                          Attempts, Redeemed FROM Redeemable 
                          WHERE HumbleKey = 'Z8KftUKAEf8zG7zY' and ProductMachineName = 'fashionpolicesquad_choice_steam'""")
        self.assertEqual(res.fetchone(), redeem_row)


class TestDBRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._database = Database(temp_db_path)
        cls._database.Initialize()
        cls._con = sqlite3.connect(temp_db_path) 

    @classmethod
    def tearDownClass(cls):
        cur = cls._con.cursor()
        cur.execute("DROP TABLE Giftable")
        cur.execute("DROP TABLE Log")
        cur.execute("DROP TABLE Redeemable")
        cur.execute("DROP TABLE HumbleChoice")
        cur.execute("DROP TABLE HumbleBundle")
        cur.execute("DROP TABLE HumbleStoreKey")
        cls._con.close()

    def test_GetOrders_returns_dict_containing_all_orders(self):
        self.maxDiff = None
        sut = TestDBRead._database
        humble_library = HumbleLibrary({
            "Z8KftUKAEf8zG7zY": april_2024_choice,
            "Yv8pEek2ehcSppPk": assassinscreed_bundle,
            "TSskvEHeqSfUbZAs": enshrouded,
            "mNUwXmdxFqwZpNPZ": wizardwithagun
            })
        order_dict = {
                "Z8KftUKAEf8zG7zY": {
                    "HumbleBundle": None,
                    "HumbleChoice": ("Z8KftUKAEf8zG7zY", "April 2024 Humble Choice", "april_2024_choice", "2024-04-30T18:51:02.620236",
                                     json.dumps(april_2024_choice["subproducts"]), 0, 
                                     json.dumps(april_2024_choice["product"]["all_choices"])),
                    "StoreKeys": [("Z8KftUKAEf8zG7zY", "Victoria 3","april_2024_choice", "2024-04-30T18:51:02.620236",
                                   "victoria3_choice_steam", "[]","Z7AQM-3XTNN-PAATK" ,"steam", 0, 529340, None, False),
                                  ("Z8KftUKAEf8zG7zY", "The Callisto Protocol","april_2024_choice",
                                   "2024-04-30T18:51:02.620236", "thecallistoprotocol_choice_steam",
                                   "[]", "996KZ-JYH6X-T62DJ",
                                   "steam", 0, 1544020, None, False),
                                  ("Z8KftUKAEf8zG7zY", "Humankind Definitive Edition", "april_2024_choice",
                                   "2024-04-30T18:51:02.620236", "humankind_definitiveedition_choice_steam", 
                                   "[]", "KBEKN-R22I4-BH9M5",
                                   "steam", 0, 1124300, None, False),
                                  ("Z8KftUKAEf8zG7zY", "Fashion Police Squad", "april_2024_choice", 
                                   "2024-04-30T18:51:02.620236", "fashionpolicesquad_choice_steam",
                                   "[]", None, "steam", 0, 1319460, None, False),
                                  ("Z8KftUKAEf8zG7zY", "Terraformers","april_2024_choice", "2024-04-30T18:51:02.620236",
                                   "terraformers_row_choice_steam", "[]", "T5JBA-F3Z39-QG3FX",
                                   "steam", 0, 1244800, None, False),
                                  ("Z8KftUKAEf8zG7zY", "Symphony of War: The Nephilim Saga","april_2024_choice",
                                   "2024-04-30T18:51:02.620236", "symphonyofwar_thenephilimsaga_choice_steam",
                                   "[]", "ZA0J0-59TLG-MVPYA",
                                   "steam", 0, 1488200, None, False),
                                  ("Z8KftUKAEf8zG7zY", "Coromon","april_2024_choice", "2024-04-30T18:51:02.620236",
                                   "coromon_choice_steam", "[]", "YN2CB-VAH8C-NFYBF",
                                   "steam", 0, 1218210, None, False),
                                  ("Z8KftUKAEf8zG7zY", "The Excavation of Hob's Barrow","april_2024_choice",
                                   "2024-04-30T18:51:02.620236", "theexcavationofhobsbarrow_choice_steam",
                                   "[]", "X7TX6-A9TYH-ZTR0Y",
                                   "steam", 0, 1182310, None, False)
                                  ]
                    },
                "Yv8pEek2ehcSppPk": {
                    "HumbleBundle": ("Yv8pEek2ehcSppPk", "Humble Assassin's Creed Bundle", "assassinscreed_bundle", 
                                     "2017-01-16T15:38:08.924170", "[]"),
                    "HumbleChoice": None,
                    "StoreKeys": [("Yv8pEek2ehcSppPk", "Assassin's Creed® Chronicles India", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_chronicles_india_bundle_na_uplay",
                                   "[]", "AP3C-XN4R-8V4E-CLPM", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® Chronicles China", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_chronicles_china_bundle_na_uplay",
                                   "[]", "UXV7-3L7M-TW67-WAET", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® Chronicles Russia", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_chronicles_russia_bundle_na_uplay",
                                   "[]", "VKJY-7AVN-TKG7-MVUH", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed®", "assassinscreed_bundle", "2017-01-16T15:38:08.924170",
                                   "assassinscreed_bundle_uplay", "[]", "UP3-4DED-A2FA-8086-E322",
                                   "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® Liberation HD", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_liberationhd_bundle_uplay",
                                   "[]", "W9QG-KVGB-YX6M-6W8W", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® III", "assassinscreed_bundle", "2017-01-16T15:38:08.924170",
                                   "assassinscreed3_bundle_uplay", "[]", "UVNL-LHY7-GKR6-GE6A",
                                   "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® III - Tyranny of King Washington: The Infamy (DLC)",
                                   "assassinscreed_bundle", "2017-01-16T15:38:08.924170", "assassinscreed3_washingtondlc_bundle_uplay",
                                   "[]", "WBMB-GP83-9MWX-86NF", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® II Deluxe Edition", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed2_deluxe_bundle_uplay",
                                   "[]", "WCGF-AEJX-GACU-XUBX", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® Unity", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_unity_bundle_na_uplay",
                                   "[]", "X8C7-GR6M-D87X-DM6E", "uplay", 0, None, None, False),
                                  ("Yv8pEek2ehcSppPk", "Assassin's Creed® Brotherhood", "assassinscreed_bundle",
                                   "2017-01-16T15:38:08.924170", "assassinscreed_brotherhood_bundle_uplay",
                                   "[]", "WPAT-4YKP-AAMM-X4RG", "uplay", 0, None, None, False)
                                  ]
                    },
                "TSskvEHeqSfUbZAs": {
                    "HumbleBundle": None,
                    "HumbleChoice": None,
                    "StoreKeys": [("TSskvEHeqSfUbZAs", "Enshrouded", "enshrouded_storefront", "2025-02-14T01:51:25.738781",
                         "enshrouded_steam", "[]", "TMQTG-FRRFB-NY4EZ", "steam", 0, None, None, False)
                                  ]
                    },
                "mNUwXmdxFqwZpNPZ": {
                        "HumbleBundle": None,
                        "HumbleChoice": None,
                        "StoreKeys": [("mNUwXmdxFqwZpNPZ", "Wizard with a Gun (Steam)", "wizardwithagun_storefront",
                                   "2023-11-01T00:55:38.697741", "wizardwithagun_storefront_steam_rlq7w",
                                   "[]", "BL603-ZYX0H-LG8A4", "steam", 0, 1150530, "2026-01-05T18:00:00.000000", False)]
                        }
                      }
        sut.SaveHumbleLibrary(humble_library)
        self.assertEqual(sut.GetOrders(), order_dict)

                      


