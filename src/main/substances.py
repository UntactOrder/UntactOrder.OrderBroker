# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.substances & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
참고: [rich] https://www.youtube.com/watch?v=4zbehnz-8QU
참고: [자동 시작] https://blog.naver.com/PostView.nhn?blogId=hunee726&logNo=220976778583&parentCategoryNo=&categoryNo=10&viewDate=&isShowPopularPosts=true&from=search
                https://liveyourit.tistory.com/23
참고: [gettext] https://minimilab.tistory.com/10
참고: [PyQt5] https://wikidocs.net/21849
             https://m.blog.naver.com/wjdrudtn0225/221999219060
참고: [curses] https://stackoverflow.com/questions/8677627/getting-mouse-presses-on-a-console-window-for-python
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import datetime
import platform
from configparser import ConfigParser

from rich import print
from rich.traceback import install as install_traceback
from rich.markdown import Markdown
from rich.console import Console
from rich.progress import track
from rich.columns import Columns
from rich.panel import Panel
from rich.theme import Theme
from rich.table import Table
from rich.live import Live

install_traceback()
sys.stderr = open(os.getcwd()+"/resource/log/recent_run.log", "wt")

theme = Theme({'success': "green", 'error': "bold red"})
log_console = Console(theme=theme, record=True, stderr=True)
console = Console(theme=theme)
eprint = log_console.print
log = log_console.log
csprint = console.print
cslog = console.log

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


def print_traceback():
    console.print_exception()
    log_console.print_exception()


def out(msg="", to=None):
    if to is None:
        to = (csprint, log)
    [f(msg) for f in to]


from dataclass.menus import MenuList


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
        sys.stderr.close()
        sys.exit(error_code)

    @classmethod
    def save_html(cls, path=None):
        """save program logs to html"""
        if path is None:
            path = os.getcwd() + f"/resource/log/{datetime.datetime.now()}.log.html".replace(' ', '_').replace(':', '-')
        out("Log saved to %s" % path)
        log_console.save_html(path)
        if cls.__OS[0] == "Windows":
            os.system(path)

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
            path = os.getcwd() + "/resource/setting.untactorder.ini"
            config.read(path)
            if 'SERVERINFO' not in config:
                config.add_section('SERVERINFO')
            try:
                cls.__IP = config['SERVERINFO']['ip']
            except KeyError:
                ip = input("서버 IP가 설정되지 않았습니다. 공유기에 포스기 컴퓨터를 고정IP로 설정한 후 해당 IP를 입력해주세요! 아무것도 입력하지 않으면 127.0.0.1을 사용합니다. : ")
                cls.__IP = '127.0.0.1' if ip == "" else ip
                config.set('SERVERINFO', 'ip', cls.__IP)
                with open(path, "wt") as fp:
                    config.write(fp)
            from configparser import NoOptionError
            try:
                cls.__PORT = config.getint('SERVERINFO', 'port')
            except NoOptionError:
                from random import randint
                port = input("서버 Port가 설정되지 않았습니다. 원하시는 포트번호를 입력해주세요! 49152~65535이외의 값을 입력하는 경우 랜덤으로 값을 생성합니다. : ")
                cls.__PORT = port if "49152" <= port <= "65535" else randint(49152, 65535)
                config.set('SERVERINFO', 'port', f'{cls.__PORT}')
                with open(path, "wt") as fp:
                    config.write(fp)

    @classmethod
    def os_checker(cls):
        cls.__OS[0], cls.__OS[1] = platform.system(), platform.release()
        match cls.__OS[0]:
            case "Darmin":
                cls.exit(-2, "MacOS는 공식적으로 지원하지 않습니다. 아무키나 눌러 프로그램을 종료합니다. ")
            case "Linux":
                out("Linux에서 실행되었습니다.")
            case "Windows":
                os.system("TITLE UntactOrder PosServer")
                if cls.__OS[1] >= "10":
                    if cls.__OPEN_WT:
                        out("Windows Terminal을 실행합니다.\n")
                        while os.system(f"wt {cls.__RUN_TYPE}{os.path.realpath(sys.argv[0])} NOT_OPEN_WT") != 0:
                            out("Windows Terminal이 설치되지 않았습니다. 인터넷을 통해 자동으로 설치를 시도합니다.\n"
                                    + "자동 설치에 동의하지 않으시면 서버 프로그램을 종료 후 Windows Store에서 Windows Terminal을 수동으로 설치해주세요.\n"
                                    + "설치 확인 메시지가 뜨는 경우 Y를 눌러 동의해주세요.\n\n")
                            if os.system("winget -v") != 0:
                                out("Windows 앱 설치 관리자가 최신버전이 아닙니다. 지금 열리는 스토어 창에서 업데이트 해주세요!")
                                os.system(
                                    "start ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1")  # &mode=mini to mini mode
                                if input("업데이트를 완료 하셨나요? (y to yes) : ") != "y":
                                    cls.exit(-3, "앱 설치 관리자가 업데이트되지 않으면 실행할 수 없습니다!! 아무키나 눌러 프로그램을 종료합니다. ")
                            if os.system("winget install --id=Microsoft.WindowsTerminal -e") != 0:
                                out("설치에 실패하였습니다. 실패가 계속되는 경우 Windows Store에서 Windows Terminal을 수동으로 설치해주세요!\n\n")
                        cls.exit(0, None)
                    else:
                        out("윈도 10 이상 버전에서 실행되었습니다.")
                elif cls.__OS[1] >= "8":
                    out("윈도 10 미만 버전에서는 완벽하게 작동하지 않을 수 있습니다.")
                else:
                    cls.exit(-4, "윈도 7 이하 버전은 지원하지 않습니다. 아무키나 눌러 프로그램을 종료합니다. ")

    @classmethod
    def update_checker(cls):
        out("\nServer Program Version Info :")
        v_file = os.getcwd() + "/resource/version.rc"
        with open(v_file, 'r') as f:
            rc = f.read().replace("\n", "")
            file_info = rc[rc.find("StringFileInfo"):rc.rfind("VarFileInfo")].replace(" ", "").replace("(u'", "('").replace(",u'", ", '")
            table = file_info[file_info.rfind("[") + 1:file_info.find("]")].replace("),", "").replace(")", "")
            for struct in table.split("StringStruct(")[1:]:
                key, val = struct.replace("'", "").split(", ")
                cls.__SERVER_INFO[key] = val
                out(f"{key} {cls.__SERVER_INFO[key]}")

    @staticmethod
    def print_menu_version():
        out("Menu Version Info: " + MenuList.get_menu_version())

    def f(self):
        import curses

        screen = curses.initscr()
        # curses.noecho()
        curses.curs_set(0)
        screen.keypad(1)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        screen.addstr("This is a Sample Curses Script\n\n")

        key = 0
        while key != 27:  # Esc to close
            key = screen.getch()
            # screen.erase()
            if key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                y, x = screen.getyx()
                screen.addstr('mx, my = %i,%i                \r' % (mx, my))
            screen.refresh()

        curses.endwin()


