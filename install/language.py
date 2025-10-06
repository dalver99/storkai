"""
###############################################
# language.py
#
# Purpose:
#   Handles language selection and greeting UX for the installer.
###############################################
"""

import sys


def choose_language() -> str:
    print("1. English / 영어")
    print("2. Korean / 한국어")
    language_choice = input(
        "Enter the number of the language you want to use / 사용하실 언어의 숫자를 입력해주세요: "
    )
    if language_choice == "1" or language_choice == "English":
        print("You have chosen English")
        return "1"
    if language_choice == "2" or language_choice == "Korean":
        print("한국어를 선택하셨습니다.")
        return "2"

    print("Invalid choice")
    sys.exit(1)


def greet(language_choice: str) -> None:
    print(r"""
  ███████╗████████╗ ██████╗ ██████╗ ██╗  ██╗   |                        /\          
 ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██║ ██╔╝    |                     /\/  \        
 ███████╗   ██║   ██║   ██║██████╔╝█████╔╝     |        /\    /\    /      \   
 ╚════██║   ██║   ██║   ██║██╔══██╗██╔═██╗     |       /  \  /  \  /               
 ███████║   ██║   ╚██████╔╝██║  ██║██║  ██╗    |      /    \/    \/              
 ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    |    _/                        
                                               |___/__________________________
 """)

    if language_choice == "1":
        print("Welcome to STORK(Stock Recommendation Kit)!")
    else:
        print("STORK(Stock Recommendation Kit)에 오신 것을 환영합니다!")


