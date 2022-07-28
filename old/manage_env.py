# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : development environment sync tool & Last Modded : 2022.01.10. ###
Coded with Python 3.10 Grammar by IRACK000
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os

py = "python"


def import_dependence_modules():
    os.system(f"{py} -m pip install -r ./requirements.txt")


def export_dependence_modules():
    os.system(f"{py} -m pip freeze > requirements_new.txt")


if __name__ == "__main__":
    version = input("\n1. 컴퓨터 기본 파이썬 버전(python)\n2. 파이썬 3.8.10(python3.8, Windows 7용)\n파이썬 버전을 선택하세요. : ")
    if version == "1":
        opt = input("\n1. python\n2. python3\n3. 직접 입력\n환경변수에 등록된 python3의 호출 키워드를 선택하세요. : ")
        py += ("3" if opt == "2" else "" if opt == "1" else input("버전을 입력하세요(python3.?) : ").replace("python", ""))
        if "python3.8" in py:
            raise Exception("Do not use python3.8 with build option 1.")
    elif version == "2":
        py += "3.8"
    print("선택된 파이썬 버전 : ", end='', flush=True)
    if 1 == os.system(f"{py} --version"):
        raise Exception(f"파이썬 버전({py})을 찾을 수 없습니다.")

    msg = "1. import(install) requirements\n2. export requirements\n\nselect option : "
    (import_dependence_modules if input(msg) == "1" else export_dependence_modules)()
