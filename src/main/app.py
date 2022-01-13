# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.app & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : ?
Reference : ?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys
from flask import Flask

if '__main__' == __name__:  # IDE가 실행 단위로 판단하지 않도록 통상적 경우와 리터럴 위치를 반대로 함.
    from cli.apis import check_py_version, change_work_dir  # 상대 경로 import; 파일 위치에 따라 코드가 수정 되어야 함.
    check_py_version()
    change_work_dir(__file__)


DEBUG = True

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=DEBUG)
