import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_lightweight_charts import renderLightweightCharts
import time
from datetime import datetime, timedelta

# Streamlit app setup
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    layout='wide'
)

# Fetch FSL.NS data for 11th Oct with 5-minute interval
symbol = 'FSL.NS'
start_date = '2024-10-11'
end_date = '2024-10-12'
interval = '5m'

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
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')

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

