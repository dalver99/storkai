"""
###############################################
# previous_choices.py
#
# Purpose:
#   Reads an existing .env and optionally uses prior choices.
###############################################
"""

import os
import sys
from typing import Dict, Tuple


REQUIRED_KEYS = [
    "DART_API_KEY",
    "OPENAI_API_KEY",
    "AI_CHOICE",
    "DATABASE_TYPE",
]


def _parse_env(lines: list[str]) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for line in lines:
        if "=" in line:
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    return values


def maybe_use_previous_choices(language_choice: str) -> Tuple[bool, Dict[str, str]]:
    if not os.path.exists(".env"):
        return False, {}

    if language_choice == "1":
        print(".. Previous choices found!")
        prompt = "Do you want to use the previous choices? WARNING: Choosing no will reset existing SQLite database! (y/n): "
    else:
        print(".. 이전 환경 세팅이 있습니다!")
        prompt = "이전 환경 세팅을 사용하시겠습니까? 경고: 아니오를 선택하면 기존 SQLite 데이터베이스가 초기화됩니다! (y/n): "

    use_previous = input(prompt).strip().lower()
    if use_previous != "y":
        return False, {}

    with open(".env", "r") as f:
        lines = f.readlines()

    values = _parse_env(lines)
    if all(key in values and values[key] for key in REQUIRED_KEYS):
        if language_choice == "1":
            print("Using previous choices. Install is complete!")
        else:
            print("이전 환경 세팅을 사용합니다. 설치가 완료되었습니다!")
        return True, values

    if language_choice == "1":
        print("Something went wrong. Please re-clone and start again.")
    else:
        print("문제가 발생했습니다. 다시 클론하고 시작하세요.")
    sys.exit(1)
