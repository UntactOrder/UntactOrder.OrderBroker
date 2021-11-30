# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.dataclass.menus & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import datetime
import sqlite3
from configparser import ConfigParser


class Menu(object):
    """docstring for Menu."""

    def __init__(self, menu_id, name, price, menutype, pinned, soldout=False, available=True):
        super(Menu, self).__init__()
        self.__available: int = 1 if available else 0
        self.__soldout: int = 1 if soldout else 0
        self.__pinned: int = 1 if pinned else 0
        self.__id: str = menu_id
        self.__name: str = name
        self.__price: int = price
        self.__type: str = menutype

    def is_available(self):
        return self.__available

    def is_soldout(self):
        return self.__soldout

    def set_pinned(self, pinned=True):
        self.__pinned: int = 1 if pinned else 0

    def get_price(self):
        return self.__price

    def change_price(self, to):
        self.__price: int = to

    def get_type(self):
        return self.__type

    def change_type(self, to):
        self.__type: str = to

    def get_name(self):
        return self.__name

    def rename(self, new_name):
        self.__name: str = new_name

    def get_id(self):
        return self.__id

    def get_info(self):
        return self.__id, self.__name, self.__price, self.__type,\
               1 if self.__pinned else 0, 1 if self.__soldout else 0, 1 if self.__available else 0


class MenuList(object):
    """docstring for MenuList.
       db table name (menu version) form :
           f"menu{datetime.datetime.now()}".replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
       db column form : (id integer PRIMARY KEY autoincrement,
                         name text, price integer, type text, pinned integer, soldout integer, available integer)
    """

    config = ConfigParser()
    CONFIGPATH = os.path.dirname(
        os.path.abspath(os.path.dirname(os.path.abspath(__file__)))) + "/resource/setting.untactorder.ini"
    __MENUS = []
    _LOCATION = os.path.dirname(
        os.path.abspath(os.path.dirname(os.path.abspath(__file__)))) + "/resource/data/menus.untactorder.db"
    _COLUMNS_INIT = """(id integer PRIMARY KEY autoincrement,
     name text, price integer, type text, pinned integer, soldout integer, available integer)
     """
    _COLUMNS = "(name, price, type, pinned, soldout, available)"
    _CURRENT_MENU_VERSION = None

    @classmethod
    def get_menu_from_db(cls):
        """꼭 한번은 호출 해야 함"""
        config = cls.config
        config.read(cls.CONFIGPATH)
        if 'MENUINFO' not in config:
            config.add_section('MENUINFO')
        try:
            cls._CURRENT_MENU_VERSION = config['MENUINFO']['VERSION']
        except KeyError:
            input("주문 메뉴 버전 설정 데이터가 없습니다. 엔터를 눌러 가장 마지막에 생성된 버전으로 설정합니다. 다른 버전을 사용하기를 원하는 경우 서버 실행후 설정을 변경해주세요! : ")

        with sqlite3.connect(cls._LOCATION) as db:
            new_menu_setted = False
            cur = db.cursor()  # 커서 바인딩
            if cls._CURRENT_MENU_VERSION is None:
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [table[0] for table in cur.fetchall() if table[0] != 'sqlite_sequence']
                tables.sort()
                try:
                    cls._CURRENT_MENU_VERSION = tables[-1]
                except IndexError:
                    cls.make_new_menus()
                    cls._CURRENT_MENU_VERSION = cls.set_menus_to_db()
                    new_menu_setted = True
                config.set('MENUINFO', 'VERSION', cls._CURRENT_MENU_VERSION)
                with open(cls.CONFIGPATH, "wt") as fp:
                    config.write(fp)

            if not new_menu_setted:
                cur.execute("CREATE TABLE IF NOT EXISTS " + cls._CURRENT_MENU_VERSION + cls._COLUMNS_INIT)
                cur.execute(f"SELECT * from {cls._CURRENT_MENU_VERSION}")
                [cls.__MENUS.append(Menu(*read)) for read in cur.fetchall()]

    @classmethod
    def get_menu_version(cls, detailed=False) -> str:
        string = cls._CURRENT_MENU_VERSION if cls._CURRENT_MENU_VERSION is not None else "Not Initialized"
        if detailed:
            for menu in cls.__MENUS:
                string += f"\n{menu.get_info()}"
        return string

    @classmethod
    def get_menu_by_index(cls, index):
        return cls.__MENUS[index]

    @classmethod
    def make_new_menus(cls):
        while True:
            name = input("새로운 메뉴의 이름을 입력해 주세요. 입력을 마치려면 엔터만 입력 하세요. : ")
            if name == "":
                return
            while True:
                try:
                    price = int(input("메뉴의 가격을 입력해 주세요. : "))
                    break
                except ValueError:
                    print("숫자 이외의 문자가 입력 되었습니다.")
            menu_type = input("해당 메뉴의 타입을 입력해 주세요. 타입은 메뉴 분류를 의미 합니다. : ")
            pinned = input("해당 메뉴를 매장 이용자에게 추천 할까요? (y to confirm) : ") in ('y', 'Y')
            cls.__MENUS.append(Menu(len(cls.__MENUS), name, price, menu_type, pinned))

    @classmethod
    def set_menus_to_db(cls) -> str:
        with sqlite3.connect(cls._LOCATION) as db:  # 파일 없으면 새로 생김
            cur = db.cursor()  # 커서 바인딩
            values = [menu.get_info() for menu in cls.__MENUS]
            table_name = f"menu{datetime.datetime.now()}"\
                .replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
            print("New Menu Version Created : " + table_name)
            cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + cls._COLUMNS_INIT)
            cur.executemany(f"INSERT INTO {table_name} VALUES(?,?,?,?,?,?,?)", values)
            db.commit()
            return table_name

    @classmethod
    def to_dict(cls):
        dic = {}
        for menu in cls.__MENUS:
            if menu.is_soldout() or not menu.is_available():
                continue
            cur = dic[menu.get_id()] = dict()
            _, cur['name'], cur['price'], cur['type'], cur['pinned'], _, _ = menu.get_info()
        return dic


MenuList.get_menu_from_db()

if __name__ == "__main__":
    print(MenuList.get_menu_version(detailed=True))
