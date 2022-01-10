# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
cx_Freeze & PyInstaller builder

# PyInstaller 3.10.0 빌드 오류 해결 관련
# https://github.com/pyinstaller/pyinstaller/issues/6301
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
import platform


if __name__ == "__main__":
    tool = "cx_Freeze"
    if input("1. cx_Freeze\n2. PyInstaller\n빌드에 사용할 툴을 선택하세요. : ") == "2":
        tool = "PyInstaller"

    if platform.system() == "Windows":
        os.system("TITLE cx_Freeze builder")
    elif platform.system() == "Linux":
        os.system("sudo apt-get install patchelf")

    py_version = sys.version.split(" ")[0].split(".")
    if int(py_version[0]) < 3 or int(py_version[1]) < 8 or (int(py_version[1]) == 8 and int(py_version[2]) < 10):
        raise Exception("Python 3.8.10 or higher is required.")

    version = input("\n1. 컴퓨터 기본 파이썬 버전(python)\n2. 파이썬 3.8.10(python3.8, Windows 7용)\n빌드에 사용할 파이썬 버전을 선택하세요. : ")
    py = "python"
    if version == "1":
        opt = input("\n1. python\n2. python3\n3. 직접 입력\n환경변수에 등록된 python3의 호출 키워드를 선택하세요. : ")
        py += ("3" if opt == "2" else "" if opt == "1" else input("버전을 입력하세요(python3.?) : ").replace("python", ""))
        if "python3.8" in py:
            raise Exception("Do not use python3.8 with build option 1.")
    elif version == "2":
        py += "3.8"
        print("\n\nWindows 7 호환성을 위해 Pyside버전을 2버전으로 변경합니다. 스크립트가 정상 종료되지 못한 경우 수동으로 src/main/qt_core.py 파일을 원래대로 되돌려주세요.\n\n")
        os.rename("src/main/qt_core.py", "src/main/qt_core.py.bak")
        with open("src/main/qt_core.py.bak", "rt", encoding='utf-8') as ori, \
                open("src/main/qt_core.py", "wt", encoding='utf-8') as new:
            for line in ori.readlines():
                if "SUPPORT_WINDOWS_7" in line:
                    print(line)
                    line = line.replace("False", "True")
                    print(">> " + line, end="\n\n\n")
                new.write(line)
    print("선택된 파이썬 버전 : ", end='', flush=True)
    if 1 == os.system(f"{py} --version"):
        raise Exception(f"파이썬 버전({py})을 찾을 수 없습니다.")

    os.system(f"{py} -m pip install wheel")
    os.system(f"{py} -m pip install --upgrade pip")
    os.system(f"{py} -m pip install tinyaes " + ("PySide2" if version == "2" else "PySide6"))
    if tool == "cx_Freeze":
        print("cx_Freeze 설치")
        os.system(f"{py} -m pip install cx_Freeze pywin32")

        opt = input("\n1. 빌드만\n2. MSI 만들기(실제 배포시에는 다른 패키징 방식을 사용하세요!)\n작업을 선택하세요. : ")
        os.system(f"{py} ./setup.py " + ("bdist_msi " if opt == "2" else "build " + py))
    else:
        if input("PyInstaller의 버전을 변경할까요? (y to yes) : ") == "y":
            os.system(f"{py} -m pip uninstall PyInstaller")
            if input("PyInstaller의 dev 버전을 사용해서 빌드할까요? (y to Yes) : ") == "y":
                os.system(f"{py} -m pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip")
            else:
                os.system(f"{py} -m pip install pyinstaller")
        else:
            os.system(f"{py} -m pip install pyinstaller")
        # 새로운 build.spec 생성하려면 주석 처리된 것을 이용하세요.
        # os.system(f"{py} -m PyInstaller -n newName --icon=icon.ico --hidden-import PySide6.QtSvg src/main/main.py --clean")
        os.system(f"{py} -m PyInstaller build.spec --noconfirm")

    if version == "2":
        os.remove("src/main/qt_core.py")
        os.rename("src/main/qt_core.py.bak", "src/main/qt_core.py")
        print("\nqt_core.py 파일을 원래대로 되돌렸습니다.")

    input("\n작업이 종료되었습니다. 오류 로그가 있는지 확인하세요. 아무 키나 눌러서 종료합니다. ")
