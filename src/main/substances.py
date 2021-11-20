# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.substances & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import platform
from rich import print
from configparser import ConfigParser


try:
    from msvcrt import getch
except ModuleNotFoundError:
    import tty
    import termios

    def getch(char_width=1):
        """get a fixed number of typed characters from the terminal. Linux / Mac only
        https://www.reddit.com/r/learnpython/comments/7036k5/can_i_use_getch_on_macos_x/"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(char_width)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class PosServer(object):
    """docstring for PosServer."""

    __DEBUG = False
    __OPEN_WT = not __DEBUG
    __RUN_TYPE = ""
    __OS = ["", ""]  # [system, release]
    __IP = None
    __PORT = None
    __SERVER_INFO = dict()

    def __init__(self):
        pass

    def quit(self):
        """quit server and exit program"""
        self.exit()

    @staticmethod
    def exit(error_code=0, prompt="Press any key to exit program. "):
        """exit program"""
        if prompt is not None:
            print(prompt, end='', flush=True)
            getch()
        sys.exit(error_code)

    @classmethod
    def server_config_parser(cls, debug=False):
        cls.__DEBUG = debug
        cls.__OPEN_WT = not debug
        match len(sys.argv):
            case 1:
                pass
            case 2 | 4:
                if sys.argv[1] == "NOT_OPEN_WT":
                    cls.__OPEN_WT = False
                if len(sys.argv) == 4:
                    cls.__IP, cls.__PORT = sys.argv[2], sys.argv[3]
            case 3:
                cls.__IP, cls.__PORT = sys.argv[1], sys.argv[2]
            case _:
                cls.exit(-1, f"파라미터가 잘못 입력되었습니다.\n입력된 파라미터 : {sys.argv}\n아무키나 눌러 프로그램을 종료합니다.")

        if cls.__OPEN_WT:
            cls.__RUN_TYPE = "python " if os.path.splitext(sys.argv[0])[1] == ".py" else ""
        else:
            config = ConfigParser()
    #            config.read('settings.ini')

    @classmethod
    def os_checker(cls):
        cls.__OS[0], cls.__OS[1] = platform.system(), platform.release()
        match cls.__OS[0]:
            case "Darmin":
                cls.exit(-2, "MacOS는 공식적으로 지원하지 않습니다. 아무키나 눌러 프로그램을 종료합니다. ")
            case "Linux":
                print("Linux에서 실행되었습니다.")
            case "Windows":
                os.system("TITLE UntactOrder PosServer")
                if cls.__OS[1] >= "10":
                    if cls.__OPEN_WT:
                        print("Windows Terminal을 실행합니다.\n")
                        while os.system(f"wt {cls.__RUN_TYPE}{sys.argv[0]} NOT_OPEN_WT") != 0:
                            print("Windows Terminal이 설치되지 않았습니다. 인터넷을 통해 자동으로 설치를 시도합니다.\n"
                                  + "자동 설치에 동의하지 않으시면 서버 프로그램을 종료 후 Windows Store에서 Windows Terminal을 수동으로 설치해주세요.\n"
                                  + "설치 확인 메시지가 뜨는 경우 Y를 눌러 동의해주세요.\n\n")
                            if os.system("winget -v") != 0:
                                print("Windows 앱 설치 관리자가 최신버전이 아닙니다. 지금 열리는 스토어 창에서 업데이트 해주세요!")
                                os.system("start ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1")  # &mode=mini to mini mode
                                if input("업데이트를 완료 하셨나요? (y to yes) : ") != "y":
                                    cls.exit(-3, "앱 설치 관리자가 업데이트되지 않으면 실행할 수 없습니다!! 아무키나 눌러 프로그램을 종료합니다. ")
                            if os.system("winget install --id=Microsoft.WindowsTerminal -e") != 0:
                                print("설치에 실패하였습니다. 실패가 계속되는 경우 Windows Store에서 Windows Terminal을 수동으로 설치해주세요!\n\n")
                        cls.exit(0, None)
                    else:
                        print("윈도 10 이상 버전에서 실행되었습니다.")
                elif cls.__OS[1] >= "8":
                    print("윈도 10 미만 버전에서는 완벽하게 작동하지 않을 수 있습니다.")
                else:
                    cls.exit(-4, "윈도 7 이하 버전은 지원하지 않습니다. 아무키나 눌러 프로그램을 종료합니다. ")

    @classmethod
    def update_checker(cls):
        print("\nServer Program Version Info :")
        v_file = os.path.dirname(sys.argv[0]) + "\\resource\\version.rc"
        with open(v_file, 'r') as f:
            rc = f.read().replace("\n", "")
            file_info = rc[rc.find("StringFileInfo"):rc.rfind("VarFileInfo")].replace(" ", "").replace("(u'", "('").replace(",u'", ", '")
            table = file_info[file_info.rfind("[")+1:file_info.find("]")].replace("),", "").replace(")", "")
            for struct in table.split("StringStruct(")[1:]:
                key, val = struct.replace("'", "").split(", ")
                cls.__SERVER_INFO[key] = val
                print(key, cls.__SERVER_INFO[key])
