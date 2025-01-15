#IMPORTING LIBRARIES 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime
import streamlit as st

# INITIAL STOCK PORTFOLIO OWNED BY ME
stock_portfolio = {
    "ASHOKLEY": 80,
    "TATAPOWER": 80,
    "TATMOTORS": 60,
    "IREDA": 116,
    "MOREPENLAB": 167,
    "BANKOFMAHARASHTRA": 220,
    "COCHINSHIP": 18,
}

# PRICE PER SHARE OF MY OWNED STOCKS
price_per_share = {
    "ASHOKLEY": "₹209",
    "TATAPOWER": "₹410",
    "TATMOTORS": "₹960",
    "IREDA": "₹218",
    "MOREPENLAB": "₹84",
    "BANKOFMAHARASHTRA": "₹65",
    "COCHINSHIP": "₹1530",
}

# Streamlit UI
st.title("Stock Portfolio Manager")
st.sidebar.title("Portfolio Actions")

# ACTION BUTTONS IN THE SIDEBAR
actions = st.sidebar.radio(
    "Select an Action",
    options=["View Portfolio", "Total Investment", "Buy Stock", "Sell Stock", "Stock Trend", 
             "Average Daily Return", "Volatility", "Risk vs Return","Daily Trading Volume"]
)

# COMMAND-1: VIEW PORTFOLIO
if actions == "View Portfolio":
    st.subheader("Your Stock Portfolio:")

    #CREATING DATAFRAMES TO HANDLE VALUES LIKE STOCKS OWNED AND THE INITIAL INVESTMENT
    df_stocks = pd.DataFrame(list(stock_portfolio.items()), columns=["STOCK", "SHARES OWNED"])
    df_price = pd.DataFrame(list(price_per_share.items()), columns=["STOCK", "PRICE/SHARE"])

    #MERGING THE TWO DATAFRAMES
    df_portfolio = pd.merge(df_stocks, df_price, on="STOCK", how="left")
    st.dataframe(df_portfolio)

# COMMAND-2: TOTAL INVESTMENT
elif actions == "Total Investment":
    st.subheader("Total Investment and Portfolio Value:")

    #ALL THE DATAFRAMES AS A FINAL PORTFOLIO
    df_stocks = pd.DataFrame(list(stock_portfolio.items()), columns=["STOCK", "SHARES OWNED"])
    df_price = pd.DataFrame(list(price_per_share.items()), columns=["STOCK", "PRICE/SHARE"])
    df_portfolio = pd.merge(df_stocks, df_price, on="STOCK", how="left")

    #HANDLING THE ₹ SYMBOL TO INITIATE THE CALCULATIONS AS ITS A STRING AND ONLY NUMERIC VALUES CAN PERFORM CALCULATIONS
    df_portfolio["PRICE/SHARE"] = df_portfolio["PRICE/SHARE"].replace("₹", "", regex=True).astype(float)
    df_portfolio["TOTAL INVESTMENT"] = df_portfolio["SHARES OWNED"] * df_portfolio["PRICE/SHARE"]
    total_investment = df_portfolio["TOTAL INVESTMENT"].sum()

    #AGAIN ADDING THE ₹ SYMBOL TO THE DATAFRAMES AS CALCULATIONS ARE PERFORMED
    df_portfolio["TOTAL INVESTMENT"] = "₹" + df_portfolio["TOTAL INVESTMENT"].astype(int).astype(str)
    st.write(f"Total Portfolio Value: ₹{int(total_investment)}")

    #DSIPLAYING THE PORTFOLIO
    st.dataframe(df_portfolio)

# COMMAND-3: BUY STOCK
elif actions == "Buy Stock":
    st.subheader("Buy a Stock")
    buy_stock = st.text_input("Enter the Stock Ticker (e.g., TATAPOWER)")
    buy_price = st.number_input("Enter the Price per Share", min_value=1, value=200)
    quantity = st.number_input("Enter the Number of Shares", min_value=1, value=1)
    
    #IF STOCK IS ALREADY IN THE PORTFOLIO THEN ADDING ITS MORE QUANTITY AND AVERAGING THE PRICE
    if st.button("Add Stock"):

        #FETCHING THE DATE FROM THE PORTFOLIO OWNED
        if buy_stock in stock_portfolio:
            old_quantity = stock_portfolio[buy_stock]
            old_price = int(price_per_share[buy_stock].replace("₹", ""))

            #AVERAGING THE PRICE OF THE EXISTING STOCK WHEN MORE SHARE(S) ARE ADDED
            new_avg_price = ((old_price * old_quantity) + (buy_price * quantity)) / (old_quantity + quantity)
            stock_portfolio[buy_stock] += quantity
            price_per_share[buy_stock] = f"₹{round(new_avg_price, 2)}"

            #DISPLAYING ADDED SHARE(S) WITH AVERAGE PRICE
            st.write(f"{quantity} share(s) added to {buy_stock} at ₹{round(new_avg_price, 2)} per share.")

        #IF THE STOCKKIS NEW TO THE PORTFOLIO THEN ADDING THE FRESH SHARE(S)
        else:
            stock_portfolio[buy_stock] = quantity
            price_per_share[buy_stock] = f"₹{buy_price}"

            #DISPLAYING NEW STOCK AND THE SHARE(S) ADDED TO THE PORTFOLIO WITH BUY PRICE
            st.write(f"{buy_stock} added to the portfolio with {quantity} share(s) at ₹{buy_price} per share.")
        
        #DISPLAYING THE NEW UPDATED PORTFOLIO BY HANDLING THE DATAFRAMES
        df_stocks = pd.DataFrame(list(stock_portfolio.items()), columns=["STOCK", "SHARES OWNED"])
        df_price = pd.DataFrame(list(price_per_share.items()), columns=["STOCK", "PRICE/SHARE"])
        df_portfolio = pd.merge(df_stocks, df_price, on="STOCK", how="left")
        st.dataframe(df_portfolio)

