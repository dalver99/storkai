import os
import streamlit as st
from utils.ui import hide_sidebar, home_button
from dotenv import load_dotenv
from utils.sqlite import query_db_and_close
from utils.sql_queries import favorites_query
import datetime

# import yfinance
import plotly.graph_objects as go
import pandas as pd
import FinanceDataReader as fdr

load_dotenv()
language_choice = os.getenv("LANGUAGE_CHOICE")

def fetch_fdr_data(stock_code: str, start_date: datetime.date, end_date: datetime.date):
    # check if stock_code is a valid stock code
    if not stock_code.isdigit() or len(stock_code) != 6:
        st.error("Invalid stock code" if language_choice == "1" else "유효하지 않은 종목 코드")
        return None
    if stock_code.isdigit() and len(stock_code) == 6:
        fdr_code = f"KRX: {stock_code}"
    return fdr.DataReader(fdr_code, start=start_date, end=end_date)

def show_chart(stock_code: str, data: pd.DataFrame):
    # chart with plotly
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

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"],
                    increasing_line_color="red",
                    decreasing_line_color="blue",
                )
            ]
        )
        fig.update_layout(
            title=f"Price Chart ({stock_code})",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            height=500,
            yaxis=dict(
                tickformat="~s",  # Use SI prefix or plain numeric, no exponent, and avoids 0,1,2,3
                showgrid=True,
                fixedrange=False,
            ),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No price data available for this stock." if language_choice == "1" else "이 종목의 가격 데이터를 찾을 수 없습니다.")


def analyze_stock():
    load_dotenv()
    language_choice = os.getenv("LANGUAGE_CHOICE")
    hide_sidebar()
    st.title("Analyze Stock" if language_choice == "1" else "주식 분석")

    # Show list of favorites stock as a button, which will switch the UI content
    #Get data
    favorites = query_db_and_close(favorites_query)

    for favorite in favorites:
        if st.button(
            f"{favorite[1]} ({favorite[0]})", key=f"favorite_button_{favorite[0]}"
        ):
            # save it as a state
            st.session_state.selected_stock = favorite[0]

    # Now selected, show some UIs.. first lets show a chart
    if "selected_stock" in st.session_state:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=90)

        data = fetch_fdr_data(st.session_state.selected_stock, start_date, end_date)
        #wait till data arrives
        show_chart(st.session_state.selected_stock, data)

        # Then do basic analysis on data
        # First, calculate average price change ratio of the stock for close prices, in absolute value, percentages, 
        average_price_change_ratio = abs(data["Close"].pct_change().mean()) * 100
        st.write(f"Average price change ratio: {average_price_change_ratio}")

        # show dates where it had more than double the price change ratio
        double_price_change_dates = data[data["Close"].pct_change() > 0.02].index
        st.write(f"Dates: {double_price_change_dates}")

analyze_stock()
