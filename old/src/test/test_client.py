from src.main.networklayer.presentation import get
from src.main.networklayer.presentation import put
from src.main.networklayer.presentation import run
from src.main.networklayer.presentation import get_respond

import socket
SERVER_ADDR = ('192.168.219.101', 53321)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(SERVER_ADDR)
    print('서버에 연결 되었습니다.')

    get("/customer/1", sokt=client, addr="")
    data = get_respond(client, "")
    print(data)
    run("sign_up" if data['respond'] == 'none' else "sign_in", {"id": 1, "pw": "123456"}, sokt=client, addr="")
    data = get_respond(client, "")
    print(data)

    get("/data/menu", sokt=client, addr="")
    data = get_respond(client, "")
    print(data)
    put("new_order", value={"0": "2", "1": "1", "2": "1"}, sokt=client, addr="")
    data = get_respond(client, "")
    print(data)
    get("/customer/1/orderlist", sokt=client, addr="")
    data = get_respond(client, "")
    print(data)



