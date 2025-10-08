###############################################
# install.py
#
# Purpose:
#   Orchestrates the installation flow by delegating to modules under
#   install/ for language selection, prior choices, OpenAI, DART, and DB.
###############################################

import sys
from install._1greetingsnlanguage import choose_language, greet
from install._2previous_choices import maybe_use_previous_choices
from install._3openai_setup import configure_openai
from install._4dart_setup import configure_dart
from install._5db_setup import configure_database, create_table


# Choose language and greet
language_choice = choose_language()
greet(language_choice)

# Offer to reuse previous choices from .env
used_previous, _values = maybe_use_previous_choices()

if used_previous:
    pass
else:
    configure_openai()
    configure_dart()
    configure_database()
    create_table()

print("Install is complete!" if language_choice == "1" else "설치가 완료되었습니다.")
print(
    "Please run the command 'python main.py' to start the program."
    if language_choice == "1"
    else "프로그램을 시작하려면 'python main.py' 명령어를 실행해주세요."
)
