# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.customers & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from orders import OrderList


class Customer(object):
    """docstring for Customer."""

    def __init__(self, socket, id, pw):
        super(Customer, self).__init__()
        self.__socket = socket
        self.id = id
        self.__pw = pw
        self.__orderlist = OrderList()

    def get_new_order(self):
        pass

    def sign_in(self):
        pass

    def set_socket(self, socket):
        self.__socket = socket


class CustomerGroup(dict):
    """docstring for CustomerGroup."""

    def __init__(self):
        super(CustomerGroup, self).__init__()

    def sign_in(self, socket, id):
        user = self.id
        user.set_socket(socket)

    def sign_up(self, socket, id, pw):
        self[id] = Customer(socket, id, pw)
