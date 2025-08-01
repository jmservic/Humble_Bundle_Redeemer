import unittest
from humblelibrary import OrderFactory, HumbleLibrary, HumbleChoice, HumbleBundle, HumbleStoreKey


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
                      "tpkd_dict": {
                          "all_tpks":
                            [
                                  {
                                      "machine_name": None,
                                      "redeem_key_val": None,
                                      "key_type_human_name": None,
                                      "steam_app_id": None,
                                      "is_expired": False
                                  }
                            ]
                        }
                      }
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleStoreKey) 

    def test_subscriptionplan_category_returns_humblechoice_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "subscriptionplan"}}
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleChoice) 

    def test_subscriptioncontent_category_returns_humblechoice_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "subscriptioncontent"}}
        order = sut.CreateOrder(order_dict)
        self.assertIsInstance(order, HumbleChoice) 

    def test_bundle_category_returns_humblebundle_object(self):
        sut = OrderFactory()
        order_dict = {"product": {"category": "bundle"}}
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
                                                "redeem_key": "TMQTG-FRRFB-NY4EZ",
                                                "key_type": "Steam",
                                                "platform_id": None,
                                                "is_expired": False
                                                })) 

