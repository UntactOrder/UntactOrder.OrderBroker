# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.orders & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import datetime
import sqlite3

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dataclass.menus import MenuList
get_menu = MenuList.get_menu_by_index


class Order(dict):
    """docstring for Order."""

    ids = []

    def __init__(self, id, ordr):
        super(Order, self).__init__(ordr)
        self.__id: str = id
        self.__price: int = 0
        for menu_id, count in self.items():
            menu = get_menu(int(menu_id))
            self.__price += menu.get_price() * int(count)

    def get_id(self):
        return self.__id

    def get_price(self):
        return self.__price


class OrderList(list):
    """docstring for OrderList.
       고객 전화번호별 데이터베이스 관리
    """

    def __init__(self):
        super(OrderList, self).__init__()

    def make_new_order(self, ordr):
        """주문 아이디 중복 여부 확인 필요함"""
        _id = id = f"ordr{datetime.datetime.now()}".replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
        # 데이터베이스에 중복 아이디 있는지 검사
        sequence_num = 0
        while True:
            if _id in Order.ids:
                _id = id + f"s{sequence_num}"
                sequence_num += 1
            else:
                Order.ids.append(_id)
                id = _id
                break
        try:  # 메뉴 개수가 이상하거나 한 경우
            self.append(Order(id, ordr))
            stat = "success"
        except Exception:
            stat = "fail"
        return id, stat

    def set_data_to_db(self):
        pass

    def get_total_price(self):
        return sum([o.get_price() for o in self])

    def to_dict(self):
        return {o.get_id(): dict(o) for o in self}


if __name__ == '__main__':
    lst = OrderList()
    ordr = {"0": "2", "1": "1", "2": "1"}
    id, status = lst.make_new_order(ordr)
    print(f"id={id}, status={status}")
    print(lst.get_total_price())
    print(lst.to_dict())

    ordr = {"0": "1", "1": "1", "2": "0"}
    id, status = lst.make_new_order(ordr)
    print(f"id={id}, status={status}")
    print(lst.get_total_price())
    print(lst.to_dict())
