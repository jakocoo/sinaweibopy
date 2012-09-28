# -*- coding: utf-8 -*-

__author__ = 'kuliguo'
__version__ = '0.2'

import unittest
from weiboOAuthTest import weiboOAuthTest
from weiboNoAuthClientTest import weiboNoAuthClientTest
from weiboOAuthClientTest import weiboOAuthClientTest

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(weiboOAuthTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(weiboNoAuthClientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(weiboOAuthClientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)



