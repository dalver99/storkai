import os
import streamlit as st
from utils.ui import hide_sidebar, home_button
from dotenv import load_dotenv
from utils.sqlite import query_db_and_close
import yfinance
import plotly.graph_objects as go
import pandas as pd

def show_chart(stock_code: str):
    #get data from yfinance
    import datetime
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=90)
    # For Korean stocks, yfinance expects ".KS" or ".KQ" extension.
    # If stock_code is just 6 digits, append ".KS" (main board); you may adjust for KOSDAQ as needed.
    yf_code = stock_code
    if stock_code.isdigit() and len(stock_code) == 6:
        yf_code = f"{stock_code}.KS"
    data = yfinance.download(yf_code, start=start_date, end=end_date + datetime.timedelta(days=1), auto_adjust=False)
    # print(data)

    #chart with plotly
    if data is not None and not data.empty:
        # Clean index: yfinance sometimes returns MultiIndex, ensure simple DatetimeIndex for proper plotting
        if isinstance(data.index, pd.MultiIndex):
            data = data.reset_index(level=0, drop=True)
        if not isinstance(data.index, (pd.DatetimeIndex, pd.Index)):
            data.index = pd.to_datetime(data.index)

        # Sometimes yfinance returns 2-level columns (if multiple tickers or columns). Fix for single ticker case.
        if isinstance(data.columns, pd.MultiIndex):
            # Try to get rid of ticker level if possible
            data.columns = data.columns.get_level_values(0)

        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='red',
            decreasing_line_color='blue'
        )])
        fig.update_layout(
            title=f"Price Chart ({stock_code})",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            height=500,
            yaxis=dict(
                tickformat="~s",  # Use SI prefix or plain numeric, no exponent, and avoids 0,1,2,3
                showgrid=True,
                fixedrange=False
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No price data available for this stock.")




def analyze_stock():
    load_dotenv()
    language_choice = os.getenv("LANGUAGE_CHOICE")
    hide_sidebar()
    st.title("Analyze Stock" if language_choice == "1" else "주식 분석")

    #Show list of favorites stock as a button, which will switch the UI content
    favorites = query_db_and_close("""
        SELECT favorite_stocks.stock_code, company_info.corp_name
        FROM favorite_stocks
        LEFT JOIN company_info ON favorite_stocks.stock_code = company_info.stock_code
    """)

    for favorite in favorites:
        if st.button(f"{favorite[1]} ({favorite[0]})", key=f"favorite_button_{favorite[0]}"):
            #save it as a state
            st.session_state.selected_stock = favorite[0]

    #Now selected, show some UIs.. first lets show a chart
    if "selected_stock" in st.session_state:
        show_chart(st.session_state.selected_stock)


analyze_stock()