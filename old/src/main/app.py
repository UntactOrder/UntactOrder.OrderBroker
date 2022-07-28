# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.app & Last Modded : 2022.03.17. ###
Coded with Python 3.10 Grammar by IRACK000
Description : PosServer HTTP Server
Reference : [create_app] https://stackoverflow.com/questions/57600034/waitress-command-line-returning-malformed-application-when-deploying-flask-web
            [Logging] https://stackoverflow.com/questions/52372187/logging-with-command-line-waitress-serve
            [flask] https://flask.palletsprojects.com/en/2.0.x/api/
            [route multi rules] https://stackoverflow.com/questions/17285826/flask-redirecting-multiple-routes
                                https://hackersandslackers.com/flask-routes/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from datetime import datetime, time
from functools import lru_cache

from flask import Flask, request, jsonify, make_response, Request, Response, abort
from waitress import serve

if '__main__' == __name__:  # IDE가 실행 단위로 판단하지 않도록 통상적 경우와 리터럴 위치를 반대로 함.
    from cli.apis import check_py_version, change_work_dir  # 상대 경로 import; 파일 위치에 따라 코드가 수정 되어야 함.
    check_py_version()
    change_work_dir(__file__)


DEBUG = True


# HTTP Error Codes
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503


# TODO: Logging


INVALID_ORDER_TOKEN_ERROR = "Invalid order token."


class JsonParseError(Exception):
    def __init__(self, msg):
        super(JsonParseError, self).__init__(msg)


class UnauthorizedClientError(Exception):
    def __init__(self, msg):
        super(UnauthorizedClientError, self).__init__(msg)


class ForbiddenAccessError(Exception):
    def __init__(self, msg):
        super(ForbiddenAccessError, self).__init__(msg)