# COMMAND-4: SELL STOCK
elif actions == "Sell Stock":
    st.subheader("Sell a Stock")
    sell_stock = st.text_input("Enter the Stock Ticker (e.g., TATAPOWER)")
    sell_price = st.number_input("Enter the Selling Price per Share", min_value=1, value=200)
    quantity = st.number_input("Enter the Number of Shares", min_value=1, value=1)

    #IF STOCK IS ALREADY IN THE PORTFOLIO THEN SELING THE SHARES AND AVERAGING THE PRICE
    if st.button("Sell Stock"):

        #FETCHING THE DATE FROM THE PORTFOLIO OWNED
        if sell_stock in stock_portfolio:
            old_quantity = stock_portfolio[sell_stock]
            old_price = int(price_per_share[sell_stock].replace("₹", ""))

            #AVERAGING THE PRICE OF THE EXISTING STOCK WHEN SOME SHARE(S) ARE SOLD
            new_avg_price = ((old_price * old_quantity) - (sell_price * quantity)) / (old_quantity - quantity)
            stock_portfolio[sell_stock] -= quantity
            price_per_share[sell_stock] = f"₹{round(sell_price, 2)}"

            #DISPLAYING ADDED SHARE(S) WITH AVERAGE PRICE
            st.write(f"{quantity} share(s) of {sell_stock} sold at ₹{sell_price} per share.")
        
        #DISPLAYING THE NEW UPDATED PORTFOLIO BY HANDLING THE DATAFRAMES
        df_stocks = pd.DataFrame(list(stock_portfolio.items()), columns=["STOCK", "SHARES OWNED"])
        df_price = pd.DataFrame(list(price_per_share.items()), columns=["STOCK", "PRICE/SHARE"])
        df_portfolio = pd.merge(df_stocks, df_price, on="STOCK", how="left")
        st.dataframe(df_portfolio)

# COMMAND-5: STOCK TREND
elif actions == "Stock Trend":
    st.subheader("Stock Price Trend")

    #GETIING INPUT AS THE STOCK(S) "TICKER"(S)
    tickers = st.text_input("Enter Stock Ticker(s) (e.g., TATAPOWER, TATMOTORS)").split(",")

    #STARTING DATE AND ENDING DATE FOR FETCHING THE DATA
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    if st.button("Plot Trend"):

        #FETCHING DATA FROM YAHOO FINANCE
        data = yf.download(tickers, start=start_date, end=end_date, threads=False)

        #ADJUSTING THE CLOSSING PRICE FOR VISUALISATION
        adj_close = data["Adj Close"]

        #PLOTTING THE TRENDLINE 
        plt.figure(figsize=(15, 7))

        #FOR A SINGLE TICKER
        if len(tickers) == 1:
            plt.plot(adj_close, label=tickers[0])

        #FOR MORE TICKERS
        else:
            for ticker in tickers:
                if ticker in adj_close.columns:
                    plt.plot(adj_close[ticker], label=ticker)
        plt.title("Stock Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Adjusted Closing Price")
        plt.legend()
        st.pyplot()

