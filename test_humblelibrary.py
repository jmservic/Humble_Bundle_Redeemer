import unittest
from humblelibrary import OrderFactory, HumbleLibrary, HumbleChoice, HumbleBundle, HumbleStoreKey, ChoiceContent
from humble_ref_data import january_2019_monthly, april_2021_choice, june_2020_choice, april_2024_choice, june_2025_choice, assassinscreed_bundle

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
        platforms =["steam"]
        product_machine_names = []
        self.assertEqual(sut.ProductMachineNames(platforms), product_machine_names)

    #Test with a bundle that has mixed keys
    def test_ProductMachineNames_returns_list_containing_product_machine_names_for_the_given_platforms(self):
        pass

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
        
    def test_RedeemableProducts_returns_unredeemed_products(self):
        sut = self.CreateHumbleChoice(april_2024_choice)
        products = ["fashionpolicesquad_choice_steam"]
        self.assertEqual(sut.RedeemableProducts(), products)

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
                      "created": None,
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
                      "created": None,
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
                        "created": None,
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
                        "created": None,
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





