import streamlit as st
import yfinance as yf
from streamlit_lightweight_charts import renderLightweightCharts
from datetime import datetime, timedelta
import time

# Set page layout and title
st.set_page_config(
    page_title='Real-Time Stock Market Dashboard',
    page_icon='📈',
    layout='wide'
)

# Dashboard title
st.title("Real-Time Stock Market Data Dashboard")

# Define stock symbol and interval
stock_symbol = "FSL.NS"
interval = '5m'  # 5-minute interval

# Number of refreshes
refresh_time_seconds = 30  # Set refresh interval (in seconds)

# Creating a single-element container for real-time updates
placeholder = st.empty()

# Real-time simulation loop
for _ in range(200):  # You can replace the range with while True for infinite updates
    # Define the date range for fetching the stock data
    start_date = '2024-10-10'
    end_date = datetime.now().strftime('%Y-%m-%d')  # Current date

    # Fetch stock data using Yahoo Finance
    stock_data = yf.download(tickers=stock_symbol, interval=interval, start=start_date, end=end_date)

    # Convert the data into the format required for the candlestick chart
    candlestick_data = [
        {
            "open": row['Open'], 
            "high": row['High'], 
            "low": row['Low'], 
            "close": row['Close'], 
            "time": int(row.name.timestamp())  # Convert the index (datetime) to Unix timestamp
        }
        for row in stock_data.itertuples()
    ]

    # Chart options
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    # Candlestick series data
    seriesCandlestickChart = [{
        "type": 'Candlestick',
        "data": candlestick_data,
        "options": {
            "upColor": '#26a69a',
            "downColor": '#ef5350',
            "borderVisible": False,
            "wickUpColor": '#26a69a',
            "wickDownColor": '#ef5350'
        }
    }]

    # Render the chart inside the placeholder container
    with placeholder.container():
        st.subheader(f"Candlestick Chart for {stock_symbol} on {start_date}")
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": seriesCandlestickChart
            }
        ], 'candlestick')

        # Display the detailed stock data
        st.markdown("### Stock Data View")
        st.dataframe(stock_data)

    # Wait before refreshing again
    time.sleep(refresh_time_seconds)
