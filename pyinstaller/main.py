# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.main & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from multiprocessing import freeze_support

from substances import print
from substances import print_traceback
from substances import PosServer

DEBUG = False


if __name__ == '__main__':
    freeze_support()  # https://github.com/pyinstaller/pyinstaller/issues/4104
    try:
        # before server start
        PosServer.server_config_parser(DEBUG)
        PosServer.os_checker()
        PosServer.update_checker()
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
