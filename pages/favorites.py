import os
import streamlit as st
from utils.ui import hide_sidebar
from utils.check import check_essential_env_vars
from utils.sqlite import query_db_and_close
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox


def favorites():
    load_dotenv()
    language_choice = os.getenv("LANGUAGE_CHOICE")
    hide_sidebar()
    st.title("Favorites")
    
    # Show list of favorites, add or remove
    if check_essential_env_vars():
        #Show the current favorites in a checklist
        #query database for favorites
        favorites = query_db_and_close("SELECT * FROM favorite_stocks")

        if len(favorites) == 0:
            st.write("No favorites found" if language_choice == "1" else "관심 종목이 없습니다.")
        else:
            for favorite in favorites:
                st.write(favorite[0])

        #Users can un-check, or..

        #fetch company info from database
        company_info = query_db_and_close("SELECT * FROM company_info")

        #trim data for search bar, only corp_name and stock_code is needed.
        company_info = [{"corp_name": row[1], "stock_code": row[3]} for row in company_info]

        #Add favorites by searching - selecting stocks.
        #Show a search bar with a button to add to favorites
        # Define a search function that filters company_info by user input
        def search_stocks(query: str):
            results = [
                company
                for company in company_info
                if query.lower() in company["corp_name"].lower()
                or query.lower() in company["stock_code"].lower()
            ]
            # Give results as nicely formatted label/value choices for the searchbox.
            formatted_results = [
                f"{company['corp_name']} ({company['stock_code']})"
                for company in results[:10]
            ]
            return formatted_results

        selected_stock = st_searchbox(
            search_stocks,
            placeholder="Search for a stock" if language_choice == "1" else "관심 종목 검색",
            key="favorite_search_bar",
        )

        if selected_stock:
            #Activate a button to add to favorites, preferabbly addable by hitting enter
            if st.button("Add to favorites" if language_choice == "1" else "관심 종목에 추가", key="add_to_favorites_button"):
                query_db_and_close(f"INSERT INTO favorite_stocks (corp_code) VALUES ('{selected_stock}')")
                st.success("Stock added to favorites" if language_choice == "1" else "종목이 관심 종목에 추가되었습니다.")
            st.rerun() 
        else:
            st.error("No stock selected" if language_choice == "1" else "종목을 선택하지 않았습니다.")

        #Stock retriev
    else:
        st.write("Essential env vars are not set. Please Check settings page. 환경 변수가 설정되지 않았습니다. 설정 페이지를 확인해주세요.")


favorites()
