# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.network.session & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar by IRACK000
Description : ?
Reference : [java - python JSON 소켓 통신 프로그래밍] https://strawberry-smoothie.tistory.com/46
            [Excuter] https://docs.python.org/ko/3.7/library/concurrent.futures.html
                      https://leo-bb.tistory.com/54
                      https://hamait.tistory.com/833
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import time
from concurrent.futures import ThreadPoolExecutor
from socket import socket as Socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from src.main.cli.apis import log

__server_socket = None
__accept_terminated = False


def init_server():
    """initialize Server Socket"""
    from src.main.substances import PosServer
    global __server_socket
    __server_socket = Socket(AF_INET, SOCK_STREAM)
    __server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    log("[SESSION] WinError 수정 완료")
    __server_socket.bind(PosServer.get_server_addr())  # 커널에 바인드.
    log("[SESSION] Bind 성공")
    __server_socket.listen()  # 접속 대기.
    log("[SESSION] Listen 시작")


def close_server():
    global __server_socket
    sokt_close(__server_socket, "SERVER")


def accept_continuously(connected):
    global __server_socket
    if __server_socket is None:
        init_server()
    while not __accept_terminated:
        client_socket, client_addr = __server_socket.accept()
        log(f"[SESSION] Client{client_addr}가 연결 되었습니다.")
        connected.append((client_socket, client_addr))


def manage_connections(cus_group):
    log("[SESSION] Manage_Connections Thread Started.")
    signin_pool = ThreadPoolExecutor()
    connected = []
    signin_pool.submit(accept_continuously, connected)
    from src.main.network.application import sign_in
    while not __accept_terminated:
        if len(connected) > 0:
            client_socket, client_addr = connected.pop(0)
            signin_pool.submit(sign_in, cus_group, client_socket, client_addr)
            log(f"[SESSION] {client_addr} is in signin_pool.")
        else:
            time.sleep(0)
    signin_pool.shutdown(wait=False)  # 기다리게 했더니 아예 안꺼지네....
    log("[SESSION] Manage_Connections Thread terminated.")


def terminate_accept():
    global __accept_terminated
    __accept_terminated = True


def send(sokt, addr, jsn):
    sokt.sendall(jsn)
    log(f"[SESSION:{addr}] send finished")


def recv(sokt: Socket, addr):
    data = sokt.recv(4096)
    if not data:  # 빈 문자열 수신시 연결을 끊어야 함
        data = -1
        log(f"[SESSION:{addr}] recv failed")
    else:
        log(f"[SESSION:{addr}] recv finished")
    return data


def send_continually(sokt, addr, send_queue):
    log(f"[SESSION:{addr}] Order Management Thread - Send Started.")
    while -1 not in send_queue:
        if len(send_queue) > 0:
            log(f"[SESSION:{addr}] send_con - send data found")
            jsn = send_queue.pop(0)
            log(f"[SESSION:{addr}] send_con - send start")
            send(sokt, addr, jsn)
            log(f"[SESSION:{addr}] send_con - send finished")
        else:
            time.sleep(0)  # Thread.yield()


def recv_continually(sokt, addr, recv_queue):
    log(f"[SESSION:{addr}] Order Management Thread - Recv Started.")
    while -1 not in recv_queue:
        log(f"[SESSION:{addr}] recv_con - recv start")
        data = recv(sokt, addr)
        log(f"[SESSION:{addr}] recv_con - recv finished")
        recv_queue.append(data)


def sokt_close(sokt, addr):
    if sokt is not None:
        sokt.close()
    log(f"[SESSION:{addr}] socket closed.")