# < Create Flask App ------------------------------------------------------------------------------------------------->
def create_app():
    app = Flask(__name__)

    service_denial_msg = "From 2:50 to 5:10, it is server inspection time. Sorry for the inconvenience. " \
                         "We would appreciate it if you could try again after the inspection."
    service_denial_start = time(2, 50, 0, 0)
    service_denial_end = time(5, 10, 0, 0)

    break_time_start = time(15, 30, 0, 0)  # time(15, 30, 0, 0)
    break_time_end = time(15, 30, 0, 0)  #time(16, 30, 0, 0)
    @lru_cache(maxsize=1)
    def break_time_msg(break_start, break_end):
        return f"From {f'{break_start}'[:-3]} to {f'{break_end}'[:-3]}, it is store break time. " \
               f"Sorry for the inconvenience. We would appreciate it if you could try again after the break."

    def server_status_noticer(func):
        def notice_service_denial(*args, **kwargs):
            # notice server inspection time
            if service_denial_start <= datetime.now().time() <= service_denial_end:
                abort(SERVICE_UNAVAILABLE, description="[ServerInspectionTimeError] " + service_denial_msg)
            # notice store break time
            if not break_time_start == break_time_end and break_time_start <= datetime.now().time() <= break_time_end:
                abort(SERVICE_UNAVAILABLE, description="[StoreBreakTimeError] "
                                                       + break_time_msg(break_time_start, break_time_end))
            # run function with error handling
            else:
                try:
                    return func(*args, **kwargs)
                except (ValueError | KeyError | TypeError | JsonParseError) as e:
                    abort(BAD_REQUEST, description=f"[{type(e).__name__}] {str(e)}")
                except (OSError | RuntimeError) as e:
                    abort(INTERNAL_SERVER_ERROR, description=f"[{type(e).__name__}] {str(e)}")
                except UnauthorizedClientError as e:
                    abort(UNAUTHORIZED, description=f"[{type(e).__name__}] {str(e)}")
                except ForbiddenAccessError as e:
                    abort(FORBIDDEN, description=f"[{type(e).__name__}] {str(e)}")
        notice_service_denial.__name__ = func.__name__  # rename function name
        return notice_service_denial

    def parse_json(req: Request, required_key: dict[str, type] = None) -> (str, dict):
        """
        Parse the request json
        :param req: Request object
        :param required_key: required key Info (json must have this keys)
        :return: dict when the request is valid, Response object when the request is invalid
        """
        personal_json = req.get_json()
        def check_keys() -> bool:  # TODO: check if get_json returns proper type of value or just returns str type
            for key, T in (required_key if required_key is not None else {}).items():
                if key not in personal_json or not personal_json[key] or not isinstance(personal_json[key], T):
                    return False
            return True
        if not personal_json or len(personal_json) >= len(required_key)+1 or not check_keys():
            raise JsonParseError("Json does not contain required keys.")
        elif 'token' not in personal_json or not isinstance(personal_json['token'], str):
            raise UnauthorizedClientError("Authorization token is not found.")
        else:
            return personal_json.pop('token'), personal_json

    @app.route('/')
    @server_status_noticer
    def index():
        """ To check if the server is running """
        return f"Hello, {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}!"

    #
    # process log in/out requests
    #
    @app.post('/sign')
    @server_status_noticer
    def process_sign_in_or_up() -> Response:
        """ Process the sign in or sign up request (CUSTOMER) - POST method
            Request:
                Body = {token: user_order_token, password: MD5(table_password)}
            Response:
                200 Login Success - Login Succeed
                401 Unauthorized  - User Order Token Not Found
                403 Forbidden     - Password Invalid
                404 Not Found     - Table Not Exists
        """
        parsed_json = parse_json(request)
        ap.process_sign_in_or_up(parsed_json[0], **parsed_json[1])
        result = ?
        if result:
            return jsonify({'status': "success"})
        else:
            404? 401?
            return jsonify({'status': "success"})

    @app.put('/sign')  # initial login process
    @app.patch('/sign')  # additional login process
    @server_status_noticer
    def process_admin_sign_in_or_up() -> Response:
        """ Process the sign in or sign up request (ADMIN) - Put/Patch method
            Request:
                if method is put:
                    Body = {token: firebase_id_token, password: MD5(cert_password)}
                else:  # when method is patch
                    Body = {main_token: firebase_id_token (main_token), token: firebase_id_token (additional_token),
                            password: MD5(cert_password)}
            Response:
                200 Login Success - Login Succeed
                403 Forbidden     - Password Invalid
                                  - Already Registered
        """
        parsed_json = parse_json(request)
        ap.process_sign_in_or_up(parsed_json[0], **parsed_json[1])
        result = ?
        if result:
            return jsonify({'status': "success"})
        else:
            403
            return jsonify({'status': "success"})

    @app.patch('/signout')
    @app.patch('/sign_out')
    @server_status_noticer
    def process_sign_out() -> Response:
        """ Process the sign out request (ADMIN, CUSTOMER) - POST method
            * Check if the token belongs to ADMIN first.
            * Customer will be able to sign out only when there's no order history in customer's table.
            Request:
                Body = if ADMIN      - {token: firebase_id_token, password: MD5(cert_password)}
                       elif CUSTOMER - {token: order_token, password: MD5(table_password)}       <= Delete Table
            Response:
                200 Login Success - Login Succeed
                401 Unauthorized  - Token Not Matched to any User/Admin
                403 Forbidden     - Password Invalid
        """
        parsed_json = parse_json(request)
        ap.process_sign_in_or_up(parsed_json[0], **parsed_json[1])
        result = ?
        if result:
            return jsonify({'status': "success"})
        else:
            404? 401?
            return jsonify({'status': "success"})

    #
    # process table order requests
    #
    @app.post('/table/<int:table_number>/status')
    def get_table_status(table_number: int) -> Response:
        """ Get table status - POST method
            Request:
                Body = if ADMIN      - {token: firebase_id_token}
                       elif CUSTOMER - {token: order_token}
            Response:
                200 Not Found      ['status': 0]
                200 Not Registered ['status': 1]
                200 Not Ordered    ['status': 2]
                200 Registered     ['status': 3]
                401 Unauthorized  - Token Not Matched to any User/Admin
        """
        return 0

    @app.patch('/table/<int:table_number>/password')
    def patch_table_password(table_number: int) -> Response:
        """ Change table password. - Patch method
            Request:
                Body = if ADMIN      - {token: firebase_id_token,
                                        password: MD5(cert_password), new_password: MD5(new_table_password)}
                       elif CUSTOMER - {token: order_token,
                                        password: MD5(table_password), new_password: MD5(new_table_password)}
            Response:
                200 Patch Success
                401 Unauthorized  - User Order Token Not Found
                403 Forbidden     - Password Invalid
                404 Not Found     - Table Not Exists
        """

    @app.post('/table/<int:table_number>/order/', defaults={'order_index': -1})
    @app.post('/table/<int:table_number>/order_history', defaults={'order_index': -1})
    @app.post('/table/<int:table_number>/order/<int:order_index>')
    def get_table_order_history(table_number: int, order_index: int) -> Response:
        """ Get table order history - POST method
            If order_index is -1 then get all order history. If order_index >= 0 then get specific order history.
            Request:
                Body = if ADMIN      - {token: firebase_id_token}
                       elif CUSTOMER - {token: order_token}
            Response:
                401 Unauthorized  - User Order Token Not Found
                404 Not Found     - Table Not Exists
                200 Success - [{ordered_by: user_order_token, alias: order_timestamp, status: order_status,
                               data: [{index: item_index, quantity: item_quantity, message: order_message}, ...]}, ...]
                * order_status: int - 0(ordered), 1(accepted), 2(proceeding), 3(served), 4(cancelled), 5(purchased)
        """
        return 0

    @app.put('/table/<int:table_number>/order')
    def put_new_order(table_number: int) -> Response:
        """ Put new order - Put method
            Request:
                Body = if ADMIN      - {token: firebase_id_token, password: MD5(cert_password)}
                       elif CUSTOMER - {token: order_token, password: MD5(table_password)}
                     += {data: [{index: item_index, quantity: item_quantity, message: order_message}, ...]}, ...]}
            Response:
                200 Order Success, {'order_index': ?}
                401 Unauthorized  - User Order Token Not Found
                403 Forbidden     - Password Invalid
                404 Not Found     - Table Not Exists
        """
        token, personal_json = parse_json(request, {'order': str})
        if token != ORDER_TOKEN:
            raise UnauthorizedClientError(INVALID_ORDER_TOKEN_ERROR)
        else:
            return jsonify({"token": ORDER_TOKEN})

    @app.post('/table/<int:table_number>/order/<int:order_index>/status')
    def get_order_status(table_number: int, order_index: int) -> Response:
        """ Get Order Status - Post method
            Request:
                Body = if ADMIN      - {token: firebase_id_token}
                       elif CUSTOMER - {token: order_token}
            Response:
                200 Ordered        ['status': 0]
                200 Accepted       ['status': 1]
                200 Processing     ['status': 2]
                200 Served         ['status': 3]
                200 Cancelled      ['status': 4]
                200 Purchased      ['status': 5]
                401 Unauthorized  - Token Not Matched to any TableUser/Admin
                404 Not Found     - Table Not Exists
        """
        return 0

    @app.patch('/table/<int:table_number>/order/<int:order_index>/status')
    def patch_order_status(table_number: int, order_index: int) -> Response:
        """ Patch Order Status - Patch method
            Request:
                Body = if ADMIN      - {token: firebase_id_token, password: MD5(cert_password), status: order_status}
                                        if order_status is purchased then += {payment_method: payment_method}
                                        * payment_method: int - 0~12; etc, cash, card, kakao_pay, naver_pay, payco,
                                                                      zero_pay, paypal, paytm, phone_pay, wechat_pay,
                                                                      ali_pay, jtnet_pay
                       elif CUSTOMER - {token: order_token, password: MD5(table_password), status: 4}  # cancel only
            Response:
                200 Patch Success
                401 Unauthorized  - Token Not Matched to any TableUser/Admin
                403 Forbidden     - Password Invalid
                                  - Not Allowed to Change Order Status
                404 Not Found     - Table Not Exists
        """
        return 0

    #
    # store administrative requests
    #
    @app.patch('/table/<int:table_number>/purchase')
    def process_purchase_request(table_number: int) -> Response:
        """ Process purchase request (ADMIN) - Patch method
            Request:
                Body = {token: firebase_id_token, password: MD5(cert_password), status: order_status}
                        if order_status is purchased then += {payment_method: payment_method}
                        * payment_method: int - 0~12; etc, cash, card, kakao_pay, naver_pay, payco,
                                                      zero_pay, paypal, paytm, phone_pay, wechat_pay,
                                                      ali_pay, jtnet_pay
            Response:
                200 Patch Success
                401 Unauthorized  - Unauthorized Token
                403 Forbidden     - Password Invalid
                404 Not Found     - Table Not Exists
        """

    @app.post('/table/status')
    def get_all_table_status(table_number: int, order_index: int) -> Response:
        """ Get All Table Status (ADMIN) - Post method
            Request:
                Body = {token: firebase_id_token}
            Response:
                200 Success, {0: true(; created), 1: false(; not created), ...}
                401 Unauthorized  - Unauthorized Token
        """
        return 0

    @app.post('/table')
    def get_all_table_history() -> Response:
        """ Get All Table History (ADMIN) - Post method
            Request:
                Body = {token: firebase_id_token}
            Response:
                200 Success - {0: [{ordered_by: user_order_token, alias: order_timestamp, status: order_status,
                                   data: [{index: item_index, quantity: item_quantity, message: order_message}, ...]},
                                   ...],
                               ...}  ## key is table number
                * order_status: int - 0(ordered), 1(accepted), 2(proceeding), 3(served), 4(cancelled), 5(purchased)
        """
        return 0

    @app.patch('/break_time')
    def set_break_time() -> Response:
        """ Set Break Time (ADMIN) - Patch method
            Request:
                Body = {token: firebase_id_token, password: MD5(cert_password),
                        break_time_start: "15:30", break_time_end: "16:30"}
            Response:
                200 Patch Success
                401 Unauthorized  - Unauthorized Token
                403 Forbidden     - Password Invalid
        """
        return 0

    #
    # requests related with store's menu
    #
    @app.post('/item', defaults={'option': "all"})
    @app.post('/item/version', defaults={'option': "version"})
    @app.post('/item/list', defaults={'option': "list"})
    @app.post('/item/sold_out', defaults={'option': "sold_out"})
    def get_item_list(option: str) -> Response:
        """ Get Item List (ADMIN) - Post method
            Request:
                Body = {token: firebase_id_token or order_token}
            Response:
                if option is all:
                    200 Success, {items: [{index: item_index, name: item_name, price: item_price, type: item_type,
                                           photo: item_photo_url, description: item_description,
                                           ingredient: item_ingredient, hashtag: item_hashtag, pinned: item_pinned}, ...],
                                  version: item_list_version, sold_out: [item_index, ...]}
                if option is version:
                    200 Success, {version: item_list_version}
                elif option is list:
                    200 Success, [{index: item_index, name: item_name, price: item_price, type: item_type,
                                   photo: item_photo_url, description: item_description, ingredient: item_ingredient,
                                   hashtag: item_hashtag, pinned: item_pinned}, ...]
                elif option is sold_out:
                    200 Success, {sold_out: [item_index, ...]}
                401 Unauthorized  - Unauthorized Token
        """
        return 0

    @app.patch('/item/<int:item_index>')
    @app.patch('/item', defaults={'item_index': -1})
    def patch_item(item_index: int) -> Response:
        """ Patch Item (ADMIN) - Patch method
            When item_index is -1, it means that it is a new item - Requires all information about the item
            When item_index is not -1, it means that it is an existing item - Requires only the information to be changed
            Request:
                Body = {token: firebase_id_token, password: MD5(cert_password),
                        item_info: {name: item_name, price: item_price, type: item_type,
                                    photo: item_photo_url, description: item_description,
                                    ingredient: item_ingredient, hashtag: item_hashtag, pinned: item_pinned}}
            Response:
                200 Patch Success
                401 Unauthorized  - Unauthorized Token
                403 Forbidden     - Password Invalid
                404 Not Found     - Item Not Found
        """
        return 0


if __name__ == '__main__':
    wsgiapp = create_app()
    serve(wsgiapp, host='0.0.0.0', port=5000, url_scheme='https')
