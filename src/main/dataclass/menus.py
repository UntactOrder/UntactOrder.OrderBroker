# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.menus & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sqlite3


class Menu(object):
    """docstring for Menu."""

    def __init__(self, id, name, price):
        super(Menu, self).__init__()
        self.avaliable: bool = True
        self.pinned: bool = False
        self.id: str = id
        self.name: str = name
        self.price: int = price

    def set_pinned(self, pinned=True):
        self.pinned: bool = pinned

    def change_price(self, to):
        self.price: int = to

    def rename(self, new_name):
        self.name: str = new_name


class MenuList(dict):
    """docstring for MenuList."""

    _db = sqlite3.connect(os.getcwd()+"/resource/log/recent_run.log")

    @classmethod
    def get(cls):
        pass