if __name__ == "__main__":
    try:
        out("[bold]this [cyan]is[/] normal text[/]")

        csprint("this is normal text", style="bold underline red on white")
        log("adding two numbers.", log_locals=True)

        table = Table(title="Star wars Movies")
        table.add_column("Released", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Box Office", style="green", justify="right")

        table.add_row("Dec 20, 2019", "Star Wars", "$952,110,690")
        table.add_row("May 25, 2018", "Solo", "$352,110,690")
        table.add_row("Dec 15, 2017", "Star Wars Last Jedi", "$1,332,110,690")

        out(table)

        text = """
### This is h3
        """
        csprint(Markdown(text))
        csprint(Markdown("""
# This is h1
        """))
        csprint(Markdown("""
## This is h2
1. hello World
2. hi?
        """))

        import time
        log("File Download Start")
        for i in track(range(10), description="Processing..."):
            print(f"working {i}")
            time.sleep(0.5)


        import json
        from urllib.request import urlopen
        index = 0

        def get_content(user, repeat):
            """Extract text from user dict."""
            country = user["location"]["country"]
            name = f"{user['name']['first']} {user['name']['last']}"
            string = f"[b]{name}[/b]\n[yellow]{country}"
            for i in range(repeat):
                string = string + f"\n{country}"
            return string

        def generate() -> Columns:
            """Make a new table."""
            global index
            user_renderables = [Panel(get_content(user, index), expand=True) for user in users]
            return Columns(user_renderables)

        users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]

        with Live(refresh_per_second=1, console=console, vertical_overflow="visible") as live:
            csprint("종료하려면 여기를 누르세요!")
            for row in range(3):
                time.sleep(1)
                index = row
                live.update(generate())
                log(f"{row}", f"description {row}", "[red]ERROR")


        '''import gettext
        import re
        import sys
        import locale

        # locale 설정을 ko_KR.UTF-8로 지정
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

        # 지정된 locale 설정을 확인
        loc = locale.getlocale()
        csprint(loc)

        # po 파일과 mo 파일을 설정해둔 파일명과 locale 폴더명을 bind 한다
        # po, mo 파일 설정방법은 '파이썬 gettext 이용하여 다국어 번역기 만들기' 확인
        # locale.bindtextdomain('gettext_test', '/home/practice/locale')
        # locale.textdomain('gettext_test')

        try:
            csprint(locale.gettext('안녕'))
        except Exception:
            print_traceback()
        '''
    except Exception:
        print_traceback()

    PosServer.save_html()
    PosServer.exit()
