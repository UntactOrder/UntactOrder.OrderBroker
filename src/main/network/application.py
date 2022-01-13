# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.network.application & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar by IRACK000
* <응용 계층>
* 데이터 가공 매서드 호출.
* qr 에서 테이블 번호 받기 -> 로그인 요청 -> 테이블 번호에 대해 비밀 번호 등록 여부 확인
* send to server : {"method": "get", "uri": "/customer/TABLE_NAME"}
* * recv : respond = {"requested": {"method": "get", "uri": "/customer/TABLE_NAME"},
                      *                     "respond": "ok|none|multi|null|disabled"}
* }
* 등록x -> 등록 하기(비밀 번호 새로 생성, 보내기)
* (3번 반복)등록o -> 일치 ->
* send to server : {"method": "run", "uri": "sign_up|sign_in", "value": {
    *                   "id": TABLE_NAME, "pw": PASSWORD
                                                *                   }}
                   * * recv : respond = {"requested": {"method": "run", "uri": "sign_up|sign_in", "value": TABLE_NAME},
*                     "respond": "ok|wrong_pw"}
* }
* 일치 or 등록 -> 메뉴 요청 및 받아 오기(서버)
                    * send to server : {"method": "get", "uri": "/data/menu"}
                                       * recv : respond = {"requested": {"method": "get", "uri": "/data/menu"},
                                                           *             "respond": "{
                                                                                    *                 "메인": {
*                     "0": {"name": "봉골레 파스타", "price": "12000", "pinned":"true"},
*                     "1": {"name": "새우 베이컨 필라프", "price": "13500", "pinned":"true"}
*                 }
*             }"}
               * -> 고른 메뉴 보내기(서버로)
                         * send to server : {"method": "put", "uri": "new_order", "value": {
*     "메인": {"0": "2", "1": "1", "2": "1"},
*     "사이드": {"0": "2", "1": "1", "2": "1"}
* }}
* recv : respond = {"requested": {"method": "put", "uri": "new_order", "value": "202111182208"}, "respond": "success"}
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from src.main.cli.apis import log
from src.main.network.session import sokt_close
import src.main.network.presentation as pr


def sign_in(cus_group, sokt, addr):
    log(f"[SIGNIN:{addr}] GET Table Method.")
    for i in (0, 1, 2):
        log(f"[SIGNIN:{addr}] GET Table Method - ({i+1}/3).")
        data = pr.get_request(sokt, addr)
        table = -1
        status = ""
        try:  # 테이블 네임의 get 요청 외에 모든 요청을 무시, 3회 시도 이후 연결 해제
            if data['method'] == 'get' and '/customer/' in data['uri']:
                table = int(data['uri'].split('/')[-1])
                status = cus_group.check_id(table)
                pr.respond(data, status, sokt, addr)
                if status in ("ok", "none"):
                    log(f"[SIGNIN:{addr}] GET Table Method - success.")
                    break
        except Exception:
            pass
        if i == 2 or status in ("multi", "disabled", "null") or data == -1:
            log(f"[SIGNIN:{addr}] SIGNIN Method - failed.")
            sokt_close(sokt, addr)
    if status == "none":
        sign_up(cus_group, table, sokt, addr)
    elif status == "ok":
        log(f"[SIGNIN:{addr}] SIGNIN Method.")
        for i in (0, 1, 2):  # 비밀 번호 입력은 3번 시도 가능
            log(f"[SIGNIN:{addr}] SIGNIN Method - ({i+1}/3).")
            data = pr.get_request(sokt, addr)
            try:
                if data['method'] == 'run' and data['uri'] == 'sign_in':
                    status = cus_group.sign_in(sokt, addr, table, data['value']['pw'])
                    data['value'] = data['value']['id']
                    pr.respond(data, status, sokt, addr)
                    if status == "ok":
                        log(f"[SIGNIN:{addr}] SIGNIN Method - success.")
                        return
            except Exception:
                pass
            if i == 2 or data == -1:
                log(f"[SIGNIN:{addr}] SIGNIN Method - failed.")
                sokt_close(sokt, addr)


def sign_up(cus_group, table, sokt, addr):
    log(f"[SIGNIN:{addr}] SIGNUP Method.")
    data = pr.get_request(sokt, addr)
    try:  # 테이블 네임의 get 요청 외에 모든 요청을 무시
        if data['method'] == 'run' and data['uri'] == 'sign_up':
            status = cus_group.sign_up(sokt, addr, table, data['value']['pw'])
            data['value'] = data['value']['id']
            pr.respond(data, status, sokt, addr)
            log(f"[SIGNIN:{addr}] SIGNUP Method - success.")
            return
    except Exception:
        pass
    log(f"[SIGNIN:{addr}] SIGNUP Method - failed.")
    sokt_close(sokt, addr)


get_request = pr.get_request


def process_request(addr, requested, respond_data=None, send_queue=None):
    """파라 미터가 이상한 요청을 확인 하여 무시 해야 함"""
    try:
        if respond_data is None:
            log(f"[PROCESS_REQ:{addr}] Generator Method.")
            respond_data = {}
            match requested['method']:
                case 'get':
                    if requested['uri'] == '/data/menu':
                        log(f"[PROCESS_REQ:{addr}] Yielded - GET_MENU.")
                        yield 'GET_MENU', respond_data
                        log(f"[PROCESS_REQ:{addr}] Resume - GET_MENU.")
                        pr.respond(requested, respond_data['menu'], send_queue=send_queue)
                    elif '/customer/' in requested['uri']:
                        if 'orderlist' == requested['uri'].split('/')[3]:
                            log(f"[PROCESS_REQ:{addr}] Yielded - GET_ORDRLST.")
                            yield 'GET_ORDRLST', respond_data
                            log(f"[PROCESS_REQ:{addr}] Resume - GET_ORDRLST.")
                            pr.respond(requested, respond_data['ordrlst'], send_queue=send_queue)
                case 'put':
                    if requested['uri'] == 'new_order':
                        if type(requested['value']) == dict:
                            log(f"[PROCESS_REQ:{addr}] Yielded - PUT_NORDR.")
                            yield 'PUT_NORDR', respond_data
                            log(f"[PROCESS_REQ:{addr}] Resume - PUT_NORDR.")
                            requested['value'] = respond_data['time']
                            pr.respond(requested, respond_data['status'], send_queue=send_queue)
        else:
            pr.respond(requested, respond_data, send_queue=send_queue)
    except Exception:
        pass
    yield None, None
