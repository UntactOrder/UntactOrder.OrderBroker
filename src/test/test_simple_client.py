import unittest

import socket

from src.main.substances import PosServer
from src.main.networklayer.presentation import get
from src.main.networklayer.presentation import put
from src.main.networklayer.presentation import run
from src.main.networklayer.presentation import get_respond

PosServer.server_config_parser(True)
SERVER_ADDR = PosServer.get_server_addr()
print(SERVER_ADDR)

client = None
status = ""


class MyTestCase(unittest.TestCase):
    def test1_connect(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(SERVER_ADDR)
        print("서버에 연결 되었습니다.")

    def test2_get_table_info(self):
        get("/customer/1", sokt=client, addr="")
        result = get_respond(client, "")
        global status
        status = result['respond']
        print(result)

    def test3_run_sign_in(self):
        if status == 'none':
            run("sign_in", {"id": 1, "pw": "123456"}, sokt=client, addr="")
            result = get_respond(client, "")
            print(result)
        else:
            run("sign_up", {"id": 1, "pw": "123456"}, sokt=client, addr="")
            result = get_respond(client, "")
            print(result)

    def test4_get_menu_data(self):
        get("/data/menu", sokt=client, addr="")
        result = get_respond(client, "")
        print(result)

    def test5_put_new_order(self):
        put("new_order", value={"0": "2", "1": "1", "2": "1"}, sokt=client, addr="")
        result = get_respond(client, "")
        print(result)

    def test6_get_order_list(self):
        get("/customer/1/orderlist", sokt=client, addr="")
        result = get_respond(client, "")
        print(result)

    def test7_close_server(self):
        client.close()


if __name__ == '__main__':
    unittest.main()
