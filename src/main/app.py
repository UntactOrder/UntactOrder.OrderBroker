# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.app & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : ?
Reference : ?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys
from flask import Flask, request, jsonify
from waitress import serve

if '__main__' == __name__:  # IDE가 실행 단위로 판단하지 않도록 통상적 경우와 리터럴 위치를 반대로 함.
    from cli.apis import check_py_version, change_work_dir  # 상대 경로 import; 파일 위치에 따라 코드가 수정 되어야 함.
    check_py_version()
    change_work_dir(__file__)


DEBUG = True

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/hi')
def hi():  # put application's code here
    return 'hi!'


@app.route('/ip', methods=['GET'])
def name():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #return jsonify({'ip': request.remote_addr}), 200
    #return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200


if __name__ == '__main__':
    #http://daplus.net/python-flask-app-run-%EC%9D%84-%EB%8F%85%EB%A6%BD%ED%98%95%EC%9C%BC%EB%A1%9C-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%97%AC%EB%9F%AC-%EA%B3%A0%EA%B0%9D%EC%97%90%EA%B2%8C-%EC%84%9C%EB%B9%84/
    #app.run(debug=DEBUG, threaded=False, processes=3)
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
