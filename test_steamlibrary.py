import unittest
from steamlibrary import SteamLibrary
from datetime import datetime

class TestSteamLibrary(unittest.TestCase):

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
        found_product, exact_match = sut.ContainsProduct(game_title)
        self.assertEqual((found_product, exact_match), (True, True))
        
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
        found_product, exact_match = sut.ContainsProduct(id=game_id)
        self.assertEqual((found_product, exact_match), (True, True))

    def test_ContainsProduct_returns_false_for_unowned_game(self):
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
        game_id = 1150535
        found_product, exact_match = sut.ContainsProduct(id=game_id)
        self.assertEqual((found_product, exact_match), (False, False))

    def test_ContainsBundle_returns_true_for_owned_bundle(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 617290,
             "name": "Remnant: From the Ashes"
                },
            {"appid": 1245150,
             "name": "Remnant: From the Ashes - Swamps of Corsus"
                },
            {"appid": 1344680,
             "name": "Remnant: From the Ashes - Subject 2923"
                }
            ]}
        license_info = []
        sut = SteamLibrary(library_info, license_info)
        self.assertTrue(sut.ContainsBundle(bundle_info))

    def test_ContainsBundle_returns_false_for_unowned_bundle(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 1150530,
             "name": "Wizard with a Gun",
                }
            ]}
        license_info = []
        sut = SteamLibrary(library_info, license_info)
        self.assertFalse(sut.ContainsBundle(bundle_info))

    def test_ContainsBundle_returns_false_for_partially_owned_bundle(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 617290,
             "name": "Remnant: From the Ashes"
                }
            ]}
        license_info = []
        sut = SteamLibrary(library_info, license_info)
        self.assertFalse(sut.ContainsBundle(bundle_info))

    def test_ContainsBundle_returns_true_for_partially_owned_bundle_with_free_unowned_packages(self):
        bundle_info = {'m_nDiscountPct': '20',
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 575436,
                            'm_rgIncludedAppIDs': [1286680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 5999,
                            'm_nFinalPriceInCents': 5999,
                            'm_nFinalPriceWithBundleDiscount': 4799},
                           {'m_nPackageID': 634830,
                            'm_rgIncludedAppIDs': [1769531],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634833,
                            'm_rgIncludedAppIDs': [1769532],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634836,
                            'm_rgIncludedAppIDs': [1769533],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634827,
                            'm_rgIncludedAppIDs': [1769530],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 1002525,
                            'm_rgIncludedAppIDs': [1621031],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002532,
                            'm_rgIncludedAppIDs': [1622260],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002533,
                            'm_rgIncludedAppIDs': [1621032],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0}],
                           'm_bIsCommercial': False,
                           'm_bRestrictGifting': False} 

        library_info = {"rgGames": [
            {"appid": 1286680,
             "name": "Tiny Tina's Wonderland"
                },
            {"appid": 1769531,
             "name": "Tiny Tina's Wonderlands: Gutton's Gamble"
                },
            {"appid": 1769532,
             "name": "Tiny Tina's Wonderlands: Molten Mirrors"
                },
            {"appid": 1769533,
             "name": "Tiny Tina's Wonderlands: Shattering Spectreglass"
             },
            {"appid": 1769530,
             "name": "Tiny Tina's Wonderlands: Coiled Captors"
             }
            ]}
        license_info = []
        sut = SteamLibrary(library_info, license_info)
        self.assertTrue(sut.ContainsBundle(bundle_info))

    def test_ProductRegisterDate_returns_acquisition_date_for_owned_game_by_title(self):

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
        acquisition_date = sut.ProductRegisterDate(game_title)
        self.assertEqual(acquisition_date, datetime(2023, 10, 31))

    def test_ProductRegisterDate_returns_acquisition_date_for_owned_game_by_id(self):
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
        acquisition_date = sut.ProductRegisterDate(id=game_id)
        self.assertEqual(acquisition_date, datetime(2023, 10, 31))

    def test_BundleRegisterDate_returns_acquisition_date_for_latest_appid_for_owned_bundle(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 617290,
             "name": "Remnant: From the Ashes"
                },
            {"appid": 1245150,
             "name": "Remnant: From the Ashes - Swamps of Corsus"
                },
            {"appid": 1344680,
             "name": "Remnant: From the Ashes - Subject 2923"
                }
            ]}
        license_info = [
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes",
                 "aq_method": "retail"
                    },
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes - Swamps of Corsus",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 4),
                 "title": "Remnant: From the Ashes - Subject 2923",
                 "aq_method": "retail"
                 }
                ]
        sut = SteamLibrary(library_info, license_info)
        acquisition_date = sut.BundleRegisterDate(bundle_info)
        self.assertEqual(acquisition_date, datetime(2025, 1, 4))
    
    def test_BundleRegisterDate_returns_acquisition_date_for_latest_appid_for_partially_owned_bundle_with_free_unowned_products(self):
        bundle_info = {'m_nDiscountPct': '20',
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 575436,
                            'm_rgIncludedAppIDs': [1286680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 5999,
                            'm_nFinalPriceInCents': 5999,
                            'm_nFinalPriceWithBundleDiscount': 4799},
                           {'m_nPackageID': 634830,
                            'm_rgIncludedAppIDs': [1769531],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634833,
                            'm_rgIncludedAppIDs': [1769532],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634836,
                            'm_rgIncludedAppIDs': [1769533],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634827,
                            'm_rgIncludedAppIDs': [1769530],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 1002525,
                            'm_rgIncludedAppIDs': [1621031],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002532,
                            'm_rgIncludedAppIDs': [1622260],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002533,
                            'm_rgIncludedAppIDs': [1621032],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0}],
                           'm_bIsCommercial': False,
                           'm_bRestrictGifting': False} 

        library_info = {"rgGames": [
            {"appid": 1286680,
             "name": "Tiny Tina's Wonderland"
                },
            {"appid": 1769531,
             "name": "Tiny Tina's Wonderlands: Gutton's Gamble"
                },
            {"appid": 1769532,
             "name": "Tiny Tina's Wonderlands: Molten Mirrors"
                },
            {"appid": 1769533,
             "name": "Tiny Tina's Wonderlands: Shattering Spectreglass"
             },
            {"appid": 1769530,
             "name": "Tiny Tina's Wonderlands: Coiled Captors"
             }
            ]}
        license_info = [
                {"date": datetime(2025, 1, 1),
                 "title": "Tiny Tina's Wonderland",
                 "aq_method": "retail"
                    },
                {"date": datetime(2025, 1, 2),
                 "title": "Tiny Tina's Wonderlands: Gutton's Gamble",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 3),
                 "title": "Tiny Tina's Wonderlands: Molten Mirrors",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 4),
                 "title": "Tiny Tina's Wonderlands: Shattering Spectreglass",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 5),
                 "title": "Tiny Tina's Wonderlands: Coiled Captors",
                 "aq_method": "retail"
                 }
                ]
        sut = SteamLibrary(library_info, license_info)
        acquisition_date = sut.BundleRegisterDate(bundle_info)
        self.assertEqual(acquisition_date, datetime(2025, 1, 5))

    def test_ProductAcquisitionMethod_returns_acquisition_method_for_owned_game_by_title(self):

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
        acquisition_method = sut.ProductAcquisitionMethod(game_title)
        self.assertEqual(acquisition_method, "retail")

    def test_ProductAcquisitionMethod_returns_acquisition_method_for_owned_game_by_id(self):
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
        acquisition_method = sut.ProductAcquisitionMethod(id=game_id)
        self.assertEqual(acquisition_method, "retail")

    def test_BundleAcquisitionMethod_returns_acquisition_method_for_owned_bundle(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 617290,
             "name": "Remnant: From the Ashes"
                },
            {"appid": 1245150,
             "name": "Remnant: From the Ashes - Swamps of Corsus"
                },
            {"appid": 1344680,
             "name": "Remnant: From the Ashes - Subject 2923"
                }
            ]}
        license_info = [
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes",
                 "aq_method": "retail"
                    },
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes - Swamps of Corsus",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 4),
                 "title": "Remnant: From the Ashes - Subject 2923",
                 "aq_method": "retail"
                 }
                ]
        sut = SteamLibrary(library_info, license_info)
        acquisition_method = sut.BundleAcquisitionMethod(bundle_info)
        self.assertEqual(acquisition_method, "retail")
    
    def test_BundleAcquisitionMethod_returns_acquisition_method_for_partially_owned_bundle_with_free_unowned_products(self):
        bundle_info = {'m_nDiscountPct': '20',
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 575436,
                            'm_rgIncludedAppIDs': [1286680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 5999,
                            'm_nFinalPriceInCents': 5999,
                            'm_nFinalPriceWithBundleDiscount': 4799},
                           {'m_nPackageID': 634830,
                            'm_rgIncludedAppIDs': [1769531],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634833,
                            'm_rgIncludedAppIDs': [1769532],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634836,
                            'm_rgIncludedAppIDs': [1769533],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 634827,
                            'm_rgIncludedAppIDs': [1769530],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 799},
                           {'m_nPackageID': 1002525,
                            'm_rgIncludedAppIDs': [1621031],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002532,
                            'm_rgIncludedAppIDs': [1622260],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0},
                           {'m_nPackageID': 1002533,
                            'm_rgIncludedAppIDs': [1621032],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': None,
                            'm_nFinalPriceInCents': 0,
                            'm_nFinalPriceWithBundleDiscount': 0}],
                           'm_bIsCommercial': False,
                           'm_bRestrictGifting': False} 

        library_info = {"rgGames": [
            {"appid": 1286680,
             "name": "Tiny Tina's Wonderland"
                },
            {"appid": 1769531,
             "name": "Tiny Tina's Wonderlands: Gutton's Gamble"
                },
            {"appid": 1769532,
             "name": "Tiny Tina's Wonderlands: Molten Mirrors"
                },
            {"appid": 1769533,
             "name": "Tiny Tina's Wonderlands: Shattering Spectreglass"
             },
            {"appid": 1769530,
             "name": "Tiny Tina's Wonderlands: Coiled Captors"
             }
            ]}
        license_info = [
                {"date": datetime(2025, 1, 1),
                 "title": "Tiny Tina's Wonderland",
                 "aq_method": "retail"
                    },
                {"date": datetime(2025, 1, 2),
                 "title": "Tiny Tina's Wonderlands: Gutton's Gamble",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 3),
                 "title": "Tiny Tina's Wonderlands: Molten Mirrors",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 4),
                 "title": "Tiny Tina's Wonderlands: Shattering Spectreglass",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 5),
                 "title": "Tiny Tina's Wonderlands: Coiled Captors",
                 "aq_method": "retail"
                 }
                ]
        sut = SteamLibrary(library_info, license_info)
        acquisition_method = sut.BundleAcquisitionMethod(bundle_info)
        self.assertEqual(acquisition_method, "retail")

    def test_BundleAcquisitionMethod_returns_mixed_for_owned_bundle_with_products_differing_in_acquisition_method(self):
        bundle_info = {'m_nDiscountPct': '17', 
                       'm_bMustPurchaseAsSet': 1,
                       'm_rgItems': [
                           {'m_nPackageID': 388789,
                            'm_rgIncludedAppIDs': [617290],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 3999,
                            'm_nFinalPriceInCents': 3999,
                            'm_nFinalPriceWithBundleDiscount': 3319},
                           {'m_nPackageID': 432094,
                            'm_rgIncludedAppIDs': [1245150],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829},
                           {'m_nPackageID': 470211,
                            'm_rgIncludedAppIDs': [1344680],
                            'm_bPackageDiscounted': False,
                            'm_nBasePriceInCents': 999,
                            'm_nFinalPriceInCents': 999,
                            'm_nFinalPriceWithBundleDiscount': 829}
                           ],
                       'm_bIsCommercial': False,
                       'm_bRestrictGifting': False}

        library_info = {"rgGames": [
            {"appid": 617290,
             "name": "Remnant: From the Ashes"
                },
            {"appid": 1245150,
             "name": "Remnant: From the Ashes - Swamps of Corsus"
                },
            {"appid": 1344680,
             "name": "Remnant: From the Ashes - Subject 2923"
                }
            ]}
        license_info = [
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes",
                 "aq_method": "retail"
                    },
                {"date": datetime(2025, 1, 1),
                 "title": "Remnant: From the Ashes - Swamps of Corsus",
                 "aq_method": "retail"
                 },
                {"date": datetime(2025, 1, 4),
                 "title": "Remnant: From the Ashes - Subject 2923",
                 "aq_method": "steam store"
                 }
                ]
        sut = SteamLibrary(library_info, license_info)
        acquisition_method = sut.BundleAcquisitionMethod(bundle_info)
        self.assertEqual(acquisition_method, "mixed")

