# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from substances import print
from substances import print_traceback
from substances import PosServer

__DEBUG = False


if __name__ == '__main__':
    try:
        PosServer.server_config_parser(__DEBUG)
        PosServer.os_checker()
        PosServer.update_checker()

        pos = PosServer()
        pos.f()
    except Exception:
        print_traceback()

    PosServer.save_html()
    if __DEBUG:
        PosServer.exit()
    else:
        PosServer.exit(prompt=None)
