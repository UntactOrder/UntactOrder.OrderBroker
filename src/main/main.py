# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from substances import PosServer
from substances import getch

__DEBUG = True


if __name__ == '__main__':
    PosServer.server_config_parser(__DEBUG)
    PosServer.os_checker()
    PosServer.update_checker()
    if __DEBUG:
        getch()
