# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.networklayer.session & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
참고: [java - python JSON 소켓 통신 프로그래밍] https://strawberry-smoothie.tistory.com/46
참고: [Excuter] https://docs.python.org/ko/3.7/library/concurrent.futures.html
               https://leo-bb.tistory.com/54
               https://hamait.tistory.com/833
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import socket
from concurrent.futures import ThreadPoolExecutor
import json


def manage_connections(sokt):
    num = 10
    while True:
        input_tmp = input('전송할 데이터를 입력하세요 : ')
        data = {'name': 'client', 'contents': input_tmp, 'num': num}
        print("send: name: {0}, contents: {1}, num: {2}".format(data['name'], data['contents'], data['num']))
        sokt.sendall(json.dumps(data).encode('UTF-8'))
        print(">> send finished")

        data = sokt.recv(4096)
        print(">> recv finished")
        data = json.loads(data)
        print("receive: name: {0}, contents: {1}, num: {2}".format(data['name'], data['contents'], data['num']))

        num = int(data['num']) + 1
    sokt.close()


def client():
    try:
        print('클라이언트 동작')
        # initialize Socket
        SERVER_ADDR = ('127.0.0.1', 50000)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(SERVER_ADDR)
            print('서버에 연결 되었습니다.')

            manage_connections(client)

    except Exception as e:
        print(e)
        input_tmp = input('아무거나 눌러서 종료')


def server():
    executor = ThreadPoolExecutor()
    try:
        print('서버 동작')
        # initialize Socket
        HOST = '127.0.0.1'  # localhost
        PORT = 51000  # 1~65535

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("WinError 수정 완료")
            server_socket.bind((HOST, PORT))  # 커널에 바인드.
            print("Bind 성공")
            server_socket.listen()  # 접속 대기.
            print("Listen 시작")

            while True:
                client_socket, addr = server_socket.accept()  # 클라이언트 소켓 리턴.
                print('클라이언트가 연결 되었습니다.')

                executor.submit(manage_connections, client_socket)

    except Exception as e:
        print(e)
        input_tmp = input('아무거나 눌러서 종료')


if __name__=='__main__':
    server()