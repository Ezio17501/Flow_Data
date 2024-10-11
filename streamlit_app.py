import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_lightweight_charts import renderLightweightCharts
import json

st.set_page_config(
    page_title = 'Real-Time Data Science Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# Main area inputs
stock_ticker = st.text_input("Enter Stock Ticker (e.g., FSL.NS)", "FSL.NS")
start_date = st.date_input("Start Date", datetime.strptime("2024-10-01", "%Y-%m-%d"))
end_date = st.date_input("End Date", datetime.today())



# Function to perform the calculation and generate the JSON data
def perform_calculation(ticker, start_date, end_date):
    # Download hourly data
    data = yf.download(ticker, start=start_date, end=end_date, interval="60m")

    data = data[data.index.hour < 15].copy()
    data["Stock"] = ticker
    data["Date"] = data.index.date
    data["Time"] = data.index.time
    data = data.drop(columns=["Adj Close", "Volume"])

    # Group by the date and calculate daily sums
    daily_sums = data.drop(columns=["Time", "Stock"]).groupby("Date").sum()
    daily_sums = daily_sums.rename(
        columns={
            "Open": "SumOpen",
            "High": "SumHigh",
            "Low": "SumLow",
            "Close": "SumClose",
        }
    )

    # Calculate HighDiv, LowDiv, and DiffOH-LC
    daily_sums["HighDiv"] = daily_sums["SumHigh"] / 6
    daily_sums["LowDiv"] = daily_sums["SumLow"] / 6
    daily_sums["DiffOH-LC"] = (daily_sums["SumOpen"] + daily_sums["SumHigh"]) - (
        daily_sums["SumLow"] + daily_sums["SumClose"]
    )

    # Calculate TS1, TS2, TS3, TR1, TR2, TR3
    daily_sums["TS1"] = daily_sums["HighDiv"] + (daily_sums["DiffOH-LC"] / 3)
    daily_sums["TS2"] = daily_sums["HighDiv"] + (daily_sums["DiffOH-LC"] / 6)
    daily_sums["TS3"] = daily_sums["HighDiv"] + (daily_sums["DiffOH-LC"] / 9)
    daily_sums["TR1"] = daily_sums["LowDiv"] - (daily_sums["DiffOH-LC"] / 3)
    daily_sums["TR2"] = daily_sums["LowDiv"] - (daily_sums["DiffOH-LC"] / 6)
    daily_sums["TR3"] = daily_sums["LowDiv"] - (daily_sums["DiffOH-LC"] / 9)

    # Merge daily sums with daily data
    daily_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    daily_data = daily_data.drop(columns=["Adj Close", "Volume"])
    daily_data["Date"] = daily_data.index.date

    # Add TS and TR values from daily_sums shifted by one day
    daily_data["TS1"] = np.nan
    daily_data["TS2"] = np.nan
    daily_data["TS3"] = np.nan
    daily_data["TR1"] = np.nan
    daily_data["TR2"] = np.nan
    daily_data["TR3"] = np.nan

    # Add the new row based on end_date with null values for OHLC but TS and TR values from the previous day
    end_row = {
        "Date": end_date,
        "Open": np.nan,
        "High": np.nan,
        "Low": np.nan,
        "Close": np.nan,
        "TS1": np.nan,
        "TS2": np.nan,
        "TS3": np.nan,
        "TR1": np.nan,
        "TR2": np.nan,
        "TR3": np.nan,
    }
    end_row_df = pd.DataFrame([end_row])
    daily_data = pd.concat([daily_data, end_row_df], ignore_index=True)

    daily_dates = daily_data["Date"].values
    
    for i in range(0, len(daily_sums)):
        date = daily_sums.index[i]
        dailyDateForShift = daily_dates[i + 1]
        ts_tr_values = daily_sums.loc[date, ["TS1", "TS2", "TS3", "TR1", "TR2", "TR3"]]
        daily_data.loc[
            daily_data["Date"] == dailyDateForShift,
            ["TS1", "TS2", "TS3", "TR1", "TR2", "TR3"],
        ] = ts_tr_values.values

    # Drop the Date column
    daily_data.set_index("Date", inplace=True)

    df_csv = daily_data.reset_index()
    
    # Create new columns for TS1-O, TS2-O, TS3-O, TS1-H, TS2-H, TS3-H (Open and High comparisons)
    df_csv["TS1-O"] = np.where(
        (np.floor(df_csv["TS1"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TS1"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    df_csv["TS2-O"] = np.where(
        (np.floor(df_csv["TS2"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TS2"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    df_csv["TS3-O"] = np.where(
        (np.floor(df_csv["TS3"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TS3"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    df_csv["TS1-H"] = np.where(
        (np.floor(df_csv["TS1"]) == np.floor(df_csv["High"])) |
        (abs((df_csv["TS1"] - df_csv["High"]) / df_csv["High"]) * 100 < 1),
        True,
        False
    )

    df_csv["TS2-H"] = np.where(
        (np.floor(df_csv["TS2"]) == np.floor(df_csv["High"])) |
        (abs((df_csv["TS2"] - df_csv["High"]) / df_csv["High"]) * 100 < 1),
        True,
        False
    )

    df_csv["TS3-H"] = np.where(
        (np.floor(df_csv["TS3"]) == np.floor(df_csv["High"])) |
        (abs((df_csv["TS3"] - df_csv["High"]) / df_csv["High"]) * 100 < 1),
        True,
        False
    )

    # Create new columns for TR1-O, TR2-O, TR3-O (Open comparisons)
    df_csv["TR1-O"] = np.where(
        (np.floor(df_csv["TR1"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TR1"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR2-O"] = np.where(
        (np.floor(df_csv["TR2"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TR2"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR3-O"] = np.where(
        (np.floor(df_csv["TR3"]) == np.floor(df_csv["Open"])) |
        (abs((df_csv["TR3"] - df_csv["Open"]) / df_csv["Open"]) * 100 < 1),
        True,
        False
    )

    # Create new columns for TS1-L, TS2-L, TS3-L, TS1-C, TS2-C, TS3-C (Low and Close comparisons)
    df_csv["TR1-L"] = np.where(
        (np.floor(df_csv["TR1"]) == np.floor(df_csv["Low"])) |
        (abs((df_csv["TR1"] - df_csv["Low"]) / df_csv["Low"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR2-L"] = np.where(
        (np.floor(df_csv["TR2"]) == np.floor(df_csv["Low"])) |
        (abs((df_csv["TR2"] - df_csv["Low"]) / df_csv["Low"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR3-L"] = np.where(
        (np.floor(df_csv["TR3"]) == np.floor(df_csv["Low"])) |
        (abs((df_csv["TR3"] - df_csv["Low"]) / df_csv["Low"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR1-C"] = np.where(
        (np.floor(df_csv["TR1"]) == np.floor(df_csv["Close"])) |
        (abs((df_csv["TR1"] - df_csv["Close"]) / df_csv["Close"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR2-C"] = np.where(
        (np.floor(df_csv["TR2"]) == np.floor(df_csv["Close"])) |
        (abs((df_csv["TR2"] - df_csv["Close"]) / df_csv["Close"]) * 100 < 1),
        True,
        False
    )

    df_csv["TR3-C"] = np.where(
        (np.floor(df_csv["TR3"]) == np.floor(df_csv["Close"])) |
        (abs((df_csv["TR3"] - df_csv["Close"]) / df_csv["Close"]) * 100 < 1),
        True,
        False
    )

    # Convert DataFrame to CSV format
    csv_data = df_csv.to_csv(index=False)
    # Display the DataFrame in the Streamlit app
    st.dataframe(df_csv)
    # Add download button for CSV data
    st.download_button(
        label="Download CSV Data",
        data=csv_data,
        file_name=f"{stock_ticker}_data.csv",
        mime="text/csv",
    )
    
    
    # Convert data to JSON format
    json_data = {
        "candlestick": [],
        "ts1": [],
        "ts2": [],
        "ts3": [],
        "tr1": [],
        "tr2": [],
        "tr3": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
    }

    for row in daily_data.itertuples():
        time_unix = int(datetime.combine(row.Index, datetime.min.time()).timestamp())
        json_data["candlestick"].append(
            {
                "time": time_unix,
                "open": row.Open if not np.isnan(row.Open) else None,
                "high": row.High if not np.isnan(row.High) else None,
                "low": row.Low if not np.isnan(row.Low) else None,
                "close": row.Close if not np.isnan(row.Close) else None,
            }
        )
        json_data["ts1"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TS1 if not np.isnan(row.TS1) else None,
            }
        )
        json_data["ts2"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TS2 if not np.isnan(row.TS2) else None,
            }
        )
        json_data["ts3"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TS3 if not np.isnan(row.TS3) else None,
            }
        )
        json_data["tr1"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TR1 if not np.isnan(row.TR1) else None,
            }
        )
        json_data["tr2"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TR2 if not np.isnan(row.TR2) else None,
            }
        )
        json_data["tr3"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.TR3 if not np.isnan(row.TR3) else None,
            }
        )
        json_data["open"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.Open if not np.isnan(row.Open) else None,
            }
        )
        json_data["high"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.High if not np.isnan(row.High) else None,
            }
        )
        json_data["low"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.Low if not np.isnan(row.Low) else None,
            }
        )
        json_data["close"].append(
            {
                "time": row.Index.strftime("%Y-%m-%d"),
                "value": row.Close if not np.isnan(row.Close) else None,
            }
        )

    return json_data


# Fetch and display the candlestick chart
if stock_ticker and start_date and end_date:
    json_data = perform_calculation(stock_ticker, start_date, end_date)
    
    # Convert JSON data to string
    json_str = json.dumps(json_data, indent=4)
    
    # Add download button for JSON data
    st.download_button(
        label="Download JSON Data",
        data=json_str,
        file_name=f"{stock_ticker}_data.json",
        mime="application/json",
    )
