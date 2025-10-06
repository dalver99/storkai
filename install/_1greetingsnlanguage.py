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
        "Enter the number of the language\n / 사용하실 언어의 숫자를 입력해주세요: "
    )
    if language_choice == "1" or language_choice == "English":
        print("You have chosen English..")
        return "1"
    if language_choice == "2" or language_choice == "Korean":
        print("한국어를 선택하셨습니다..")
        return "2"

    print("Please try again.\n다시 시도해주세요.\n")


def greet(language_choice: str) -> None:
    print(
        r"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

             /|      ███████╗████████╗ ██████╗ ██████╗ ██╗  ██╗    |                     /         
            / |      ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██║ ██╔╝    |                  /\/          
        __/   |____  ███████╗   ██║   ██║   ██║██████╔╝█████╔╝     |     /\    /\    /         
       /'   ___   /  ╚════██║   ██║   ██║   ██║██╔══██╗██╔═██╗     |    /  \  /  \  /               
         / /    \/   ███████║   ██║   ╚██████╔╝██║  ██║██║  ██╗    |   /    \/    \/              
         |/          ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    |__/____________________
                 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 """
    )

    print(
        "- Welcome to STORK(STOck Research Kit)!"
        if language_choice == "1"
        else "STORK(STOck Research Kit)에 오신 것을 환영합니다!"
    )
