# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : PosServer.app & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by IRACK000
Description : ?
Reference : ?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.cli.apis & Last Modded : 2021.11.29. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
참고: [rich] https://www.youtube.com/watch?v=4zbehnz-8QU
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

builtin_print = print
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

if not os.path.isdir("data"):
    os.mkdir("data")
if not os.path.isdir("data/log"):
    os.mkdir("data/log")
sys.stderr = open("data/log/recent_run.log", "wt")

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


def hidecurs(on=True):
    """hidecurs(True) : hide console cursor
       hidecurs(False) : show console cursor"""
    builtin_print("\u001B[?25l" if on else "\u001B[?25h")


def clear():
    if os.name in ('nt', 'dos'):
        os.system("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")
    else:
        builtin_print("\033[H\033[J")  # print("\n" * 120)


def check_py_version():
    py_version = sys.version.split(" ")[0].split(".")
    if int(py_version[0]) < 3 or int(py_version[1]) < 8 or (int(py_version[1]) == 8 and int(py_version[2]) < 10):
        raise Exception("Python 3.8.10 or higher is required.")


def change_work_dir(current_file, echo=False):
    if os.path.abspath(os.getcwd()) == os.path.dirname(os.path.abspath(current_file)):
        workdir = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
        os.chdir(workdir)  # 작업 디렉토리를 프로젝트 루트로 변경
        if workdir not in sys.path:
            sys.path.append(workdir)  # 프로젝트 루트를 파이썬 모듈 경로에 추가
        if echo:
            print("Working directory changed to " + workdir)
