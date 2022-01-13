# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.main & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by IRACK000
Description : ?
Reference : ?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import sys

if '__main__' == __name__:  # IDE가 실행 단위로 판단하지 않도록 통상적 경우와 리터럴 위치를 반대로 함.
    from cli.apis import check_py_version, change_work_dir  # 상대 경로 import; 파일 위치에 따라 코드가 수정 되어야 함.
    check_py_version()
    change_work_dir(__file__)

from src.main.substances import print
from src.main.substances import print_traceback
from src.main.substances import PosServer

DEBUG = False


if __name__ == '__main__':
    print(sys.argv)

'''
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
'''
