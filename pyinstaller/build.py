# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
pyinstaller builder
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os


# 3.10 빌드 오류 해결
# https://github.com/pyinstaller/pyinstaller/issues/6301


if __name__ == "__main__":
    #pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
    os.system("pip install pyinstaller")
    #python -m PyInstaller –onefile -n newName --icon=icon/server_logo.ico --hidden-import PyQt5.sip src/main/main.py --clean
    os.system("python -m PyInstaller --hidden-import PyQt5.sip main.spec")
    input()
    
