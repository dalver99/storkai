# Now merge the two logic to spit out a JSON file with the stock code and the company name.
def get_stock_code_and_company_name(language_choice: str):
    import requests
    import zipfile
    from io import BytesIO
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv
    import os

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
                return stock_code_and_company_name, None
    except ET.ParseError as e:
        return None, f"XML 파싱 오류: {str(e)}"
