# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : cx_Freeze setup.py & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by IRACK000
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import re
import sys
import subprocess
from cx_Freeze import setup, Executable

print("setup.py argv : ", sys.argv)

# CHECK PYSIDE BUILD VERSION
PYSIDE_VERSION = ("PySide6", "shiboken6")
PYTHON_VERSION = "python"
if "python" in sys.argv[-1]:
    PYTHON_VERSION = sys.argv.pop(-1)
    if PYTHON_VERSION == "python3.8":  # windows 7 support
        PYSIDE_VERSION = ("PySide2", "shiboken2")

# INCLUDE OR EXCLUDE MODULES
PACKAGES = [*PYSIDE_VERSION]
with open("requirements.txt", "rt", encoding='utf-8') as f:  # include
    requirements = [re.split(r"[~=<>]", pkg)[0] for pkg in f.readlines() if pkg != '' and pkg != '\n']
    PACKAGES.extend(requirements)
print("Included packages : ", PACKAGES)
installed_packages = re.split(r"[\r\n]", subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8'))
if input("\nWould you like to use requrations.txt for package exclusion? (y to yes) : ") == "y":
    EXCLUDES = {pkg.split('==')[0] for pkg in installed_packages if pkg != ''}
    EXCLUDES.add('tkinter')
    for pkg in PACKAGES:
        try:
            EXCLUDES.remove(pkg)
        except KeyError:
            pass
    print("Excluded packages : ", EXCLUDES, end="\n\n")
else:
    EXCLUDES = set()

# ADD FILES
FILES = ["res/"]

# PARSE CONFIG FROM SETTINGS.JSON
from src.main.gui.core.json_settings import Settings
settings = Settings().items

# TARGET
TARGET = Executable(
    script="src/main/main.py",
    base="Win32GUI" if sys.platform == "win32" else None,
    target_name=settings['app_name'].split()[0]+(  # 화이트 스페이스 이전까지만 반영
        ".exe" if sys.platform == "win32" else ""),
    shortcut_name=settings['app_name'].split()[0],
    shortcut_dir="DesktopFolder",
    icon="res/icon.ico"
)

# SETUP CX FREEZE
setup(
    name=settings['app_name'],
    version=settings['version'][1:],  # 맨 앞 v 문자 제거
    description=settings['description'],
    author=settings['copyright'],
    options={'build_exe': {'include_files': FILES,
                           'packages': PACKAGES,
                           'excludes': EXCLUDES,
                           'optimize': 2}},
    executables=[TARGET]
)
