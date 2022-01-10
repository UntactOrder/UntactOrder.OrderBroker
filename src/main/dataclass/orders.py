# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.orders & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import datetime
import sqlite3

from src.main.cli import log
from src.main.dataclass.menus import MenuList
get_menu = MenuList.get_menu_by_index


class Order(dict):
    """docstring for Order."""

    ids = []

    def __init__(self, oid, user_id, ordr):
        super(Order, self).__init__(ordr)
        self.__id: str = oid
        self.__user_id: str = user_id
        self.__price: int = 0
        for menu_id, count in self.items():
            if int(count) == 0:
                del self[menu_id]
                continue
            menu = get_menu(int(menu_id))
            self.__price += menu.get_price() * int(count)

    def get_id(self):
        return self.__id

    def get_user_id(self):
        return self.__user_id

    def get_price(self):
        return self.__price


class OrderList(list):
    """docstring for OrderList.
       고객 전화 번호 별 데이터 베이스 관리
    """

    def __init__(self, user_id):
        super(OrderList, self).__init__()
        self.user_id = user_id

    def make_new_order(self, ordr):
        """주문 아이디 중복 여부 확인 필요함"""
        log(f"[ORDRLST] NEW ORDER from TABLE {self.user_id}.")
        _oid = oid = f"ordr{datetime.datetime.now()}".replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
        log(f"[ORDRLST] Temporary order id = {_oid}.")
        # 데이터베이스에 중복 아이디 있는지 검사
        sequence_num = 0
        while True:
            if _oid in Order.ids:
                log(f"[ORDRLST] {_oid} is already exists.")
                _oid = oid + f"s{sequence_num}"
                sequence_num += 1
            else:
                Order.ids.append(_oid)
                log(f"[ORDRLST] Order id setted : {_oid}.")
                oid = _oid
                break
        try:
            new_ordr = Order(oid, self.user_id, ordr)
            self.append(new_ordr)
            log(f"[ORDRLST] Order Object successfully added.")
            stat = "success"
        except Exception:  # 메뉴 개수가 이상하거나 한 경우
            new_ordr = None
            log(f"[ORDRLST] Order Object addition failed.")
            stat = "fail"
        return oid, stat, new_ordr

    def set_data_to_db(self):
        pass

    def get_total_price(self):
        return sum([o.get_price() for o in self])

    def to_dict(self):
        return {o.get_id(): dict(o) for o in self}


if __name__ == '__main__':
    lst = OrderList("1")
    ordr = {"0": "2", "1": "1", "2": "1"}
    _id, status, new_ordr = lst.make_new_order(ordr)
    print(f"id={_id}, status={status}")
    print(lst.get_total_price())
    print(lst.to_dict())

    ordr = {"0": "1", "1": "1", "2": "0"}
    _id, status, new_ordr = lst.make_new_order(ordr)
    print(f"id={_id}, status={status}")
    print(lst.get_total_price())
    print(lst.to_dict())
