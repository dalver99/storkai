import os
import streamlit as st
from utils.ui import hide_sidebar
from utils.check import check_essential_env_vars
from utils.sqlite import query_db_and_close
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox


# Define a search function that filters company_info by user input
def search_stocks(query: str):
    company_info = query_db_and_close("SELECT * FROM company_info")

    #trim data for search bar, only corp_name and stock_code is needed.
    company_info = [{"corp_name": row[1], "stock_code": row[3]} for row in company_info]

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
            # Display favorites with individual checkboxes, keep checkbox state with session_state
            st.write("### Select favorites to delete." if language_choice == "1" else "### 삭제할 관심 종목을 선택하세요.")
            
            if "checked_favorites" not in st.session_state:
                st.session_state.checked_favorites = set() 
                 # Use set for efficient lookup. O1 is good!

            #what you gonna do?
            checked_favorites = set(st.session_state.checked_favorites)

            for favorite in favorites:
                corp_code = favorite[0]
                corp_name = favorite[1] if len(favorite) > 1 else ""
                #Due to loading time..
                stock_code = favorite[3] if len(favorite) > 3 else ""
                label = f"{corp_name} ({stock_code})" if corp_name and stock_code else corp_code

                checked = corp_code in checked_favorites
                
                new_checked = st.checkbox(label, value=checked, key=f"favorite_checkbox_{corp_code}")
                if new_checked:
                    checked_favorites.add(corp_code)
                else:
                    checked_favorites.discard(corp_code)

            st.session_state.checked_favorites = checked_favorites
            delete_disabled = len(checked_favorites) == 0

            if st.button(
                "Delete Selected" if language_choice == "1" else "선택 삭제",
                disabled=delete_disabled,
                key="delete_favorites_button"
            ) and not delete_disabled:
                for corp_code in list(checked_favorites):
                    query_db_and_close(f"DELETE FROM favorite_stocks WHERE corp_code = '{corp_code}'")
                st.session_state.checked_favorites = set()
                st.success("Selected favorites deleted." if language_choice == "1" else "선택한 관심 종목이 삭제되었습니다.")
                st.rerun()


        #Add favorites by searching - selecting stocks.

        #Show a search bar with a button to add to favorites
        st.write("---")
        st.write("### Add favorites by searching - selecting stocks." if language_choice == "1" else "### 관심 종목을 검색하여 추가할 수 있습니다.")

        selected_stock = st_searchbox(
            search_stocks,
            placeholder="Search for a stock (ex: 삼성전자)" if language_choice == "1" else "관심 종목 검색 (ex: 삼성전자)",
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

        
        from utils.ui import home_button
        home_button(language_choice)

    else:
        st.write("Essential env vars are not set. Please Check settings page. 환경 변수가 설정되지 않았습니다. 설정 페이지를 확인해주세요.")


favorites()
