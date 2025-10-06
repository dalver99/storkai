"""
###############################################
# openai_setup.py
#
# Purpose:
#   Validates and persists OpenAI configuration into .env.
###############################################
"""

import os
import sys
import openai


def configure_openai(language_choice: str) -> None:
    print("Choose which AI to use: " if language_choice == "1" else "사용하실 AI를 선택해주세요: ")
    print("1. OpenAI")
    ai_choice = input(
        "Enter the number of the AI you want to use: "
        if language_choice == "1"
        else "사용하실 AI의 숫자를 입력해주세요: "
    )

    if ai_choice not in ("1", "OpenAI"):
        print("Invalid choice" if language_choice == "1" else "올바르지 않은 선택입니다.")
        sys.exit(1)

    if language_choice == "1":
        print("You have chosen OpenAI")
    else:
        print("OpenAI를 선택하셨습니다.")

    openai_api_key = input("Enter your API key for OpenAI: ")
    if not openai_api_key.startswith("sk-") or openai_api_key == "":
        print("❌ Invalid OpenAI key format." if language_choice == "1" else "❌ OpenAI 키 형식이 올바르지 않습니다.")
        sys.exit(1)

    try:
        openai.api_key = openai_api_key
        openai.models.list()
        print("OpenAI API key is valid!" if language_choice == "1" else "OpenAI 키가 유효합니다!")
    except Exception:
        print("❌ Invalid OpenAI key." if language_choice == "1" else "❌ OpenAI 키가 유효하지 않습니다.")
        sys.exit(1)

    lines: list[str] = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()

    # Remove any existing OPENAI_API_KEY or AI_CHOICE lines
    lines = [
        line
        for line in lines
        if not (line.startswith("OPENAI_API_KEY=") or line.startswith("AI_CHOICE="))
    ]
    # Add new values
    lines.append(f"OPENAI_API_KEY={openai_api_key}\n")
    lines.append("AI_CHOICE=openai\n")

    with open(".env", "w") as f:
        f.writelines(lines)

    if language_choice == "1":
        print(f"OpenAI API key saved to .env: {openai_api_key[:5]}...")
    else:
        print(f"OpenAI 키가 .env에 저장되었습니다: {openai_api_key[:5]}...")


