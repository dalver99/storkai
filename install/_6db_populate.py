# Now merge the two logic to spit out a JSON
def fill_db_with_stock_code_and_company_name():
    # fetch language choice and database name from .env
    with open(".env", "r") as f:
        lines = f.readlines()
    language_choice = (
        [line for line in lines if line.startswith("LANGUAGE_CHOICE=")][0]
        .split("=")[1]
        .strip()
    )
    database_name = (
        [line for line in lines if line.startswith("DATABASE_NAME=")][0]
        .split("=")[1]
        .strip()
    )
    print("--------------------------------")
    import requests
    import zipfile
    from io import BytesIO
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv
    import os
    import sqlite3

    # fetch language choice from .env
    load_dotenv()
    API_KEY = os.getenv("DART_API_KEY")
    BASE_URL = "https://opendart.fss.or.kr/api"
    url = f"{BASE_URL}/corpCode.xml?crtfc_key={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(
                f"API 요청 실패: HTTP 상태 코드 {response.status_code}"
                if language_choice == "1"
                else f"API 요청 실패: HTTP 상태 코드 {response.status_code}"
            )
            return None, f"API 요청 실패: HTTP 상태 코드 {response.status_code}"

        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            with zip_file.open("CORPCODE.xml") as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                # Extract all details for each company in the XML
                stock_code_and_company_name = []
                for company in root.findall(".//list"):
                    company_data = {}
                    for child in company:
                        company_data[child.tag] = child.text
                    if (
                        company_data["stock_code"] is not None
                        and company_data["stock_code"].strip() != ""
                    ):
                        stock_code_and_company_name.append(company_data)
    except ET.ParseError as e:
        return None, f"XML 파싱 오류: {str(e)}"

    # Upload to DB
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company_info")
    rows = cursor.fetchall()

    if len(rows) != 0:
        print(
            "Database is not empty. Stopping data population."
            if language_choice == "1"
            else "데이터베이스가 비어있지 않습니다. 데이터 삽입을 건너뜁니다."
        )
        return
    else:
        print(
            "Database is empty. Populating data..."
            if language_choice == "1"
            else "데이터베이스가 비어있습니다. 데이터를 삽입합니다..."
        )
        for row in stock_code_and_company_name:
            cursor.execute(
                "INSERT INTO company_info (corp_code, corp_name, corp_eng_name, stock_code, modify_date) VALUES (?, ?, ?, ?, ?)",
                (
                    row["corp_code"],
                    row["corp_name"],
                    row["corp_eng_name"],
                    row["stock_code"],
                    row["modify_date"],
                ),
            )
        conn.commit()
        conn.close()
        print(
            f"Number of rows inserted: {len(stock_code_and_company_name)}"
            if language_choice == "1"
            else f"삽입된 행의 수: {len(stock_code_and_company_name)}"
        )
        print(
            "Data populated successfully."
            if language_choice == "1"
            else "데이터가 성공적으로 삽입되었습니다."
        )
