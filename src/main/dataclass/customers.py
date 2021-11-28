# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.customers & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import time
import sqlite3
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from console import *
from dataclass.menus import MenuList
from dataclass.orders import OrderList
from networklayer.session import sokt_close
from networklayer.session import send_continually
from networklayer.session import recv_continually
from networklayer.application import get_request
from networklayer.application import process_request


class Customer(object):
    """docstring for Customer."""

    def __init__(self, socket, addr, id, pw):
        super(Customer, self).__init__()
        self.__socket = socket
        self.__addr = addr
        self.id = id
        self.__pw = pw
        self.__orderlist = OrderList()

    def get_order_list(self):
        return self.__orderlist

    def sign_in(self, pw):
        return pw == self.__pw

    def is_logged_in(self):
        return self.__socket is not None

    def set_socket(self, socket, addr):
        self.__socket = socket
        self.__addr = addr

    def get_socket(self):
        return self.__socket

    def get_addr(self):
        return self.__addr

    def make_new_order(self, ordr):
        return self.__orderlist(self.id, ordr)

    def disconnect(self):
        sokt_close(self.__socket, self.__addr)
        self.set_socket(None, None)


class CustomerGroup(dict):
    """docstring for CustomerGroup.
       테이블 별 데이터 베이스 관리
    """

    _LOCATION = (os.getcwd() if __name__ != "__main__" else "..") + "/resource/data/tables.untactorder.db"
    print(_LOCATION)
    _COLUMNS_INIT = "(id integer PRIMARY KEY autoincrement, name text, price integer, type text, pinned integer, soldout integer, available integer)"
    _COLUMNS = "(name, price, type, pinned, soldout, available)"

    def __init__(self, popup_queue):
        super(CustomerGroup, self).__init__()
        self.__networking_data = {}
        self.__executor = ThreadPoolExecutor()
        self.__popup_queue = popup_queue
        self.__table_range = 10  # 테이블 개수 설정 (1번~10번) - ini 파일에 따라 자동 세팅
        self.__disabled_table = []  # 비활성화 되어있는 테이블 번호
        self.get_table_from_db()

    def __del__(self):
        for data in self.__networking_data:
            data[0].append(-1)
            data[1].append(-1)
        self.__executor.shutdown(wait=True)

    def get_table_from_db(self):
        """꼭 한번은 호출해야 함"""
        self.__table_range = 15
        log(f"[CUSTOMER] 테이블 수 {self.__table_range}로 설정됨")

    def sign_in(self, socket, addr, id, pw):
        if self[id].sign_in(pw):
            self[id].set_socket(socket, addr)
            net_data = ([], [])  # (send_queue, recv_queue)
            self.__networking_data[id] = net_data
            self.__executor.submit(self.manage_orders, self[id], net_data)
            log(f"[CUSTOMER:{addr}] sign_in - ok")
            return "ok"
        else:
            log(f"[CUSTOMER:{addr}] sign_in - wrong_pw")
            return "wrong_pw"

    def sign_up(self, socket, addr, id, pw):
        self[id] = Customer(socket, addr, id, pw)
        net_data = ([], [])  # (send_queue, recv_queue)
        self.__networking_data[id] = net_data
        self.__executor.submit(self.manage_orders, self[id], net_data)
        log(f"[CUSTOMER:{addr}] sign_ip - ok")
        return "ok"

    def check_id(self, id):
        if 0 < id <= self.__table_range:
            if id in self.__disabled_table:
                return "disabled"
            elif id in self.keys():
                if self[id].is_logged_in():
                    return "multi"
                else:
                    return "ok"
            else:
                return "none"
        else:
            return "null"

    def manage_orders(self, user, net_data):
        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread Started.")
        send_thread = Thread(target=send_continually, args=(user.get_socket(), user.get_addr(), net_data[0]))
        recv_thread = Thread(target=recv_continually, args=(user.get_socket(), user.get_addr(), net_data[1]))
        while True:
            data = get_request(recv_queue=net_data[1])
            if data == -1:
                break
            elif data is not None:
                process = process_request(data, send_queue=net_data[0])
                req, rep = next(process)
                match req:
                    case 'GET_MENU':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : GET_MENU")
                        rep['menu'] = MenuList.to_dict()
                        next(process)
                    case 'GET_ORDRLST':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : GET_ORDRLST")
                        rep['ordrlst'] = user.get_order_list().to_dict()
                        next(process)
                    case 'PUT_NORDR':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : PUT_NORDR")
                        ordr_id, status = user.make_new_order(data['value'])
                        req['time'] = ordr_id
                        req['status'] = status
                        next(process)
            else:
                time.sleep(0)  # Thread.yield()
        net_data[0].append(-1)
        user.disconnect()
        id = user.get_id()
        if len(user.get_order_list()) < 1:
            log(f"[CUSTOMER:{user.get_addr()}] Customer Object Deleted.")
            del self[id]
        del self.__networking_data[id]
        send_thread.join()
        recv_thread.join()
        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread Terminated.")


if __name__ == "__main__":
    group = CustomerGroup([])