# COMMAND-6: AVERAGE DAILY RETURN
elif actions == "Average Daily Return":
    st.subheader("Average Daily Return")

    #GETIING INPUT AS THE STOCK(S) "TICKER"(S)
    tickers = st.text_input("Enter Stock Ticker(s) (e.g., TATAPOWER, TATMOTORS)").split(",")

    #STARTING DATE AND ENDING DATE FOR FETCHING THE DATA
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    

    if st.button("Plot Return"):

        #FETCHING DATA FROM YAHOO FINANCE 
        data = yf.download(tickers, start=start_date, end=end_date, threads=False)

        #ADJUSTING THE CLOSING PRICE 
        adj_close = data["Adj Close"]

        #CALCULATING THE RETURNS BY CONVERTING IT TO PERCENTAGE AND THEN INTO DAILY MEAN
        returns = adj_close.pct_change().dropna()
        average_daily_return = returns.mean() * 100

        #PLOTTING THE BAR GRAPH
        plt.figure(figsize=(15, 7))
        average_daily_return.plot(kind="bar", color="pink", edgecolor="black")

        #LABELLING
        plt.title("Average Daily Return (%)")
        plt.xlabel("Tickers")
        plt.ylabel("Daily Return (%)")
        plt.xticks(rotation=5)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot()

# COMMAND-7: VOLATILITY
elif actions == "Volatility":
    st.subheader("Stock Volatility")

   #GETIING INPUT AS THE STOCK(S) "TICKER"(S)
    tickers = st.text_input("Enter Stock Ticker(s) (e.g., TATAPOWER, TATMOTORS)").split(",")

    #STARTING DATE AND ENDING DATE FOR FETCHING THE DATA
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Plot Volatility"):

        #FETCHING DATA FROM YAHOO FINANCE 
        data = yf.download(tickers, start=start_date, end=end_date, threads=False)

        #ADJUSTING THE CLOSING PRICE 
        adj_close = data["Adj Close"]

        #ADJUSTING THE RETURNS INTO VOLATILITY
        returns = adj_close.pct_change().dropna()
        volatility = returns.std() * 100

        #PLOTTING THE BAR GRAPH
        plt.figure(figsize=(15, 7))
        volatility.plot(kind="bar", color="red", edgecolor="black")

        #LABELLING 
        plt.title("Daily Volatility (%)")
        plt.xlabel("Tickers")
        plt.ylabel("Volatility (%)")
        plt.xticks(rotation=5)
        plt.grid(axis="y", alpha=0.7, linestyle="--")
        st.pyplot()

# COMMAND-8: RISK V/S RETURN
elif actions == "Risk vs Return":
    st.subheader("Risk vs Return")

   #GETIING INPUT AS THE STOCK(S) "TICKER"(S)
    tickers = st.text_input("Enter Stock Ticker(s) (e.g., TATAPOWER, TATMOTORS)").split(",")

    #STARTING DATE AND ENDING DATE FOR FETCHING THE DATA
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    if st.button("Plot Risk vs Return"):
        
        #FETCHING DATA FROM YAHOO FINANCE 
        data = yf.download(tickers, start=start_date, end=end_date, threads=False)

        #CHANGING THE RETURNS INTO AVERAGE DAILY RETURN
        adj_close = data["Adj Close"]
        returns = adj_close.pct_change().dropna()
        volatility = returns.std() * 100
        average_daily_returns = returns.mean() * 100

        #PLOTTING THE SCATTER PLOT
        plt.figure(figsize=(15, 7))
        plt.scatter(volatility, average_daily_returns, color="purple", s=100)

        #LABELLING IT AND SPECIFYING THE FONTSIZE , H-AXIS, V-AXIS AND MANAGING AS MANY TICKERS AS IT CAN ON THE BASIS OF THE USER INPUT
        for i, ticker in enumerate(tickers):
            plt.text(volatility[i], average_daily_returns[i], ticker, fontsize=12, ha='right', va='bottom')
        plt.title("Risk vs Return (Volatility vs Average Returns)")
        plt.xlabel("Volatility (%)")
        plt.ylabel("Average Returns (%)")
        plt.grid(alpha=0.7)
        st.pyplot()


#COMMAND-9: DAILY TRADING VOLUME
elif actions == "Daily Trading Volume":
    st.subheader("Daily Trading Volumes")

    # Getting tickers from the user
    tickers = st.text_input("Enter Stock Ticker(s) (e.g., TATAPOWER, TATMOTORS)").split(",")

    # Getting the start and end date of the data
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Daily Trading Volume"):

        # Fetching data of the tickers
        data = yf.download(tickers, start=start_date, end=end_date, threads=False)

        volume = data["Volume"]

        # Plotting the bar graph of daily trading volume for all tickers
        plt.figure(figsize=(15, 7))

        # Creating a bar plot where each ticker's volume is displayed separately
        for idx, tickerf in enumerate(tickers):
            if tickerf in volume.columns:
                # Plot the volume for each ticker as a separate bar on the same x-axis (date)
                plt.bar(volume.index + pd.Timedelta(days=idx * 1), volume[tickerf], label=tickerf, alpha=0.6, width=0.8)

        plt.title("Daily Trading Volume")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.xticks(rotation=45)
        plt.grid(axis="y", alpha=0.7, linestyle="--")
        plt.legend()
        st.pyplot()


