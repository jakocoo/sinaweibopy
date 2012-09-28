# -*- coding: utf-8 -*-

__author__ = 'kuliguo'
__version__ = '0.2'

import unittest
from weibo__login import login

class weiboOAuthClientTest(unittest.TestCase):
    def setUp(self):
        self.client = login()
        self.app_key = '1865902151'

    def test_isExpired(self):
        self.assertFalse(self.client.is_expires())

    #@unittest.skip("need to refine")
    def test_user_timeline(self):
        st = self.client.statuses.user_timeline()
        self.assertEqual(st.statuses[0].user.domain, u"xiaodandanwa")

    #@unittest.skip("need to refine")
    def test_codeToLocation(self):
        result = self.client.common.code_to_location(codes='100', source=self.app_key)
        location = result[0].values()[0]
        self.assertEqual(location, u'卡塔尔')

if __name__ == "__main__":
    unittest.main()
