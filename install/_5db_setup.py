"""
###############################################
# db_setup.py
#
# Purpose:
#   Configures SQLite (or other DBs when available) and persists to .env.
###############################################
"""

import os
import sys


def configure_database(language_choice: str) -> None:
    print("--------------------------------")
    print(
        "Choose which database to use: "
        if language_choice == "1"
        else "사용하실 데이터베이스를 선택해주세요: "
    )
    print("1. PostgreSQL(Developing)")
    print("2. SQLite")

    database_choice = input(
        "Enter the number of the database you want to use: "
        if language_choice == "1"
        else "사용하실 데이터베이스의 숫자를 입력해주세요: "
    )

    if database_choice in ("1", "PostgreSQL"):
        print(
            "PostgreSQL is currently under development. Please wait for the update."
            if language_choice == "1"
            else "PostgreSQL는 현재 개발 중입니다. 업데이트 될 때까지 기다려주세요."
        )

        sys.exit(0)

    if database_choice not in ("2", "SQLite"):
        print(
            "Invalid choice" if language_choice == "1" else "올바르지 않은 선택입니다."
        )
        sys.exit(1)

    # SQLite path/name
    if language_choice == "1":
        print("You have chosen SQLite")
        print("Initializing SQLite database...")
    else:
        print("SQLite를 선택하셨습니다.")
        print("SQLite 데이터베이스를 초기화합니다...")

    # Default name to stork.db, but user can change it if user wants
    print(
        "Use Default Name? (y/n): "
        if language_choice == "1"
        else "기본 이름을 사용하시겠습니까? (y/n): "
    )
    use_default_name = input().strip().lower()
    if use_default_name == "y":
        database_name = "stork.db"
    else:
        database_name = input("Enter the name of the database you want to use: ")
        if database_name == "":
            print("Invalid name. Using default name.")
            database_name = "stork.db"

    lines: list[str] = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()

    # Remove any existing DATABASE_NAME or DATABASE_TYPE lines
    lines = [
        line
        for line in lines
        if not (line.startswith("DATABASE_NAME=") or line.startswith("DATABASE_TYPE="))
    ]
    # Add new values
    lines.append(f"DATABASE_NAME={database_name}\n")
    lines.append("DATABASE_TYPE=sqlite\n")
    with open(".env", "w") as f:
        f.writelines(lines)

    if language_choice == "1":
        print("SQLite database information saved to .env")
    else:
        print("SQLite 데이터베이스 정보가 .env에 저장되었습니다.")

    # Create the database and table as before
    if language_choice == "1":
        print(f"SQLite database created: {database_name}")
    else:
        print(f"SQLite 데이터베이스가 생성되었습니다: {database_name}")


def create_table(language_choice: str) -> None:
    print(
        "Creating SQLite table..."
        if language_choice == "1"
        else "SQLite 테이블을 생성합니다..."
    )
    # Check Database Type from .env
    with open(".env", "r") as f:
        lines = f.readlines()
    database_type = (
        [line for line in lines if line.startswith("DATABASE_TYPE=")][0]
        .split("=")[1]
        .strip()
    )
    if database_type == "sqlite":
        print(
            "Creating SQLite table..."
            if language_choice == "1"
            else "SQLite 테이블을 생성합니다..."
        )
    else:
        print(
            "Database type is not SQLite. Skipping table creation."
            if language_choice == "1"
            else "데이터베이스 타입이 SQLite가 아닙니다. 테이블 생성을 건너뜁니다."
        )
        sys.exit(0)
    database_name = (
        [line for line in lines if line.startswith("DATABASE_NAME=")][0]
        .split("=")[1]
        .strip()
    )
    # Create table with sqlite3
    os.system(f"sqlite3 {database_name} < create_table.sql")
