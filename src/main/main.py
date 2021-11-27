# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from substances import print
from substances import print_traceback
from substances import PosServer

__DEBUG = True


if __name__ == '__main__':
    try:
        # before server start
        PosServer.server_config_parser(__DEBUG)
        PosServer.os_checker()
        PosServer.update_checker()
        PosServer.print_menu_version()

        # server start
        pos = PosServer()
        #pos.f()
    except Exception:
        print_traceback()

    # save logs
    PosServer.save_html()
    if __DEBUG:
        PosServer.exit()
    else:
        PosServer.exit(prompt=None)
