# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.app & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
from flask import Flask

py_version = sys.version.split(" ")[0].split(".")
if int(py_version[0]) < 3 or int(py_version[1]) < 8 or (int(py_version[1]) == 8 and int(py_version[2]) < 10):
    raise Exception("Python 3.8.10 or higher is required.")

if os.path.abspath(os.getcwd()) == os.path.dirname(os.path.abspath(__file__)):
    workdir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    os.chdir(workdir)  # 작업 디렉토리를 프로젝트 루트로 변경
    if workdir not in sys.path:
        sys.path.append(workdir)  # 프로젝트 루트를 파이썬 모듈 경로에 추가

DEBUG = True

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
