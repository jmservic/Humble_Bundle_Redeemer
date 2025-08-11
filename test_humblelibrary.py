import unittest
from datetime import datetime, timedelta
from humblelibrary import OrderFactory, HumbleLibrary, HumbleChoice, HumbleBundle, HumbleStoreKey, ChoiceContent
from humble_ref_data import january_2019_monthly, april_2021_choice, june_2020_choice, april_2024_choice, june_2025_choice, assassinscreed_bundle, mixed_key_bundle

def EqualInContent(collection_1, collection_2):
    if not collection_1 or not collection_2 or len(collection_1) != len(collection_2):
        print(collection_1)
        return False
    for item in collection_1:
        if item not in collection_2:
            print(item)
            return False
    return True

class TestHumbleLibrary(unittest.TestCase):
    orders_dict = {"NUDtNZdxFP7seeap": january_2019_monthly,
                  "pAqvWHcU26DfphXe": june_2020_choice,
                  "A7CESV6Pp4ZWFarX": april_2021_choice,
                  "Z8KftUKAEf8zG7zY": april_2024_choice,
                  "rw3m6TUnb3eqmHzM": june_2025_choice,
                  "Yv8pEek2ehcSppPk": assassinscreed_bundle                      
            }

    def test_SetProductRegistered_sets_registered_flag_on_product(self):
        sut = HumbleLibrary(TestHumbleLibrary.orders_dict)
        sut.SetProductRegistered("Z8KftUKAEf8zG7zY", "thecallistoprotocol_choice_steam")
        choice_products = sut.GetOrder("Z8KftUKAEf8zG7zY").Products()
        
        for product in choice_products:
            if product.ProductMachineName() == "thecallistoprotocol_choice_steam":
                self.assertTrue(product.Registered())
            else:
                self.assertFalse(product.Registered())

    def test_UpdateOrder_updates_order_with_new_data(self):
        sut = HumbleLibrary(TestHumbleLibrary.orders_dict)
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in june_2025_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        order_dict["tpkd_dict"]["all_tpks"].append({
          "is_gift": False,
          "machine_name": "biped_choice_steam",
          "gamekey": "rw3m6TUnb3eqmHzM",
          "exclusive_countries": [],
          "num_days_until_expired": -1,
          "disallowed_countries": [],
          "show_custom_instructions_in_user_libraries": False,
          "key_type": "steam",
          "visible": True,
          "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
          "display_separately": False,
          "redeemed_key_val": "redacted",
          "key_type_human_name": "Steam",
          "steam_app_id": 1071870,
          "human_name": "Biped",
          "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
          "auto_expand": True,
          "is_expired": False,
          "class": "steambutton",
          "keyindex": 0,
          "disclaimer": "Steam will not provide extra giftable copies of games you already own."
        })

        sut.UpdateOrder(order_dict)
        self.assertTrue(sut.GetOrder("rw3m6TUnb3eqmHzM").Updated())

    def test_UpdateOrder_inserts_new_order_if_not_in_the_HumbleLibrary_object(self):
        sut = HumbleLibrary(TestHumbleLibrary.orders_dict)
        sut.UpdateOrder(mixed_key_bundle)
        self.assertIsNotNone(sut.GetOrder("AvBcDeF041124034"))

    def test_ChoiceChooseContent_returns_dict_of_unchosen_content(self):
        sut = HumbleLibrary(TestHumbleLibrary.orders_dict)
        unchosen_content = {"rw3m6TUnb3eqmHzM": {
                    "havendock": ["havendock_choice_steam"],
                    "warhammer40000_boltgun": ["warhammer40k_boltgun_row_choice_steam"],
                    "legacyofkainsoulreaver12remastered": ["legacyofkaintmsoulreaver1and2remastered_row_choice_steam"],
                    "skerritual": ["skerrittual_choice_steam"],
                    "biped": ["biped_choice_steam"],
                    "bootdev_june2025_onemonthfree": ["bootdev1monthsubscription_june_choice_coupon"]    
               }
            }
        self.assertEqual(sut.ChoiceChooseContent(), unchosen_content)

    def test_ChoiceRedeemableContent_returns_unredeemed_choice_content(self):
        sut = HumbleLibrary(TestHumbleLibrary.orders_dict)
        redeemable_content = {"Z8KftUKAEf8zG7zY": [ 
                                "fashionpolicesquad_choice_steam"            
                                ]
                              }
        self.assertEqual(sut.ChoiceRedeemableContent(), redeemable_content)

    def test_ChoiceKeyContent_returns_product_info_for_choice_bundles(self):
        sut = HumbleLibrary({"NUDtNZdxFP7seeap": january_2019_monthly,
                             "Yv8pEek2ehcSppPk": assassinscreed_bundle,
                             "mvHZvHGE7dzzcGTC":{"amount_spent": 71.99,
                                                 "product": {
                                                    "category": "storefront",
                                                    "machine_name": "dragonsdogma2_deluxe_storefront",
                                                    "empty_tpkds": {},
                                                    "post_purchase_text": "",
                                                    "human_name": "Dragon's Dogma 2 - Deluxe Edition",
                                                    "partial_gift_enabled": True
                                                    },
                                                "gamekey": "mvHZvHGE7dzzcGTC",
                                                "uid": "XX5FHNZNHP351",
                                                "created": "2024-03-19T20:08:02.142843",
                                                "missed_credit": None,
                                                "subproducts": [],
                                                "total_choices": 0,
                                                "tpkd_dict": {
                                                    "all_tpks": [
                                                        {
                                                        "is_gift": False,
                                                        "machine_name": "dragonsdogma2_deluxe_preorder_us_steam",
                                                        "gamekey": "mvHZvHGE7dzzcGTC",
                                                        "exclusive_countries": [
                                                            "CA",
                                                            "US"
                                                        ],
                                                        "num_days_until_expired": -1,
                                                        "disallowed_countries": [],
                                                        "show_custom_instructions_in_user_libraries": False,
                                                        "key_type": "steam",
                                                        "visible": True,
                                                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                                                        "display_separately": False,
                                                        "redeemed_key_val": "GRAC5-P2ATX-T88AV",
                                                        "key_type_human_name": "Steam",
                                                        "steam_app_id": None,
                                                        "human_name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                                                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                                        "auto_expand": False,
                                                        "is_expired": False,
                                                        "class": "steambutton",
                                                        "keyindex": 0,
                                                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                                                        }
                                                    ]
                                                },
                                                "choices_remaining": 0,
                                                "currency": "USD",
                                                "is_giftee": False,
                                                "claimed": True,
                                                "total": 79.99,
                                                "path_ids": [
                                                "6337784953110528",
                                                "5906387817922560"
                                                ]
                                              }
                                              })
        product_info = [{"key": "8WB97-DXQQ8-CQW4T",
                         "key_type": "steam",
                         "platform_id": 445980,
                         "name": "Wizard of Legend",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key":"M0968-5PKWM-2LFAH",
                         "key_type": "steam",
                         "platform_id": 225540,
                         "name": "Just Cause 3 XXL Edition",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "LCGM6-DYY4V-RAQYH",
                         "key_type": "steam",
                         "platform_id": 378860,
                         "name": "Project CARS 2",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K6RJG-75NKD-68ANV",
                         "key_type": "steam",
                         "platform_id": 359100,
                         "name": "Q.U.B.E. 2",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "L0K0D-F4MXW-EXC94",
                         "key_type": "steam",
                         "platform_id": 514900,
                         "name": "\u003Eobserver_",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K7WEC-FTCJ4-7LHI6",
                         "key_type": "steam",
                         "platform_id": 535480,
                         "name": "Sundered",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K7YP7-PXXFK-M7PN5",
                         "key_type": "steam",
                         "platform_id": 680360,
                         "name": "Regions of Ruin",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K4NIP-5CAKI-HA5BG",
                         "key_type": "steam",
                         "platform_id": 368390,
                         "name": "Darkside Detective",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        #{"key": "GRAC5-P2ATX-T88AV",
                        # "key_type": "steam",
                        # "platform_id": None,
                        # "name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                        # "expired": False
                        # }
                        ]
        self.assertTrue(EqualInContent(sut.ChoiceKeyContent(), product_info))


    def test_ChoiceKeyContent_returns_platform_specific_product_info_for_choice_bundles(self):
        sut = HumbleLibrary({"NUDtNZdxFP7seeap": january_2019_monthly,
                             "Yv8pEek2ehcSppPk": assassinscreed_bundle,
                             "mvHZvHGE7dzzcGTC":{"amount_spent": 71.99,
                                                 "product": {
                                                    "category": "storefront",
                                                    "machine_name": "dragonsdogma2_deluxe_storefront",
                                                    "empty_tpkds": {},
                                                    "post_purchase_text": "",
                                                    "human_name": "Dragon's Dogma 2 - Deluxe Edition",
                                                    "partial_gift_enabled": True
                                                    },
                                                "gamekey": "mvHZvHGE7dzzcGTC",
                                                "uid": "XX5FHNZNHP351",
                                                "created": "2024-03-19T20:08:02.142843",
                                                "missed_credit": None,
                                                "subproducts": [],
                                                "total_choices": 0,
                                                "tpkd_dict": {
                                                    "all_tpks": [
                                                        {
                                                        "is_gift": False,
                                                        "machine_name": "dragonsdogma2_deluxe_preorder_us_steam",
                                                        "gamekey": "mvHZvHGE7dzzcGTC",
                                                        "exclusive_countries": [
                                                            "CA",
                                                            "US"
                                                        ],
                                                        "num_days_until_expired": -1,
                                                        "disallowed_countries": [],
                                                        "show_custom_instructions_in_user_libraries": False,
                                                        "key_type": "steam",
                                                        "visible": True,
                                                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                                                        "display_separately": False,
                                                        "redeemed_key_val": "GRAC5-P2ATX-T88AV",
                                                        "key_type_human_name": "Steam",
                                                        "steam_app_id": None,
                                                        "human_name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                                                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                                        "auto_expand": False,
                                                        "is_expired": False,
                                                        "class": "steambutton",
                                                        "keyindex": 0,
                                                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                                                        }
                                                    ]
                                                },
                                                "choices_remaining": 0,
                                                "currency": "USD",
                                                "is_giftee": False,
                                                "claimed": True,
                                                "total": 79.99,
                                                "path_ids": [
                                                "6337784953110528",
                                                "5906387817922560"
                                                ]
                                              }
                                              })
        product_info = []
        self.assertEqual(sut.ChoiceKeyContent("uplay"), [])

    def test_KeysContent_returns_product_info_for_all_orders(self):
        sut = HumbleLibrary({"NUDtNZdxFP7seeap": january_2019_monthly,
                             "Yv8pEek2ehcSppPk": assassinscreed_bundle,
                             "mvHZvHGE7dzzcGTC":{"amount_spent": 71.99,
                                                 "product": {
                                                    "category": "storefront",
                                                    "machine_name": "dragonsdogma2_deluxe_storefront",
                                                    "empty_tpkds": {},
                                                    "post_purchase_text": "",
                                                    "human_name": "Dragon's Dogma 2 - Deluxe Edition",
                                                    "partial_gift_enabled": True
                                                    },
                                                "gamekey": "mvHZvHGE7dzzcGTC",
                                                "uid": "XX5FHNZNHP351",
                                                "created": "2024-03-19T20:08:02.142843",
                                                "missed_credit": None,
                                                "subproducts": [],
                                                "total_choices": 0,
                                                "tpkd_dict": {
                                                    "all_tpks": [
                                                        {
                                                        "is_gift": False,
                                                        "machine_name": "dragonsdogma2_deluxe_preorder_us_steam",
                                                        "gamekey": "mvHZvHGE7dzzcGTC",
                                                        "exclusive_countries": [
                                                            "CA",
                                                            "US"
                                                        ],
                                                        "num_days_until_expired": -1,
                                                        "disallowed_countries": [],
                                                        "show_custom_instructions_in_user_libraries": False,
                                                        "key_type": "steam",
                                                        "visible": True,
                                                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                                                        "display_separately": False,
                                                        "redeemed_key_val": "GRAC5-P2ATX-T88AV",
                                                        "key_type_human_name": "Steam",
                                                        "steam_app_id": None,
                                                        "human_name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                                                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                                        "auto_expand": False,
                                                        "is_expired": False,
                                                        "class": "steambutton",
                                                        "keyindex": 0,
                                                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                                                        }
                                                    ]
                                                },
                                                "choices_remaining": 0,
                                                "currency": "USD",
                                                "is_giftee": False,
                                                "claimed": True,
                                                "total": 79.99,
                                                "path_ids": [
                                                "6337784953110528",
                                                "5906387817922560"
                                                ]
                                              }
                                              })
        product_info = [{"key": "8WB97-DXQQ8-CQW4T",
                         "key_type": "steam",
                         "platform_id": 445980,
                         "name": "Wizard of Legend",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key":"M0968-5PKWM-2LFAH",
                         "key_type": "steam",
                         "platform_id": 225540,
                         "name": "Just Cause 3 XXL Edition",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "LCGM6-DYY4V-RAQYH",
                         "key_type": "steam",
                         "platform_id": 378860,
                         "name": "Project CARS 2",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K6RJG-75NKD-68ANV",
                         "key_type": "steam",
                         "platform_id": 359100,
                         "name": "Q.U.B.E. 2",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "L0K0D-F4MXW-EXC94",
                         "key_type": "steam",
                         "platform_id": 514900,
                         "name": "\u003Eobserver_",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K7WEC-FTCJ4-7LHI6",
                         "key_type": "steam",
                         "platform_id": 535480,
                         "name": "Sundered",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K7YP7-PXXFK-M7PN5",
                         "key_type": "steam",
                         "platform_id": 680360,
                         "name": "Regions of Ruin",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "K4NIP-5CAKI-HA5BG",
                         "key_type": "steam",
                         "platform_id": 368390,
                         "name": "Darkside Detective",
                         "created": datetime.fromisoformat("2018-12-28T13:14:02.201818"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "GRAC5-P2ATX-T88AV",
                         "key_type": "steam",
                         "platform_id": None,
                         "name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                         "created": datetime.fromisoformat("2024-03-19T20:08:02.142843"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "AP3C-XN4R-8V4E-CLPM",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles India",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UXV7-3L7M-TW67-WAET",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles China",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "VKJY-7AVN-TKG7-MVUH",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles Russia",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UP3-4DED-A2FA-8086-E322",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed®",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "W9QG-KVGB-YX6M-6W8W",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Liberation HD",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UVNL-LHY7-GKR6-GE6A",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® III",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WBMB-GP83-9MWX-86NF",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® III - Tyranny of King Washington: The Infamy (DLC)",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WCGF-AEJX-GACU-XUBX",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® II Deluxe Edition",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "X8C7-GR6M-D87X-DM6E",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Unity",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WPAT-4YKP-AAMM-X4RG",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Brotherhood",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         }
                        ]
        self.assertTrue(EqualInContent(sut.KeysContent(), product_info))

    def test_KeysContent_returns_platform_specific_product_info_for_all_orders(self):
        sut = HumbleLibrary({"NUDtNZdxFP7seeap": january_2019_monthly,
                             "Yv8pEek2ehcSppPk": assassinscreed_bundle,
                             "mvHZvHGE7dzzcGTC":{"amount_spent": 71.99,
                                                 "product": {
                                                    "category": "storefront",
                                                    "machine_name": "dragonsdogma2_deluxe_storefront",
                                                    "empty_tpkds": {},
                                                    "post_purchase_text": "",
                                                    "human_name": "Dragon's Dogma 2 - Deluxe Edition",
                                                    "partial_gift_enabled": True
                                                    },
                                                "gamekey": "mvHZvHGE7dzzcGTC",
                                                "uid": "XX5FHNZNHP351",
                                                "created": "2024-03-19T20:08:02.142843",
                                                "missed_credit": None,
                                                "subproducts": [],
                                                "total_choices": 0,
                                                "tpkd_dict": {
                                                    "all_tpks": [
                                                        {
                                                        "is_gift": False,
                                                        "machine_name": "dragonsdogma2_deluxe_preorder_us_steam",
                                                        "gamekey": "mvHZvHGE7dzzcGTC",
                                                        "exclusive_countries": [
                                                            "CA",
                                                            "US"
                                                        ],
                                                        "num_days_until_expired": -1,
                                                        "disallowed_countries": [],
                                                        "show_custom_instructions_in_user_libraries": False,
                                                        "key_type": "steam",
                                                        "visible": True,
                                                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                                                        "display_separately": False,
                                                        "redeemed_key_val": "GRAC5-P2ATX-T88AV",
                                                        "key_type_human_name": "Steam",
                                                        "steam_app_id": None,
                                                        "human_name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                                                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                                        "auto_expand": False,
                                                        "is_expired": False,
                                                        "class": "steambutton",
                                                        "keyindex": 0,
                                                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                                                        }
                                                    ]
                                                },
                                                "choices_remaining": 0,
                                                "currency": "USD",
                                                "is_giftee": False,
                                                "claimed": True,
                                                "total": 79.99,
                                                "path_ids": [
                                                "6337784953110528",
                                                "5906387817922560"
                                                ]
                                              }
                                              })
        product_info = [{"key": "AP3C-XN4R-8V4E-CLPM",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles India",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UXV7-3L7M-TW67-WAET",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles China",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "VKJY-7AVN-TKG7-MVUH",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Chronicles Russia",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UP3-4DED-A2FA-8086-E322",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed®",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "W9QG-KVGB-YX6M-6W8W",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Liberation HD",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "UVNL-LHY7-GKR6-GE6A",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® III",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WBMB-GP83-9MWX-86NF",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® III - Tyranny of King Washington: The Infamy (DLC)",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WCGF-AEJX-GACU-XUBX",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® II Deluxe Edition",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "X8C7-GR6M-D87X-DM6E",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Unity",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         },
                        {"key": "WPAT-4YKP-AAMM-X4RG",
                         "key_type": "uplay",
                         "platform_id": None,
                         "name": "Assassin's Creed® Brotherhood",
                         "created": datetime.fromisoformat("2017-01-16T15:38:08.924170"),
                         "expired": False,
                         "registered": False
                         }
                        ]
        self.assertTrue(EqualInContent(sut.KeysContent(platforms=["uplay"]), product_info))


    def Inactive_test_UnownedKeysContent_returns_unowned_registerable_keys(self):
        library_info = {"rgGames": [
            {"appid": 2674810,
             "name": "Dragon's Dogma 2 Character Creator"
                },
            {"appid": 2054970,
             "name": "Dragon's Dogma 2"
                },
            {"appid": 445980,
             "name": "Wizard of Legend"
             },
            {"appid": 225540,
             "name": "Just Cause 3"
             },
            {"appid": 378860,
             "name": "Project CARS 2"
             }
            ]}
        license_info = [
                {"date": datetime(2024, 3, 19),
                 "title": "Dragon's Dogma 2 Character Creator & Storage",
                 "aq_method": "Complimentary"
                    },
                {"date": datetime(2024, 3, 19),
                 "title": "Dragon's Dogma 2",
                 "aq_method": "Retail"},
                {"date": datetime(2018, 12, 28),
                 "title": "Wizard of Legend",
                 "aq_method": "Retail"},
                {"date": datetime(2024, 3, 19),
                 "title": "Dragon's Dogma 2",
                 "aq_method": "Retail"},
                {"date": datetime(2024, 3, 19),
                 "title": "Dragon's Dogma 2",
                 "aq_method": "Retail"},
                ]
        #steam_library = SteamLibrary(library_info, license_info)
        sut = HumbleLibrary({"NUDtNZdxFP7seeap": january_2019_monthly,
                             "Yv8pEek2ehcSppPk": assassinscreed_bundle,
                             "mvHZvHGE7dzzcGTC":{"amount_spent": 71.99,
                                                 "product": {
                                                    "category": "storefront",
                                                    "machine_name": "dragonsdogma2_deluxe_storefront",
                                                    "empty_tpkds": {},
                                                    "post_purchase_text": "",
                                                    "human_name": "Dragon's Dogma 2 - Deluxe Edition",
                                                    "partial_gift_enabled": True
                                                    },
                                                "gamekey": "mvHZvHGE7dzzcGTC",
                                                "uid": "XX5FHNZNHP351",
                                                "created": "2024-03-19T20:08:02.142843",
                                                "missed_credit": None,
                                                "subproducts": [],
                                                "total_choices": 0,
                                                "tpkd_dict": {
                                                    "all_tpks": [
                                                        {
                                                        "is_gift": False,
                                                        "machine_name": "dragonsdogma2_deluxe_preorder_us_steam",
                                                        "gamekey": "mvHZvHGE7dzzcGTC",
                                                        "exclusive_countries": [
                                                            "CA",
                                                            "US"
                                                        ],
                                                        "num_days_until_expired": -1,
                                                        "disallowed_countries": [],
                                                        "show_custom_instructions_in_user_libraries": False,
                                                        "key_type": "steam",
                                                        "visible": True,
                                                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                                                        "display_separately": False,
                                                        "redeemed_key_val": "GRAC5-P2ATX-T88AV",
                                                        "key_type_human_name": "Steam",
                                                        "steam_app_id": None,
                                                        "human_name": "Dragon's Dogma 2 - Deluxe Edition (Pre-order)",
                                                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                                                        "auto_expand": False,
                                                        "is_expired": False,
                                                        "class": "steambutton",
                                                        "keyindex": 0,
                                                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                                                        }
                                                    ]
                                                },
                                                "choices_remaining": 0,
                                                "currency": "USD",
                                                "is_giftee": False,
                                                "claimed": True,
                                                "total": 79.99,
                                                "path_ids": [
                                                "6337784953110528",
                                                "5906387817922560"
                                                ]
                                              }
                                              })

        registerable_keys = [{"key": "K6RJG-75NKD-68ANV",
                              "key_type": "steam"},
                             {"key": "L0K0D-F4MXW-EXC94",
                              "key_type": "steam"},
                             {"key": "K7WEC-FTCJ4-7LHI6",
                              "key_type": "steam"},
                             {"key": "K7YP7-PXXFK-M7PN5",
                              "key_type": "steam"},
                             {"key": "K4NIP-5CAKI-HA5BG",
                              "key_type": "steam"},
                             {"key": "AP3C-XN4R-8V4E-CLPM",
                              "key_type": "uplay"},
                             {"key": "UXV7-3L7M-TW67-WAET",
                              "key_type": "uplay"},
                             {"key": "VKJY-7AVN-TKG7-MVUH",
                              "key_type": "uplay"},
                             {"key": "UP3-4DED-A2FA-8086-E322",
                              "key_type": "uplay"},
                             {"key": "W9QG-KVGB-YX6M-6W8W",
                              "key_type": "uplay"},
                             {"key": "UVNL-LHY7-GKR6-GE6A",
                              "key_type": "uplay"},
                             {"key": "WBMB-GP83-9MWX-86NF",
                              "key_type": "uplay"},
                             {"key": "WCGF-AEJX-GACU-XUBX",
                              "key_type": "uplay"},
                             {"key": "X8C7-GR6M-D87X-DM6E",
                              "key_type": "uplay"},
                             {"key": "WPAT-4YKP-AAMM-X4RG",
                              "key_type": "uplay"}]

class TestHumbleBundle(unittest.TestCase):
    
    def test_ProductMachineNames_returns_list_containing_product_machine_names(self):
        sut = self.CreateHumbleBundle(assassinscreed_bundle)
        product_machine_names = ["assassinscreed_chronicles_india_bundle_na_uplay",
                        "assassinscreed_chronicles_china_bundle_na_uplay",
                        "assassinscreed_chronicles_russia_bundle_na_uplay",
                        "assassinscreed_bundle_uplay",
                        "assassinscreed_liberationhd_bundle_uplay",
                        "assassinscreed3_bundle_uplay",
                        "assassinscreed3_washingtondlc_bundle_uplay",
                        "assassinscreed2_deluxe_bundle_uplay",
                        "assassinscreed_unity_bundle_na_uplay",
                        "assassinscreed_brotherhood_bundle_uplay"
                        ]
        self.assertEqual(sut.ProductMachineNames(), product_machine_names)

    def test_ProductMachineNames_returns_empty_list_when_no_products_match(self):
        sut = self.CreateHumbleBundle(assassinscreed_bundle)
        platforms = ["steam"]
        product_machine_names = []
        self.assertEqual(sut.ProductMachineNames(platforms), product_machine_names)

    def test_ProductMachineNames_returns_list_containing_product_machine_names_for_given_platforms(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        platforms = ["steam", "origin"]
        product_machine_names = ["donotfeedthemonkeys_monthly_steam",
                                 "starwars_squadrons_choice_origin"
                                 ]
        self.assertEqual(sut.ProductMachineNames(platforms), product_machine_names)

    def test_ProductRedeemKeys_returns_list_containing_product_redeem_keys(self):
        sut = self.CreateHumbleBundle(assassinscreed_bundle)
        product_redeem_keys = ["AP3C-XN4R-8V4E-CLPM",
                               "UXV7-3L7M-TW67-WAET",
                               "VKJY-7AVN-TKG7-MVUH",
                               "UP3-4DED-A2FA-8086-E322",
                               "W9QG-KVGB-YX6M-6W8W",
                               "UVNL-LHY7-GKR6-GE6A",
                               "WBMB-GP83-9MWX-86NF",
                               "WCGF-AEJX-GACU-XUBX",
                               "X8C7-GR6M-D87X-DM6E",
                               "WPAT-4YKP-AAMM-X4RG"
                               ]
        self.assertEqual(sut.ProductRedeemKeys(), product_redeem_keys)

    def test_ProductRedeemKeys_returns_list_containing_product_redeem_keys_for_given_platforms(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        platforms = ["steam", "origin"]
        product_redeem_keys = ["I8M0C-J4QHW-LGAH7",
                               "99HH-F8R4-DGX5-VTMK-4NH4"
                               ]
        self.assertEqual(sut.ProductRedeemKeys(platforms), product_redeem_keys)

    def test_ProductNames_returns_list_containing_product_names(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        product_names = ["Assassin's Creed® Chronicles India",
                         "Do Not Feed the Monkeys",
                         "Star Wars Squadrons"
                         ]
        self.assertEqual(sut.ProductNames(), product_names)

    def test_ProductNames_returns_list_containing_product_names_for_given_platforms(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        platforms = ["steam", "origin"]
        product_names = ["Do Not Feed the Monkeys",
                         "Star Wars Squadrons"
                         ]
        self.assertEqual(sut.ProductNames(platforms), product_names)

    def test_Products_returns_list_containing_products(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        order_dict = {"machine_name": mixed_key_bundle["product"]["machine_name"],
                     "name": mixed_key_bundle["product"]["human_name"],
                     "gamekey": mixed_key_bundle["gamekey"],
                     "created": mixed_key_bundle["created"],
                     "subproducts": mixed_key_bundle["subproducts"]
                      }
        product_dicts = mixed_key_bundle["tpkd_dict"]["all_tpks"]
        order_factory = OrderFactory()
        products = [order_factory.CreateStoreKeyOrder(order_dict, product_dict) for product_dict in product_dicts]
        self.assertEqual(sut.Products(), products)

    def test_Products_returns_list_containing_products_for_given_platforms(self):
        sut = self.CreateHumbleBundle(mixed_key_bundle)
        platforms = ["steam", "origin"]
        order_dict = {"machine_name": mixed_key_bundle["product"]["machine_name"],
                     "name": mixed_key_bundle["product"]["human_name"],
                     "gamekey": mixed_key_bundle["gamekey"],
                     "created": mixed_key_bundle["created"],
                     "subproducts": mixed_key_bundle["subproducts"]
                      }
        product_dicts = mixed_key_bundle["tpkd_dict"]["all_tpks"]
        order_factory = OrderFactory()
        products = [order_factory.CreateStoreKeyOrder(order_dict, product_dict) for product_dict in product_dicts if product_dict["key_type"] in platforms]
        self.assertEqual(sut.Products(platforms), products)

    def CreateHumbleBundle(self, order_dict):
        order_factory = OrderFactory()
        return order_factory.CreateOrder(order_dict)


class TestHumbleChoice(unittest.TestCase):
    
    def test_FullyChosen_returns_True_for_fully_chosen_choice_bundle(self):
        sut = self.CreateHumbleChoice(april_2021_choice)
        self.assertTrue(sut.FullyChosen())

    def test_FullyChosen_returns_False_for_not_fully_chosen_choice_bundle(self):
        sut = self.CreateHumbleChoice(june_2025_choice)
        self.assertFalse(sut.FullyChosen())

    def test_MissingAllChoiceInfo_and_0_choices_remaining_returns_True_for_fully_chosen_choice_bundle(self):
        sut = self.CreateHumbleChoice(january_2019_monthly)
        self.assertTrue(sut.FullyChosen())

    def test_MissingAllChoiceInfo_and_choices_remaining_returns_False_for_choice_bundle(self):
        order_dict = {}
        order_dict.update(january_2019_monthly)
        order_dict["choices_remaining"] = 1
        sut = self.CreateHumbleChoice(order_dict)
        self.assertFalse(sut.FullyChosen())

    def test_AllProductsRedeemed_returns_True_for_fully_redeemed_choice_bundle(self):
        sut = self.CreateHumbleChoice(april_2021_choice)
        self.assertTrue(sut.AllProductsRedeemed())

    def test_AllProductsRedeemed_returns_True_for_choice_bundle_with_expired_products(self):
        order_dict = {}
        order_dict.update(april_2024_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in april_2024_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            if not tpks.get("redeemed_key_val", None):
                dateStr = (datetime.now() + timedelta(days=-1)).isoformat()
                temp_dict["expiration_date"] = dateStr 
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        sut = self.CreateHumbleChoice(order_dict)
        self.assertTrue(sut.AllProductsRedeemed())

    def test_AllProductsRedeemed_returns_False_for_choice_bundle_with_redeemable_products(self):
        sut = self.CreateHumbleChoice(april_2024_choice)
        self.assertFalse(sut.AllProductsRedeemed())

    def test_FullyChosen_returns_True_for_limited_choice_bundle_and_0_choices_remaining(self):
        sut = self.CreateHumbleChoice(june_2020_choice)
        self.assertTrue(sut.FullyChosen())

    def test_FullyChosen_returns_False_for_limited_choice_bundle_and_choices_remaining(self):
        order_dict = {}
        order_dict.update(june_2020_choice)
        order_dict["choices_remaining"] = 1
        sut = self.CreateHumbleChoice(order_dict)
        self.assertFalse(sut.FullyChosen())

    def test_UnChosenChoices_returns_empty_dict_for_fully_chosen_choice_bundle(self):
        sut = self.CreateHumbleChoice(april_2021_choice)
        self.assertEqual(sut.UnChosenChoices(), {})

    def test_UnChosenChoices_returns_empty_dict_for_MissingAllChoiceInfo_and_choices_remaining(self):
        order_dict = {}
        order_dict.update(january_2019_monthly)
        order_dict["choices_remaining"] = 1
        sut = self.CreateHumbleChoice(order_dict)
        self.assertEqual(sut.UnChosenChoices(), {})

    def test_UnChosenChoices_returns_unchosen_choices_and_products_for_choice_bundle(self):
        sut = self.CreateHumbleChoice(june_2025_choice)
        choice_dict = {"havendock": ["havendock_choice_steam"],
                       "warhammer40000_boltgun": ["warhammer40k_boltgun_row_choice_steam"],
                       "legacyofkainsoulreaver12remastered": ["legacyofkaintmsoulreaver1and2remastered_row_choice_steam"],
                       "skerritual": ["skerrittual_choice_steam"],
                       "biped": ["biped_choice_steam"],
                       "bootdev_june2025_onemonthfree": ["bootdev1monthsubscription_june_choice_coupon"]    
                       }
        self.assertEqual(sut.UnChosenChoices(), choice_dict)

    def test_UnChosenChoices_returns_unchosen_choices_for_correct_platform_with_platform_preferences(self):
        order_dict = {}
        order_dict.update(april_2021_choice)
        order_dict["choices_remaining"] = 1
        order_dict["tpkd_dict"] = {}
        order_dict["tpkd_dict"]["all_tpks"] = []
        order_dict["tpkd_dict"]["all_tpks"] += april_2021_choice["tpkd_dict"]["all_tpks"]
        del order_dict["tpkd_dict"]["all_tpks"][0]
        platform_preferences = ["epic","steam"]
        sut =self.CreateHumbleChoice(order_dict)
        choice_dict = {"shenmue3": ["shenmue3_choice_epic_keyless"]}

        self.assertEqual(sut.UnChosenChoices(platform_preferences), choice_dict)

    def test_RedeemableProducts_returns_empty_list_for_redeemed_chosen_choices_for_fully_chosen_bundle(self):
        sut = self.CreateHumbleChoice(april_2021_choice)
        self.assertEqual(sut.RedeemableProducts(), [])

    def test_RedeemableProducts_returns_unexpired_redeemable_products(self):
        order_dict = {}
        order_dict.update(april_2024_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in april_2024_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            if not tpks.get("redeemed_key_val", None):
                dateStr = (datetime.now() + timedelta(days=-1)).isoformat()
                temp_dict["expiration_date"] = dateStr 
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        sut = self.CreateHumbleChoice(order_dict)
        self.assertEqual(sut.RedeemableProducts(), [])

    def test_RedeemableProducts_returns_unredeemable_products(self):
        sut = self.CreateHumbleChoice(april_2024_choice)
        products = ["fashionpolicesquad_choice_steam"]
        self.assertEqual(sut.RedeemableProducts(), products)


    def test_Updated_returns_true_after_calling_Update_with_object_containing_new_products(self):
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in june_2025_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        order_dict["tpkd_dict"]["all_tpks"].append({
          "is_gift": False,
          "machine_name": "biped_choice_steam",
          "gamekey": "rw3m6TUnb3eqmHzM",
          "exclusive_countries": [],
          "num_days_until_expired": -1,
          "disallowed_countries": [],
          "show_custom_instructions_in_user_libraries": False,
          "key_type": "steam",
          "visible": True,
          "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
          "display_separately": False,
          "redeemed_key_val": "redacted",
          "key_type_human_name": "Steam",
          "steam_app_id": 1071870,
          "human_name": "Biped",
          "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
          "auto_expand": True,
          "is_expired": False,
          "class": "steambutton",
          "keyindex": 0,
          "disclaimer": "Steam will not provide extra giftable copies of games you already own."
        })

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertTrue(sut.Updated())

    def test_choice_objects_contain_same_products_after_calling_Update_with_object_containing_new_products(self):
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in june_2025_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        order_dict["tpkd_dict"]["all_tpks"].append({
          "is_gift": False,
          "machine_name": "biped_choice_steam",
          "gamekey": "rw3m6TUnb3eqmHzM",
          "exclusive_countries": [],
          "num_days_until_expired": -1,
          "disallowed_countries": [],
          "show_custom_instructions_in_user_libraries": False,
          "key_type": "steam",
          "visible": True,
          "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
          "display_separately": False,
          "redeemed_key_val": "redacted",
          "key_type_human_name": "Steam",
          "steam_app_id": 1071870,
          "human_name": "Biped",
          "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
          "auto_expand": True,
          "is_expired": False,
          "class": "steambutton",
          "keyindex": 0,
          "disclaimer": "Steam will not provide extra giftable copies of games you already own."
        })

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertEqual(set(sut.ProductMachineNames()), set(other.ProductMachineNames()))

    def test_choice_Updated_returns_true_after_calling_Update_with_object_containing_new_choices(self):
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

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertTrue(sut.Updated())

    def test_choice_objects_contain_same_unchosen_choices_after_calling_Update_with_object_containing_new_choices(self):
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

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertEqual(set(sut.UnChosenChoices()), set(other.UnChosenChoices()))

    def test_Updated_returns_false_after_calling_Update_with_object_containing_new_product_data(self):
        order_dict = {}
        order_dict.update(april_2024_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in april_2024_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            if temp_dict["machine_name"] == "fashionpolicesquad_choice_steam":
                temp_dict["redeemed_key_val"] = "One-Day"
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        sut = self.CreateHumbleChoice(april_2024_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Update_updates_products_with_new_product_data(self):
        order_dict = {}
        order_dict.update(april_2024_choice)
        order_dict["tpkd_dict"] = {"all_tpks": []}
        for tpks in april_2024_choice["tpkd_dict"]["all_tpks"]:
            temp_dict = {}
            temp_dict.update(tpks)
            if temp_dict["machine_name"] == "fashionpolicesquad_choice_steam":
                temp_dict["redeemed_key_val"] = "One-Day"
            order_dict["tpkd_dict"]["all_tpks"].append(temp_dict)

        sut = self.CreateHumbleChoice(april_2024_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        for product in sut.Products():
            if product.ProductMachineName() == "fashionpolicesquad_choice_steam":
                self.assertTrue(product.Updated())
            else:
                self.assertFalse(product.Updated())

    def test_choice_Updated_returns_false_after_calling_Update_with_differing_machine_name(self):
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["product"] = {}
        order_dict["product"].update(june_2025_choice["product"])
        order_dict["product"]["machine_name"] = "april_2025_choice"
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

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())


    def test_choice_Updated_returns_false_after_calling_Update_with_differing_creation_date(self):
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["product"] = {}
        order_dict["product"].update(june_2025_choice["product"])
        order_dict["created"] = "2024-04-30T18:51:02.620236" 
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

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_choice_Updated_returns_false_after_calling_Update_with_differing_gamekey(self):
        order_dict = {}
        order_dict.update(june_2025_choice)
        order_dict["product"] = {}
        order_dict["product"].update(june_2025_choice["product"])
        order_dict["gamekey"] = "Z8KftUKAEf8zG7zY"
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

        sut = self.CreateHumbleChoice(june_2025_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_FullyChosen_returns_false_when_Update_called_with_object_containing_new_choices_on_a_fully_chosen_choice_bundle(self):
        order_dict = {}
        order_dict.update(april_2024_choice)
        order_dict["product"] = {}
        order_dict["product"].update(april_2024_choice["product"])
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
                april_2024_choice["product"]["all_choices"]["contentChoiceOptions"]["contentChoiceData"]["game_data"])
        order_dict["product"]["all_choices"]["productIsChoiceless"] = True

        sut = self.CreateHumbleChoice(april_2024_choice)
        other = self.CreateHumbleChoice(order_dict)
        sut.Update(other)
        self.assertFalse(sut.FullyChosen())

    def CreateHumbleChoice(self, order_dict):
        order_factory = OrderFactory()
        return order_factory.CreateOrder(order_dict)

class TestChoiceContent(unittest.TestCase):

    def test_AllProductMachineNames_returns_product_machine_name_for_single_tpkds(self):
        machine_name = "popupdungeon"
        tpkds = [{'machine_name': 'popupdungeon_row_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 349730, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': ['AR', 'AM', 'AZ', 'BD', 'BY', 'BT', 'BR', 'CL', 'CN', 'CO', 'CR', 'GE', 'HK', 'IN', 'ID', 'KZ', 'KG', 'MY', 'MX', 'MD', 'NP', 'PK', 'PE', 'PH', 'RU', 'SG', 'LK', 'TW', 'TJ', 'TH', 'TM', 'UA', 'UY', 'UZ', 'VN'], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'Popup Dungeon', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'FE5F2-IZM8G-BF685', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.AllProductMachineNames(), ["popupdungeon_row_choice_steam"])

    def test_AllProductMachineNames_returns_product_machine_names_for_multiple_tpkds(self):
        machine_name = "simulacra1and2"
        tpkds = [{'machine_name': 'simulacra_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 712730, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'SIMULACRA', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'K05PA-BLZYB-TZP39', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}, {'machine_name': 'simulacra2_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 1011190, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'SIMULACRA 2', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'ITBPA-KEDJZ-FEAXE', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.AllProductMachineNames(), ["simulacra_choice_steam", "simulacra2_choice_steam"])

    def test_AllProductMachineNames_returns_all_product_machine_names_for_single_tpkds_with_redemption_options_with_no_platform_pref(self):
        machine_name = "shenmue3"
        tpkds = [{'shenmue3_steam': [{'machine_name': 'shenmue3_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 878670, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'Shenmue III', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'N5HFI-8CQRV-K4BTK', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}], 'shenmue3_epic': [{'is_partial_gift': False, 'key_type': 'epic_keyless', 'machine_name': 'shenmue3_choice_epic_keyless', 'gamekey': 'A7CESV6Pp4ZWFarX', 'exclusive_countries': [], 'disallowed_countries': [], 'show_custom_instructions_in_user_libraries': False, 'third_party_product_id': '5d582c08e31a43128a61093a2c3ff7f0', 'visible': True, 'sold_out': False, 'instructions_html': '<a href="https://support.humblebundle.com/hc/articles/360020257973" target="_blank">Epic Game Store Instructions</a>', 'display_separately': True, 'direct_redeem': True, 'key_type_human_name': 'Epic Games', 'human_name': 'Shenmue III', 'auto_expand': False, 'is_expired': False, 'partial_gift_enabled': True, 'num_days_until_expired': -1}]}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.AllProductMachineNames(),["shenmue3_choice_steam", "shenmue3_choice_epic_keyless"])

    def test_ProductMachineNames_returns_product_machine_name_for_single_tpkds(self):
        machine_name = "popupdungeon"
        tpkds = [{'machine_name': 'popupdungeon_row_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 349730, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': ['AR', 'AM', 'AZ', 'BD', 'BY', 'BT', 'BR', 'CL', 'CN', 'CO', 'CR', 'GE', 'HK', 'IN', 'ID', 'KZ', 'KG', 'MY', 'MX', 'MD', 'NP', 'PK', 'PE', 'PH', 'RU', 'SG', 'LK', 'TW', 'TJ', 'TH', 'TM', 'UA', 'UY', 'UZ', 'VN'], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'Popup Dungeon', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'FE5F2-IZM8G-BF685', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.ProductMachineNames(), ["popupdungeon_row_choice_steam"])

    def test_ProductMachineNames_returns_product_machine_names_for_multiple_tpkds(self):
        machine_name = "simulacra1and2"
        tpkds = [{'machine_name': 'simulacra_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 712730, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'SIMULACRA', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'K05PA-BLZYB-TZP39', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}, {'machine_name': 'simulacra2_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 1011190, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'SIMULACRA 2', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'ITBPA-KEDJZ-FEAXE', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.ProductMachineNames(), ["simulacra_choice_steam", "simulacra2_choice_steam"])

    def test_ProductMachineNames_returns_first_product_machine_name_for_single_tpkds_with_redemption_options_with_no_platform_pref(self):
        machine_name = "shenmue3"
        tpkds = [{'shenmue3_steam': [{'machine_name': 'shenmue3_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 878670, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'Shenmue III', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'N5HFI-8CQRV-K4BTK', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}], 'shenmue3_epic': [{'is_partial_gift': False, 'key_type': 'epic_keyless', 'machine_name': 'shenmue3_choice_epic_keyless', 'gamekey': 'A7CESV6Pp4ZWFarX', 'exclusive_countries': [], 'disallowed_countries': [], 'show_custom_instructions_in_user_libraries': False, 'third_party_product_id': '5d582c08e31a43128a61093a2c3ff7f0', 'visible': True, 'sold_out': False, 'instructions_html': '<a href="https://support.humblebundle.com/hc/articles/360020257973" target="_blank">Epic Game Store Instructions</a>', 'display_separately': True, 'direct_redeem': True, 'key_type_human_name': 'Epic Games', 'human_name': 'Shenmue III', 'auto_expand': False, 'is_expired': False, 'partial_gift_enabled': True, 'num_days_until_expired': -1}]}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.ProductMachineNames(),["shenmue3_choice_steam"])

    def test_ProductMachineNames_returns_first_product_machine_name_for_single_tpkds_with_redemption_options_with_platform_pref(self):
        machine_name = "shenmue3"
        tpkds = [{'shenmue3_steam': [{'machine_name': 'shenmue3_choice_steam', 'show_custom_instructions_in_user_libraries': False, 'key_type': 'steam', 'visible': True, 'is_partial_gift': False, 'display_separately': False, 'steam_app_id': 878670, 'exclusive_countries': [], 'class': 'steambutton', 'num_days_until_expired': -1, 'is_gift': False, 'auto_expand': True, 'gamekey': 'A7CESV6Pp4ZWFarX', 'disallowed_countries': [], 'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>", 'key_type_human_name': 'Steam', 'human_name': 'Shenmue III', 'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.', 'redeemed_key_val': 'N5HFI-8CQRV-K4BTK', 'is_expired': False, 'partial_gift_enabled': True, 'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'}], 'shenmue3_epic': [{'is_partial_gift': False, 'key_type': 'epic_keyless', 'machine_name': 'shenmue3_choice_epic_keyless', 'gamekey': 'A7CESV6Pp4ZWFarX', 'exclusive_countries': [], 'disallowed_countries': [], 'show_custom_instructions_in_user_libraries': False, 'third_party_product_id': '5d582c08e31a43128a61093a2c3ff7f0', 'visible': True, 'sold_out': False, 'instructions_html': '<a href="https://support.humblebundle.com/hc/articles/360020257973" target="_blank">Epic Game Store Instructions</a>', 'display_separately': True, 'direct_redeem': True, 'key_type_human_name': 'Epic Games', 'human_name': 'Shenmue III', 'auto_expand': False, 'is_expired': False, 'partial_gift_enabled': True, 'num_days_until_expired': -1}]}]
        sut = ChoiceContent(machine_name, tpkds)
        self.assertEqual(sut.ProductMachineNames(["epic","steam"]),["shenmue3_choice_epic_keyless"])

class TestHumbleStoreKey(unittest.TestCase):
    
    def test_Expired_returns_false_for_key_without_expiration(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": None,
                                  "human_name": None},
                      "gamekey": None,
                      "created": "2024-04-30T18:51:02.620236",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type": None,
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": None
                                  }
                            ]
                        }
                      }
        sut = order_factory.CreateOrder(order_dict)
        self.assertFalse(sut.Expired())

    def test_Expired_returns_false_for_key_that_has_not_expired(self):
        order_factory = OrderFactory()
        future_date = datetime.now() + timedelta(days=1)
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": None,
                                  "human_name": None},
                      "gamekey": None,
                      "created": "2024-04-30T18:51:02.620236",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type": None,
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": None,
                                      "expiration_date": future_date.isoformat()
                                  }
                            ]
                        }
                      }
        sut = order_factory.CreateOrder(order_dict)
        self.assertFalse(sut.Expired())

    def test_Expired_returns_true_for_key_that_has_expired(self):
        order_factory = OrderFactory()
        future_date = datetime.now() + timedelta(days=-1)
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": None,
                                  "human_name": None},
                      "gamekey": None,
                      "created": "2024-04-30T18:51:02.620236",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type": None,
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": None,
                                      "expiration_date": future_date.isoformat()
                                  }
                            ]
                        }
                      }
        sut = order_factory.CreateOrder(order_dict)
        self.assertTrue(sut.Expired())

    def test_Updated_returns_true_after_calling_update_with_storekey_obj_with_new_data(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }

        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertTrue(sut.Updated())

    def test_Updated_returns_false_after_calling_update_with_no_new_data(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }


        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Updated_returns_false_after_calling_update_with_differing_machine_name(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }


        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront2",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Updated_returns_false_after_calling_update_with_differing_gamekey(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs123",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }


        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Updated_returns_false_after_calling_update_with_differing_creation_date(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }


        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-15T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Updated_returns_false_after_calling_update_with_differing_product_machine_name(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }


        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront2",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-15T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeem_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertFalse(sut.Updated())

    def test_Update_makes_the_storekey_equal_to_a_storekey_generated_from_the_update_dictionary(self):
        order_factory = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                  }
                            ]
                        }
                      }

        updated_order_dict = {"product": {"category": "storefront",
                                  "machine_name": "enshrouded_storefront",
                                  "human_name": "Enshrouded"},
                      "gamekey": "TSskvEHeqSfUbZAs",
                      "created": "2025-02-14T01:51:25.738781",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": "enshrouded_steam",
                                      "redeemed_key_val": "TMQTG-FRRFB-NY4EZ",
                                      "key_type": "steam",
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": "Enshrouded",
                                      "expiration_date": "2025-12-31T01:51:25.738781"
                                  }
                            ]
                        }
                      }

        sut = order_factory.CreateOrder(order_dict)
        other = order_factory.CreateOrder(updated_order_dict)
        sut.Update(other)
        self.assertEqual(sut, other)

class TestOrderFactory(unittest.TestCase):

    def test_unknown_category_raises_error(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "Unknownbundle"}}
        with self.assertRaises(ValueError):
            sut.CreateOrder(order_dict)

    def test_storefront_category_returns_storekey_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "storefront",
                                  "machine_name": None,
                                  "human_name": None},
                      "gamekey": None,
                      "created": "2024-04-30T18:51:02.620236",
                      "subproducts": [],
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type": None,
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": None
                                  }
                            ]
                        }
                      }
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleStoreKey) 

    def test_subscriptionplan_category_returns_humblechoice_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "subscriptionplan",
                                  "machine_name": None,
                                  "human_name": None},
                      "gamekey": None,
                      "created": "2024-04-30T18:51:02.620236",
                      "subproducts": [],
                      "total_choices": 0,
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type": None,
                                      "steam_app_id": None,
                                      "is_expired": False,
                                      "human_name": None
                                  }
                            ]
                        },
                      "choices_remaining": 0
                    }
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleChoice) 

    def test_subscriptioncontent_category_returns_humblechoice_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "subscriptioncontent",
                                  "machine_name": None,
                                  "human_name": None},
                        "gamekey": None,
                        "created": "2024-04-30T18:51:02.620236",
                        "subproducts": [],
                        "total_choices": 0,
                        "tpkd_dict": {
                            "all_tpks":
                                [
                                    {
                                    "machine_name": None,
                                    "redeem_key_val": None,
                                    "key_type": None,
                                    "steam_app_id": None,
                                    "is_expired": False,
                                    "human_name": None
                                    }
                                ]
                            },
                        "choices_remaining": 0
                        }

        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleChoice) 

    def test_bundle_category_returns_humblebundle_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "bundle",
                                  "machine_name": None,
                                  "human_name": None},
                        "gamekey": None,
                        "created": "2024-04-30T18:51:02.620236",
                        "subproducts": [],
                        "total_choices": 0,
                        "tpkd_dict": {
                            "all_tpks": []
                            }
                      }
                       
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleBundle) 

    def test_creates_humblestorefront_object(self):
        sut = OrderFactory()
        order_dict = {
                'amount_spent': 26.99,
                'product': {'category': 'storefront', 'machine_name': 'enshrouded_storefront', 'empty_tpkds': {}, 'post_purchase_text': '', 'human_name': 'Enshrouded', 'partial_gift_enabled': True},
                'gamekey': 'TSskvEHeqSfUbZAs',
                'uid': 'X9ZX7MZ0141FX',
                'created': '2025-02-14T01:51:25.738781',
                'missed_credit': None,
                'subproducts': [],
                'total_choices': 0,
                'tpkd_dict': {
                    'all_tpks': [
                        {'is_gift': False, 
                         'machine_name': 'enshrouded_steam',
                         'gamekey': 'TSskvEHeqSfUbZAs',
                         'exclusive_countries': [],
                         'num_days_until_expired': -1,
                         'disallowed_countries': [],
                         'show_custom_instructions_in_user_libraries': False,
                         'key_type': 'steam',
                         'visible': True,
                         'instructions_html': "<a href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'>Steam Instructions</a>",
                         'display_separately': False,
                         'redeemed_key_val': 'TMQTG-FRRFB-NY4EZ',
                         'key_type_human_name': 'Steam',
                         'steam_app_id': None,
                         'human_name': 'Enshrouded',
                         'preinstruction_text': 'Copy this key into the Steam client, or click Redeem to redeem in-browser.',
                         'auto_expand': False,
                         'is_expired': False,
                         'class': 'steambutton',
                         'keyindex': 0,
                         'disclaimer': 'Steam will not provide extra giftable copies of games you already own.'
                         }
                        ]
                    },
                'choices_remaining': 0,
                'currency': 'USD',
                'is_giftee': False,
                'claimed': True,
                'total': 29.99,
                'path_ids': ['5044586128277504', '6726378484858880']
                }
        order = sut.CreateOrder(order_dict)
        self.assertEqual(order, HumbleStoreKey({"order_machine_name": "enshrouded_storefront",
                                                "name": "Enshrouded",
                                                "humblekey": "TSskvEHeqSfUbZAs",
                                                "product_machine_name": "enshrouded_steam",
                                                "created": "2025-02-14T01:51:25.738781",
                                                "subproducts": [],
                                                "redeem_key": "TMQTG-FRRFB-NY4EZ",
                                                "key_type": "steam",
                                                "keyindex": 0,
                                                "platform_id": None,
                                                "is_expired": False
                                                })) 

    def test_creates_humblechoice_object_with_correct_humblestorefront_object(self):
        sut = OrderFactory()
        order_dict = {"amount_spent": 0,
                "product": {
                      "category": "subscriptioncontent",
                      "machine_name": "april_2024_choice",
                "empty_tpkds": {

                                },
                "choice_url": "april-2024",
                "post_purchase_text": "",
                "partial_gift_enabled": True,
                "human_name": "April 2024 Humble Choice",
                "is_subs_v2_product": False,
                "is_subs_v3_product": True
                },
                "gamekey": "Z8KftUKAEf8zG7zY",
                "uid": "AU62FJMHZHPCK",
                "created": "2024-04-30T18:51:02.620236",
                "missed_credit": None,
                "subproducts": [],
                         "total_choices": 0,
                "tpkd_dict": {
                    "all_tpks": [
                        {
                        "is_gift": False,
                        "machine_name": "victoria3_choice_steam",
                        "gamekey": "Z8KftUKAEf8zG7zY",
                        "exclusive_countries": [],
                        "num_days_until_expired": -1,
                        "disallowed_countries": [],
                        "show_custom_instructions_in_user_libraries": False,
                        "key_type": "steam",
                        "visible": True,
                        "instructions_html": "\u003Ca href='https://support.humblebundle.com/hc/articles/204008710-How-To-Redeem-Steam-Keys' target='_blank'\u003ESteam Instructions\u003C/a\u003E",
                        "display_separately": False,
                        "redeemed_key_val": "Z7AQM-3XTNN-PAATK",
                        "key_type_human_name": "Steam",
                        "steam_app_id": 529340,
                        "human_name": "Victoria 3",
                        "preinstruction_text": "Copy this key into the Steam client, or click Redeem to redeem in-browser.",
                        "auto_expand": False,
                        "is_expired": False,
                        "class": "steambutton",
                        "keyindex": 0,
                        "disclaimer": "Steam will not provide extra giftable copies of games you already own."
                        } 
                    ]
                },
                "choices_remaining": 0,
                "currency": "USD",
                "is_giftee": False,
                "claimed": True,
                "total": 11.99,
                "path_ids": [
                "6054619522990080",
                "5809080973852672"
                ]
            }

        order = sut.CreateOrder(order_dict)
        comp_storefront = HumbleStoreKey({"order_machine_name": "april_2024_choice",
                                        "name": "Victoria 3",
                                        "humblekey": "Z8KftUKAEf8zG7zY",
                                        "product_machine_name": "victoria3_choice_steam",
                                        "created": "2024-04-30T18:51:02.620236",
                                        "subproducts": [],
                                        "redeem_key": "Z7AQM-3XTNN-PAATK",
                                        "key_type": "steam",
                                        "keyindex": 0,
                                        "platform_id": 529340,
                                        "is_expired": False
                                        }) 
        self.assertTrue(order.Contains(comp_storefront))
