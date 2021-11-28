# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PosServer.substances & Last Modded : 2021.11.07. ###
Coded with Python 3.10 Grammar for Windows (CRLF) by IRACK000
참고: [rich] https://www.youtube.com/watch?v=4zbehnz-8QU
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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