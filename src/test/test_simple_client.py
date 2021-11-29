import unittest

import socket

#from ..main.substances import PosServer
from ..main.networklayer.presentation import get
from ..main.networklayer.presentation import put
from ..main.networklayer.presentation import run
from ..main.networklayer.presentation import get_request


class MyTestCase(unittest.TestCase):
    def setUP(self):
        SERVER_ADDR = ('127.0.0.1', 53321)#PosServer.get_server_addr()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(SERVER_ADDR)
        print('서버에 연결 되었습니다.')

    def tearDown(self):
        self.client.close()

    def test_get_table_info(self):
        get("/customer/1", sokt=self.client, addr="")
        result = get_request(self.client, "")
        self.status = result['respond']
        print(result)

    def test_run_sign_in(self):
        if self.status == 'none':
            run("sign_in", {"id": 1, "pw": "123456"}, sokt=self.client, addr="")
            result = get_request(self.client, "")
            print(result)
        else:
            self.test_run_sign_up()

    def test_run_sign_up(self):
        run("sign_up", {"id": 1, "pw": "123456"}, sokt=self.client, addr="")
        result = get_request(self.client, "")
        print(result)

    def test_get_menu_data(self):
        get("/data/menu", sokt=self.client, addr="")
        result = get_request(self.client, "")
        print(result)

    def test_put_new_order(self):
        put("new_order", value={"0": "2", "1": "1", "2": "1"}, sokt=self.client, addr="")
        result = get_request(self.client, "")
        print(result)

    def test_get_order_list(self):
        get("/customer/1/orderlist", sokt=self.client, addr="")
        result = get_request(self.client, "")
        print(result)


if __name__ == '__main__':
    unittest.main()
