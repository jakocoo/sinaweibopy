# -*- coding: utf-8 -*-

__author__ = 'kuliguo'
__version__ = '0.2'

import unittest

from weibo import APIClient

class weiboNoAuthClientTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app_key = '1865902151'

    def test_isExpired(self):
        self.assertFalse(self.client.is_expires())

    def test_format(self):
        self.assertEqual(self.client.format, "json")

    def test_apitype(self):
        self.assertEqual(self.client.api_url, "https://api.weibo.com/2/")

#    def test_codeToLocation(self):
#        result = self.client.common.code_to_location(codes='100', source=self.app_key)
#        location = result[0].values()[0]
#        self.assertEqual(location, u'卡塔尔')


if __name__ == "__main__":
    unittest.main()
