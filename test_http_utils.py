import unittest
from http_utils import SetCookieHeaderToMorsels

class TestHTTPUtils(unittest.TestCase):

    def test_multiple_headers_return_cookie_morsels(self):
        headers = [('Date', 'Wed, 02 Jul 2025 16:17:55 GMT'),
                   ('Content-Type', 'application/json; charset=utf-8'), 
                   ('Transfer-Encoding', 'chunked'),
                   ('Connection', 'keep-alive'),
                   ('CF-Ray', '958f74c08dd9bd3c-ATL'),
                   ('CF-Cache-Status', 'DYNAMIC'),
                   ('Set-Cookie', '_simpleauth_sess=eyJpZCI6IkJRanY2REhXNGMifQ==|1751473075|93759ece361452d1a72172abb854ce1df076a1a0; Domain=.humblebundle.com; Expires=Tue, 30-Sep-2025 16:17:55 GMT; Secure; HttpOnly; Path=/; SameSite=None'),
                   ('Vary', 'Cookie, Accept-Encoding'),
                   ('x-cloud-trace-context', '8fa27e674ea54ec2dbc019c92f90784d'),
                   ('Server', 'cloudflare')]
        expected_morsels = {"_simpleauth_sess":
                            {
                                "expires" : "Tue, 30-Sep-2025 16:17:55 GMT",
                                "domain" : ".humblebundle.com",
                                "value" : "eyJpZCI6IkJRanY2REhXNGMifQ==|1751473075|93759ece361452d1a72172abb854ce1df076a1a0" 
                            }
                }

        morsels = SetCookieHeaderToMorsels(headers)

        self.compare_cookies(morsels, expected_morsels)

    def test_single_header_returns_cookie_morsels(self):
        headers = [
                   ('Set-Cookie', '_simpleauth_sess=eyJpZCI6IkJRanY2REhXNGMifQ==|1751473075|93759ece361452d1a72172abb854ce1df076a1a0; Domain=.humblebundle.com; Expires=Tue, 30-Sep-2025 16:17:55 GMT; Secure; HttpOnly; Path=/; SameSite=None'),
                   ]
        expected_morsels = {"_simpleauth_sess":
                            {
                                "expires" : "Tue, 30-Sep-2025 16:17:55 GMT",
                                "domain" : ".humblebundle.com",
                                "value" : "eyJpZCI6IkJRanY2REhXNGMifQ==|1751473075|93759ece361452d1a72172abb854ce1df076a1a0" 
                            }
                }

        morsels = SetCookieHeaderToMorsels(headers)
        
        self.compare_cookies(morsels, expected_morsels)

    def test_multiple_set_cookie_headers_return_multiple_cookie_morsels(self):
        headers = [('Date', 'Wed, 02 Jul 2025 16:20:36 GMT'),
                   ('Content-Type', 'application/json; charset=utf-8'),
                   ('Transfer-Encoding', 'chunked'),
                   ('Connection', 'keep-alive'),
                   ('CF-Ray', '958f78aa9963e5c7-IAD'),
                   ('CF-Cache-Status', 'DYNAMIC'),
                   ('Cache-Control', 'private'),
                   ('Expires', 'Wed, 02 Jul 2025 16:20:36 GMT'),
                   ('Set-Cookie', 'hbreqsec=True; Domain=.humblebundle.com; Path=/'),
                   ('Vary', 'Cookie, Accept-Encoding'),
                   (':', 'hbflash=You%20are%20now%20signed%20in%21; Path=/'),
                   ('Set-Cookie', '_simpleauth_sess=eyJyZXBsX3ZhbHVlIjoiMWMxOTAwNDExNjMyZTBhNjMzNjAxM2MyYWQ0Mzg2YmEiLCJ1c2VyX2lkIjo1MDM1MjA1MTg5NTY2NDY0LCJpZCI6IkJRanY2REhXNGMiLCJhdXRoX3RpbWUiOjE3NTE0NzMyMzZ9|1751473236|ffe2eb47d4211996714aac61989e45d1e06e9f3b; Domain=.humblebundle.com; Expires=Tue, 30-Sep-2025 16:20:36 GMT; Secure; HttpOnly; Path=/; SameSite=None'),
                   ('x-cloud-trace-context', '112cc06e9cb26b2576b225e7f1203d9f'),
                   ('Server', 'cloudflare')]
        
        expected_morsels = {"hbreqsec": 
                                {
                                    "domain": ".humblebundle.com",
                                    "path": "/",
                                    "value": "True"
                                },
                            "_simpleauth_sess":
                                {
                                    "expires": "Tue, 30-Sep-2025 16:20:36 GMT",
                                    "domain": ".humblebundle.com",
                                    "value": "eyJyZXBsX3ZhbHVlIjoiMWMxOTAwNDExNjMyZTBhNjMzNjAxM2MyYWQ0Mzg2YmEiLCJ1c2VyX2lkIjo1MDM1MjA1MTg5NTY2NDY0LCJpZCI6IkJRanY2REhXNGMiLCJhdXRoX3RpbWUiOjE3NTE0NzMyMzZ9|1751473236|ffe2eb47d4211996714aac61989e45d1e06e9f3b"
                                }
                            }
        morsels = SetCookieHeaderToMorsels(headers)
        
        self.compare_cookies(morsels, expected_morsels)

    def compare_cookies(self, morsels, expected_morsels):
        for (name, morsel_dict) in expected_morsels.items():
            self.assertTrue(name in morsels)
            curr_cookie = morsels[name]
            for (key, value) in morsel_dict.items():
                if key == "value":
                    self.assertEqual(curr_cookie.value, value)
                    continue
                self.assertEqual(curr_cookie[key], value)
            
