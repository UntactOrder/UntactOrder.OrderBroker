# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.dataclass.customers & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar by IRACK000
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import time
import sqlite3
from concurrent.futures import ThreadPoolExecutor

from src.main.cli.apis import log
from src.main.dataclass.menus import MenuList
from src.main.dataclass.orders import OrderList
from src.main.network.session import sokt_close
from src.main.network.session import send_continually
from src.main.network.session import recv_continually
from src.main.network.application import get_request
from src.main.network.application import process_request


class Customer(object):
    """docstring for Customer."""

    def __init__(self, socket, addr, user_id: str, pw: str):
        super(Customer, self).__init__()
        self.__socket = socket
        self.__addr = addr
        self.__id: str = user_id
        self.__pw: str = pw
        self.__orderlist: OrderList = OrderList(user_id)
        self.__total_price: int = 0

    def __del__(self):
        if self.__socket is not None:
            self.disconnect()

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

    def get_id(self):
        return self.__id

    def get_addr(self):
        return self.__addr

    def get_total_price(self):
        return self.__total_price

    def make_new_order(self, ordr):
        result = self.__orderlist.make_new_order(ordr)
        self.__total_price += result[-1].get_price()
        return result

    def disconnect(self):
        sokt_close(self.__socket, self.__addr)
        self.set_socket(None, None)


class CustomerGroup(dict):
    """docstring for CustomerGroup.
       테이블 별 데이터 베이스 관리
    """

    _LOCATION = "data/tables.untactorder.db"
    _COLUMNS_INIT = "(id integer PRIMARY KEY, name text)"

    def __init__(self, popup_queue):
        super(CustomerGroup, self).__init__()
        self.__networking_data = {}
        self.__executor = ThreadPoolExecutor()
        self.__popup_queue = popup_queue
        self.__table_range = 10  # 테이블 개수 설정 (1번~10번) - db 읽어서 자동 세팅
        self.__disabled_table = []  # 비 활성화 되어 있는 테이블 번호
        self.get_table_from_db()

    def __del__(self):
        for data in self.__networking_data:
            data[0].append(-1)
            data[1].append(-1)
        self.__executor.shutdown(wait=False)  # 이것도 기다리니까 안끝남
        log("[CUSTOMER] del CustomerGroup Instance.")

    def get_table_from_db(self):
        """꼭 한번은 호출 해야 함"""
        self.__table_range = 25  # 임시로 이렇게
        log(f"[CUSTOMER] 테이블 수 {self.__table_range}로 설정됨")

    def sign_in(self, socket, addr, user_id: str, pw: str):
        if self[user_id].sign_in(pw):
            log(f"[CUSTOMER:{addr}] sign_in - ok")
            self[user_id].set_socket(socket, addr)
            net_data = ([], [])  # (send_queue, recv_queue)
            self.__networking_data[user_id] = net_data
            self.__executor.submit(self.manage_orders, self[user_id], net_data)
            return "ok"
        else:
            log(f"[CUSTOMER:{addr}] sign_in - wrong_pw")
            return "wrong_pw"

    def sign_up(self, socket, addr, user_id: str, pw: str):
        log(f"[CUSTOMER:{addr}] sign_ip - ok")
        self[user_id] = Customer(socket, addr, user_id, pw)
        net_data = ([], [])  # (send_queue, recv_queue)
        self.__networking_data[user_id] = net_data
        self.__executor.submit(self.manage_orders, self[user_id], net_data)
        return "ok"

    def check_id(self, user_id: str):
        if 0 < int(user_id) <= self.__table_range:
            if user_id in self.__disabled_table:
                return "disabled"
            elif user_id in self.keys():
                if self[user_id].is_logged_in():
                    return "multi"
                else:
                    return "ok"
            else:
                return "none"
        else:
            return "null"

    def manage_orders(self, user: Customer, net_data: tuple):
        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread Started.")
        self.__executor.submit(send_continually, user.get_socket(), user.get_addr(), net_data[0])
        self.__executor.submit(recv_continually, user.get_socket(), user.get_addr(), net_data[1])
        while True:
            data = get_request(recv_queue=net_data[1])
            if data == -1 or -1 in net_data[0]:
                log(f"[CUSTOMER:{user.get_addr()}] User Connection is Lost.")
                break
            elif data is not None:
                log(f"[CUSTOMER:{user.get_addr()}] Data Received.")
                process = process_request(user.get_addr(), data, send_queue=net_data[0])
                req, resp = next(process)
                match req:
                    case 'GET_MENU':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : GET_MENU")
                        resp['menu'] = MenuList.to_dict()
                        next(process)
                    case 'GET_ORDRLST':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : GET_ORDRLST")
                        resp['ordrlst'] = user.get_order_list().to_dict()
                        next(process)
                    case 'PUT_NORDR':
                        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread : PUT_NORDR")
                        ordr_id, status, new_ordr = user.make_new_order(data['value'])
                        resp['time'] = ordr_id
                        resp['status'] = status
                        self.__popup_queue.put(new_ordr)
                        next(process)
            else:
                time.sleep(0)  # Thread.yield()
        net_data[0].append(-1)
        user.disconnect()
        user_id = user.get_id()
        if len(user.get_order_list()) < 1:
            log(f"[CUSTOMER:{user.get_addr()}] Customer Object Deleted.")
            del self[user_id]
        del self.__networking_data[user_id]
        log(f"[CUSTOMER:{user.get_addr()}] Order Management Thread Terminated.")

    def process_payment(self):
        # 임시로 구현해 놓은 것
        if len(self) > 0:
            user_id = list(self.keys())[0]
            del self[user_id]
            #del self.__networking_data[user_id]


if __name__ == "__main__":
    group = CustomerGroup([])
