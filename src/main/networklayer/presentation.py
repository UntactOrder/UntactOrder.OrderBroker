# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.networklayer.presentation & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import json

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from console import *
from networklayer.session import send
from networklayer.session import recv

DEBUG = True


def jsn2dic(jsn):
    dic = json.loads(jsn)
    if DEBUG:
        log(f"[JSN2DIC] {dic}")
    return dic


def dic2jsn(dic):
    if DEBUG:
        log(f"[DIC2JSN] {dic}")
    return json.dumps(dic).encode('UTF-8')


def respond(requested, respond_data, sokt=None, addr=None, send_queue=None):
    data = dic2jsn({'requested': requested, 'respond': respond_data})
    if send_queue is None:
        if sokt is None or addr is None:
            raise ValueError
        send(sokt, addr, data)
    else:
        send_queue.append(data)


def get_request(sokt=None, addr=None, recv_queue=None):
    if recv_queue is None:
        if sokt is None or addr is None:
            raise ValueError
        data = recv(sokt, addr)
        return jsn2dic(data)
    else:
        if len(recv_queue) > 0:
            data = recv_queue.pop(0)
            if data != -1:
                return jsn2dic(data)
            else:
                return -1


def get(uri, sokt=None, addr=None, send_queue=None):
    data = dic2jsn({'method': 'get', 'uri': uri})
    if send_queue is None:
        if sokt is None or addr is None:
            raise ValueError
        send(sokt, addr, data)
    else:
        send_queue.append(data)


def put(uri, value, sokt=None, addr=None, send_queue=None):
    data = dic2jsn({'method': 'put', 'uri': uri, 'value': value})
    if send_queue is None:
        if sokt is None or addr is None:
            raise ValueError
        send(sokt, addr, data)
    else:
        send_queue.append(data)


def run(uri, value, sokt=None, addr=None, send_queue=None):
    data = dic2jsn({'method': 'run', 'uri': uri, 'value': value})
    if send_queue is None:
        if sokt is None or addr is None:
            raise ValueError
        send(sokt, addr, data)
    else:
        send_queue.append(data)
