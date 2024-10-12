import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
from streamlit_lightweight_charts import renderLightweightCharts
import time
import pytz  # Import pytz for timezone handling

# Streamlit app setup
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    layout='wide'
)

# Function to refresh during market hours with timezone
def refresh_during_market_hours(refresh_interval=10):
    """Refresh the app every `refresh_interval` seconds during market hours (9:15 AM to 3:30 PM IST)."""
    
    # Define the Indian Standard Time (IST) timezone
    ist = pytz.timezone('Asia/Kolkata')

    # Define market open and close times in IST (ensure all are timezone-aware)
    market_open = ist.localize(datetime.now().replace(hour=9, minute=15, second=0, microsecond=0))
    market_close = ist.localize(datetime.now().replace(hour=15, minute=30, second=0, microsecond=0))

    # Get the current time in IST (also timezone-aware)
    now = datetime.now(ist)

    # Check if the current time is within market hours
    if market_open <= now <= market_close:
        st.write(f"Market is open! Refreshing data every {refresh_interval} seconds (IST).")
        
        # Store the last time the page was refreshed in Streamlit's session state
        if "last_refresh" not in st.session_state:
            st.session_state.last_refresh = now

        # Check if the refresh interval has passed
        if now - st.session_state.last_refresh > timedelta(seconds=refresh_interval):
            # Update the last refresh time
            st.session_state.last_refresh = now
            # Rerun the app to refresh the data
            st.rerun()
    else:
        st.write("Market is closed. No updates will be made.")

# Fetch and display candlestick chart data
def display_candlestick_chart():
    # Stock symbol and data settings
    symbol = 'FSL.NS'
    start_date = '2024-10-11'
    end_date = '2024-10-12'
    interval = '5m'

    # Fetch stock data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    # Prepare data for the candlestick chart
    candlestick_data = []
    for index, row in data.iterrows():
        # Converting timestamp to Unix format
        timestamp = int(index.timestamp())
        candlestick_data.append({
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close'],
            "time": timestamp
        })

    # Optionally, show it in Streamlit
    st.write(candlestick_data)  # To check the data in Streamlit's interface

    # Define chart options
    chartOptions = {
        "width": 800,  # Enlarged chart width
        "height": 600,  # Enlarged chart height
        "layout": {
            "background": {"type": "solid", "color": "white"},
            "textColor": "black",
        },
        "grid": {
            "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
            "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
        },
        "crosshair": {"mode": 0},
        "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10,
            "minBarSpacing": 8,
            "timeVisible": True,
            "secondsVisible": False,
        },
    }

    # Define candlestick series options
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

    # Render chart
    st.subheader(f"Candlestick Chart for {symbol} on {start_date}")
    renderLightweightCharts([{
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }], 'candlestick')

# Refresh during market hours
refresh_during_market_hours(refresh_interval=10)

# Display candlestick chart
display_candlestick_chart()

# Sleep to simulate waiting for the next refresh
time.sleep(1)


# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import time
# from datetime import datetime
# from streamlit_lightweight_charts import renderLightweightCharts

# # Streamlit app setup
# st.set_page_config(
#     page_title='Real-Time Data Science Dashboard',
#     page_icon='✅',
#     layout='wide'
# )

# # Simulating live feed for stock data on a specific date
# symbol = 'FSL.NS'
# start_date = '2024-10-11'
# end_date = '2024-10-12'
# interval = '5m'

# # Fetch historical data for 11th Oct 2024
# data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

# # Prepare initial candlestick data for the first 5-minute interval
# candlestick_data = []

# def prepare_data(data, start_idx, end_idx):
#     # Prepare the candlestick data for the range from start_idx to end_idx
#     for index, row in data.iloc[start_idx:end_idx].iterrows():
#         # Convert timestamp to Unix format
#         timestamp = int(index.timestamp())
#         candlestick_data.append({
#             "open": row['Open'],
#             "high": row['High'],
#             "low": row['Low'],
#             "close": row['Close'],
#             "time": timestamp
#         })

# # Define chart options
# chartOptions = {
#     "width": 800,  # Enlarged chart width
#     "height": 600,  # Enlarged chart height
#     "layout": {
#         "background": {"type": "solid", "color": "white"},
#         "textColor": "black",
#     },
#     "grid": {
#         "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
#         "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
#     },
#     "crosshair": {"mode": 0},
#     "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
#     "timeScale": {
#         "borderColor": "rgba(197, 203, 206, 0.8)",
#         "barSpacing": 10,
#         "minBarSpacing": 8,
#         "timeVisible": True,
#         "secondsVisible": False,
#     },
# }

# # Rendering function for the candlestick chart
# def render_candlestick_chart(i):
#     seriesCandlestickChart = [{
#         "type": 'Candlestick',
#         "data": candlestick_data,
#         "options": {
#             "upColor": '#26a69a',
#             "downColor": '#ef5350',
#             "borderVisible": False,
#             "wickUpColor": '#26a69a',
#             "wickDownColor": '#ef5350'
#         }
#     }]
    
#     # Use placeholder to update the chart with new data, using a unique key for each iteration
#     with placeholder.container():
#         st.subheader(f"Candlestick Chart for {symbol} on {start_date}")
#         renderLightweightCharts([
#             {
#                 "chart": chartOptions,
#                 "series": seriesCandlestickChart
#             }
#         ], key=f'candlestick_{i}')  # Assigning a unique key for each iteration

# # Container for the live chart
# placeholder = st.empty()

# # Simulation of live feed
# interval_seconds = 10  # 5 minutes in seconds
# total_intervals = len(data)

# # Simulate starting from the first 5-minute interval
# for i in range(total_intervals):
#     # Prepare data up to the current interval (i.e., from 0 to i+1)
#     prepare_data(data, i, i + 1)
    
#     # Render the chart with the updated data
#     render_candlestick_chart(i)
    
#     # Wait for 5 minutes before showing the next interval's data (simulating live feed)
#     if i < total_intervals - 1:  # Skip wait for the last interval
#         time.sleep(interval_seconds)

