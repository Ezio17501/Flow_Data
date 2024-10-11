import streamlit as st
import yfinance as yf
from streamlit_lightweight_charts import renderLightweightCharts
from datetime import datetime, timedelta
import time

# Set page layout and title
st.set_page_config(
    page_title='Simulated Real-Time Stock Candlestick Chart',
    page_icon='📈',
    layout='wide'
)

# Dashboard title
st.title("Simulated Real-Time Candlestick Chart for FSL.NS on 10th October 2024")

# Define stock symbol and interval
stock_symbol = "FSL.NS"
interval = '5m'  # 5-minute interval

# Define the start and end times for the simulation (9:15 AM to 3:30 PM)
market_open = datetime(2024, 10, 10, 9, 15)
market_close = datetime(2024, 10, 10, 15, 30)

# Fetch stock data for the day from Yahoo Finance
stock_data = yf.download(tickers=stock_symbol, interval=interval, start="2024-10-10", end="2024-10-11")

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

# Print the candlestick data for verification
st.write("Candlestick Data:", candlestick_data)

# Initialize chart options
chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

# Create a placeholder to display the chart
placeholder = st.empty()

# Simulate candle progression
for i in range(len(candlestick_data)):
    # Get only the candles up to the current iteration
    current_candlestick_data = candlestick_data[:i+1]
    
    # Define the candlestick chart series with only the available candles
    seriesCandlestickChart = [{
        "type": 'Candlestick',
        "data": current_candlestick_data,
        "options": {
            "upColor": '#26a69a',
            "downColor": '#ef5350',
            "borderVisible": False,
            "wickUpColor": '#26a69a',
            "wickDownColor": '#ef5350'
        }
    }]
    
    # Display the updated chart
    with placeholder.container():
        st.subheader(f"Real-Time Candlestick Chart for {stock_symbol} (Candle {i+1})")
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": seriesCandlestickChart
            }
        ], 'candlestick')

        # Display the detailed stock data in a table
        st.markdown(f"### Stock Data (up to Candle {i+1})")
        st.dataframe(stock_data.iloc[:i+1])

    # Simulate real-time by waiting 5 minutes (for testing purposes, we can reduce it to a few seconds)
    time.sleep(5)  # Change to 300 for actual 5-minute intervals
