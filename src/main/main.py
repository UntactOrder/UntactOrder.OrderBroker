# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from src.main.substances import print
from src.main.substances import print_traceback
from src.main.substances import PosServer

DEBUG = False


if __name__ == '__main__':
    try:
        # before server start
        PosServer.server_config_parser(DEBUG)
        PosServer.os_checker()
        PosServer.update_checker()
        PosServer.print_menu_version(detailed=True)
        PosServer.clear()

        # server start
        pos = PosServer()
        pos.run_server()
        pos.run_pos_cui()

        # server close
        pos.quit()
    except Exception:
        print_traceback()

    # save logs
    PosServer.save_html()
    if DEBUG:
        PosServer.exit()
    else:
        PosServer.exit(prompt=None)
