# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
pyinstaller builder
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os


if __name__ == "__main__":
    os.system("pip install pyinstaller")
    os.system("python -m PyInstaller main.spec")
    input()
