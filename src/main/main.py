# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

py_version = sys.version.split(" ")[0].split(".")
if int(py_version[0]) < 3 or int(py_version[1]) < 8 or (int(py_version[1]) == 8 and int(py_version[2]) < 10):
    raise Exception("Python 3.8.10 or higher is required.")

if os.path.abspath(os.getcwd()) == os.path.dirname(os.path.abspath(__file__)):
    workdir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
    os.chdir(workdir)  # 작업 디렉토리를 프로젝트 루트로 변경
    if workdir not in sys.path:
        sys.path.append(workdir)  # 프로젝트 루트를 파이썬 모듈 경로에 추가

from src.main.substances import print
from src.main.substances import print_traceback
from src.main.substances import PosServer

DEBUG = False


if __name__ == '__main__':
    try:
        # before server start
        PosServer.server_config_parser(DEBUG)
        PosServer.os_checker()
        #PosServer.update_checker()
        PosServer.print_menu_version(detailed=True)

        # start server things
        with PosServer() as pos:
            pos.run_pos_main_ui()
    except Exception:
        print_traceback()

    # save logs
    PosServer.save_html()
    if DEBUG:
        PosServer.exit()
    else:
        PosServer.exit(prompt=None)
