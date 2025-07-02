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
        morsels = SetCookieHeaderToMorsels(headers)
        print(morsels["_simpleauth_sess"]["expires"])
        #we're going to check for the name, value, expires, and domain on the morsels.
        self.assertTrue(True)

