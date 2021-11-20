# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclasses.orders & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from menus import MenuList


class Order(dict):
    """docstring for Order."""

    def __init__(self, id, jsn):
        super(Order, self).__init__()
        self.id = id


class OrderList(list):
    """docstring for OrderList."""

    def __init__(self):
        super(OrderList, self).__init__()

    def make_new_order(self, id, jsn):
        self.add(Order(id, jsn))
