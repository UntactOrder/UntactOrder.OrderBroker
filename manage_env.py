# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
development environment sync tool
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os


def import_dependence_modules():
    os.system("pip3 install -r ./requirements.txt")


def export_dependence_modules():
    os.system("pip3 freeze > requirements_new.txt")


if __name__ == "__main__":
    msg = "1. import(install) requirements\n2. export requirements\n\nselect option : "
    (import_dependence_modules if input(msg) == "1" else export_dependence_modules)()
