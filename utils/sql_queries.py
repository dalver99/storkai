favorites_query = """
    SELECT favorite_stocks.stock_code, company_info.corp_name
    FROM favorite_stocks
    LEFT JOIN company_info ON favorite_stocks.stock_code = company_info.stock_code
"""

