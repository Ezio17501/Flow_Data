import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_lightweight_charts import renderLightweightCharts

# Streamlit app setup
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
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
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    },
    "watermark": {
        "visible": True,
        "fontSize": 24,
        "horzAlign": 'center',
        "vertAlign": 'center',
        "color": 'rgba(171, 71, 188, 0.4)',
        "text": f"FSL.NS {start_date}"
    }
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
