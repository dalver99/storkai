"""
###############################################
# dart_setup.py
#
# Purpose:
#   Validates DART API key by calling OpenDART and persists to .env.
###############################################
"""

import os
import sys
import requests


def _test_dart_api_key(api_key: str) -> bool:
    url = "https://opendart.fss.or.kr/api/list.json"
    params = {
        "crtfc_key": api_key,
        "page_no": "1",
        "page_count": "1",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return True
    return False


def configure_dart(language_choice: str) -> None:
    dart_api_key = input("Enter your API key for DART: ")
    if dart_api_key == "" or len(dart_api_key) < 30:
        print(
            "❌ Invalid DART API key format."
            if language_choice == "1"
            else "❌ DART 키 형식이 올바르지 않습니다."
        )
        sys.exit(1)

    try:
        if _test_dart_api_key(dart_api_key):
            print(
                "DART API key test valid!"
                if language_choice == "1"
                else "DART 키 테스트가 성공했습니다!"
            )
        else:
            print(
                "❌ DART API key test failed."
                if language_choice == "1"
                else "❌ DART 키 테스트가 실패했습니다."
            )
            sys.exit(1)
    except Exception as e:
        print(
            ("❌ Error: " + str(e)) if language_choice == "1" else ("❌ 오류: " + str(e))
        )
        sys.exit(1)

    lines: list[str] = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()

    # Remove any existing DART_API_KEY lines
    lines = [line for line in lines if not line.startswith("DART_API_KEY=")]
    # Add new values
    lines.append(f"DART_API_KEY={dart_api_key}\n")
    with open(".env", "w") as f:
        f.writelines(lines)

    if language_choice == "1":
        print(f"DART API key saved to .env: {dart_api_key[:5]}...")
    else:
        print(f"DART 키가 .env에 저장되었습니다: {dart_api_key[:5]}...")


