# -*- coding: utf-8 -*-

import unittest
from icebergsdk.api import IcebergAPI

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.api_handler = IcebergAPI()
        
    def test_sso(self):
        self.user = self.api_handler.sso("lol@lol.fr", "Yves", "Durand")
        self.assertEquals(self.user['username'], 'yvesdurant1032644')
        return self

    def test_getCart(self):
        currency = self.user.Cart.mine().currency
        self.assertEquals(currency, 'EUR')


