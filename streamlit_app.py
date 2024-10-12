# import streamlit as st
# import yfinance as yf
# import pandas as pd
# from datetime import datetime
# from streamlit_lightweight_charts import renderLightweightCharts

# # Streamlit app setup
# st.set_page_config(
#     page_title='Real-Time Data Science Dashboard',
#     page_icon='✅',
#     layout='wide'
# )

# # Fetch FSL.NS data for 11th Oct with 5-minute interval
# symbol = 'FSL.NS'
# start_date = '2024-10-11'
# end_date = '2024-10-12'
# interval = '5m'

# data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

# # Prepare data for the candlestick chart
# candlestick_data = []
# for index, row in data.iterrows():
#     # Converting timestamp to Unix format
#     timestamp = int(index.timestamp())
#     candlestick_data.append({
#         "open": row['Open'],
#         "high": row['High'],
#         "low": row['Low'],
#         "close": row['Close'],
#         "time": timestamp
#     })

# # Optionally, show it in Streamlit
# st.write(candlestick_data)  # To check the data in Streamlit's interface

# # Define chart options
# chartOptions = {
#             "width": 800,  # Enlarged chart width
#             "height": 600,  # Enlarged chart height
#             "layout": {
#                 "background": {"type": "solid", "color": "white"},
#                 "textColor": "black",
#             },
#             "grid": {
#                 "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
#                 "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
#             },
#             "crosshair": {"mode": 0},
#             "priceScale": {"borderColor": "rgba(197, 203, 206, 0.8)"},
#             "timeScale": {
#                 "borderColor": "rgba(197, 203, 206, 0.8)",
#                 "barSpacing": 10,
#                 "minBarSpacing": 8,
#                 "timeVisible": True,
#                 "secondsVisible": False,
#             },
           
#         }


# # Define candlestick series options
# seriesCandlestickChart = [{
#     "type": 'Candlestick',
#     "data": candlestick_data,
#     "options": {
#         "upColor": '#26a69a',
#         "downColor": '#ef5350',
#         "borderVisible": False,
#         "wickUpColor": '#26a69a',
#         "wickDownColor": '#ef5350'
#     }
# }]

# # Render chart
# st.subheader(f"Candlestick Chart for {symbol} on {start_date}")
# renderLightweightCharts([
#     {
#         "chart": chartOptions,
#         "series": seriesCandlestickChart
#     }
# ], 'candlestick')

import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# Streamlit app setup
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

# Initial setup for live feed
symbol = 'FSL.NS'
interval = '5m'

# Setting start date to current day and time for live feed
start_date = datetime.now().strftime('%Y-%m-%d')
end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Container for real-time chart
placeholder = st.empty()

# Function to fetch and prepare data
def fetch_candlestick_data():
    # Fetch stock data for the current day
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
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
    return candlestick_data

# Initial chart options
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

# Function to render the chart
def render_candlestick_chart(candlestick_data):
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
    
    with placeholder.container():
        st.subheader(f"Candlestick Chart for {symbol} on {start_date}")
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": seriesCandlestickChart
            }
        ], 'candlestick')

# Live feed simulation
candlestick_data = fetch_candlestick_data()
render_candlestick_chart(candlestick_data)

# Real-time update loop (fetch new data every 5 minutes)
while True:
    # Fetch the latest 5-minute interval data
    new_data = fetch_candlestick_data()
    
    # Only append new data if it's different
    if new_data[-1]['time'] != candlestick_data[-1]['time']:
        candlestick_data.append(new_data[-1])
    
    # Re-render the chart with updated data
    render_candlestick_chart(candlestick_data)
    
    # Wait for 5 minutes before fetching new data
    time.sleep(300)  # 300 seconds = 5 minutes
