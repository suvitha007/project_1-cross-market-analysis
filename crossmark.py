import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:1234@localhost:3306/cross_market")
from sqlalchemy import text
st.title("*CROSS MARKET ANALYSIS*")
st.title("Crypto, Oil & Stocks overview")
st.subheader("Cross-Market Analysis Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Market overview",
        "🎉 SQL Query runner",
        "🪙 Crypto analysis"
    ]
)

if page == "📊 Market overview":

    st.header("📊 Market Overview")
    st.write("welcome to page_1 market overview") 
    
    # Date Filters
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Bitcoin Average Price Analysis"):
        btc_avg = pd.read_sql(
            """
            SELECT AVG(price_usd) AS avg_bitcoin
            FROM hist_prices
            WHERE coin_id = 'bitcoin'
              AND DATE(date) BETWEEN %s AND %s
            """,
            engine,
            params=(start_date, end_date)
        )
        st.write("Bitcoin Avg Price:", btc_avg["avg_bitcoin"][0])

    if st.button("Oil Average Price"):
        oil_avg = pd.read_sql(
            """
            SELECT AVG(price) AS avg_oil_price
            FROM oil_price
            WHERE DATE(date) BETWEEN %s AND %s
            """,
            engine,
            params=(start_date, end_date)
        )
        st.write(oil_avg)

    if st.button("^GSPC Average Price Analysis"):
        sp500_avg = pd.read_sql(
            """
            SELECT AVG(close) AS avg_sp500_price
            FROM stock_prices
            WHERE Ticker = '^GSPC'
              AND DATE(date) BETWEEN %s AND %s
            """,
            engine,
            params=(start_date, end_date)
        )
        st.write(sp500_avg)

    if st.button("^NSEI Average Price"):
        nifty_avg = pd.read_sql(
            """
            SELECT AVG(close) AS avg_nifty_price
            FROM stock_prices
            WHERE Ticker = '^NSEI'
              AND DATE(date) BETWEEN %s AND %s
            """,
            engine,
            params=(start_date, end_date)
        )
        st.write(nifty_avg)

        snapshot_df = pd.read_sql(
        """
        SELECT 
        DATE(hp.date) AS market_date,
        hp.price_usd AS bitcoin_price,
        o.price AS oil_price,
        sp_gspc.close AS sp500_close,
        sp_nsei.close AS nifty_close
        FROM hist_prices hp
        JOIN oil_price o
            ON DATE(hp.date) = o.date
        JOIN stock_prices sp_gspc
            ON DATE(hp.date) = sp_gspc.date
            AND sp_gspc.ticker = '^GSPC'
        JOIN stock_prices sp_nsei
            ON DATE(hp.date) = sp_nsei.date
            AND sp_nsei.ticker = '^NSEI'
        WHERE hp.coin_id = 'bitcoin'
        ORDER BY market_date;
        """,
        engine
    )
        st.subheader("📊 Daily Market Snapshot Table")
        st.dataframe(snapshot_df, use_container_width=True)

elif page == "🎉 SQL Query runner":

    st.title("🎉 SQL Query runner")
    st.write("Select a SQL query and click Run Query") 
    query_option = st.selectbox(
            "Choose a query",
        (
            "Bitcoin Average Price",
            "Find the top 3 cryptocurrencies by market cap",
            "List all coins where circulating supply exceeds 90 percent of total supply.",
            "Get coins that are within 10 percent of their all-time-high (ATH).",
            "Find the average market cap rank of coins with volume above $1B.",
            "Get the most recently updated coin.",
            "Find the highest daily price of Bitcoin in the last 365 days.",
            "Calculate the average daily price of Ethereum in the past 1 year.",
            "Show the daily price trend of Bitcoin in Feb 2026.",
            "Find the coin with the highest average price over 1 year.",
            "Get the percentage change in Bitcoin price during Feb 2026",
            "Find the highest oil price in the last 5 years.",
            "Get the average oil price per year.",
            "Show oil prices during COVID crash (March-April 2020).",
            "Find the lowest price of oil in the last 10 years.",
            "Calculate the volatility of oil prices (max-min difference per year).",
            "Get all stock prices for given ticker",
            "Find the highest closing price for NASDAQ (^IXIC)",
            "List top 5 days with highest price difference for S&P 500 (^GSPC)",
            "Get monthly average closing price for each ticker",
            "Get average trading volume of NSEI in 2024",
            "Compare Bitcoin vs Oil average price in 2025.",
            "Check if Bitcoin moves with S&P 500",
            "Compare Ethereum and NASDAQ daily prices for 2025",
            "Find days when oil price spiked and compare with Bitcoin price change",
            "Compare top 3 coins daily price trend vs Nifty (^NSEI)",
            "Compare stock prices (^GSPC) with crude oil prices on the same dates",
            "Correlate Bitcoin closing price with crude oil closing price (same date)",
            "Compare NASDAQ (^IXIC) with Ethereum price trends",
            "Join top 3 crypto coins with stock indices for 2025",
            "Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison",
            
        )
    )

    
    if st.button("Run Query"):
        if query_option == "Bitcoin Average Price":
            sql = """
                select  id, name, market_cap from records order by  market_cap desc limit 5
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Find the top 3 cryptocurrencies by market cap":
            sql = """
              select* from records order by market_cap_rank  limit 3 
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "List all coins where circulating supply exceeds 90 percent of total supply.":  
            sql = "select* from records where (circulating_supply*100/total_supply)>90"  
            df=pd.read_sql(sql,engine)
            st.dataframe(df)      
        elif query_option == "Get coins that are within 10 percent of their all-time-high (ATH).":
            sql="select* from records where current_price >= 0.9 * ath"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)  
        elif query_option == "Find the average market cap rank of coins with volume above $1B.":
            sql = "select id,market_cap_rank from records where total_volume > 1000000000"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)  
        elif query_option == "Get the most recently updated coin.":
            sql = "select* from records order by last_update desc limit 1"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Find the highest daily price of Bitcoin in the last 365 days.":
            sql = "SELECT MAX(price_usd) AS highest_price FROM hist_prices where coin_id='bitcoin' and date >= curdate() - interval 365 day"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Calculate the average daily price of Ethereum in the past 1 year.":
            sql = """SELECT AVG(price_usd) from hist_prices where coin_id = 'ethereum'and date >= CURDATE() - INTERVAL 1 YEAR"""
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Show the daily price trend of Bitcoin in Feb 2026.":
            sql = "select date, price_usd from hist_prices where coin_id = 'bitcoin'and date between '2025-01-01' and'2025-03-31' order by date"    
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Find the coin with the highest average price over 1 year.":
            sql = "SELECT coin_id,AVG(price_usd) AS avg_price from hist_prices where date >= CURDATE() - INTERVAL 1 YEAR group by coin_id order by avg_price desc limit 1"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)  
        elif query_option == "Get the percentage change in Bitcoin price during Feb 2026":
            sql = """SELECT 
                ((MAX(price_usd) - MIN(price_usd)) / MIN(price_usd)) * 100 AS pct_change
                FROM hist_prices
                WHERE coin_id = 'bitcoin'
                AND date BETWEEN '2024-09-01' AND '2025-09-01';
                """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)  
        elif query_option == "Find the highest oil price in the last 5 years.":
            sql = "select max(price) as highest_price from  oil_price where date >= CURDATE() - interval 5 year"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Get the average oil price per year.":
            sql = "select year(date) AS year, avg(price) AS avg_price from oil_price group by year(date) order by year"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Find the lowest price of oil in the last 10 years.":
            sql = "select MIN(price) AS lowest_price from oil_price where date >= CURDATE() - interval 10 year"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Show oil prices during COVID crash (March-April 2020).":
            sql ="select date, price FROM oil_price WHERE date BETWEEN '2020-03-01' AND '2020-04-30' ORDER BY date "
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Calculate the volatility of oil prices (max-min difference per year).":     
            sql = "select max(price) - min(price) as volatility from oil_data where date>=now() - interval 1 year"
            df=pd.read_sql(sql,engine)
            st.dataframe(df)    
        elif query_option == "Get all stock prices for given ticker":
            sql = """
            SELECT *
            FROM stock_prices
            WHERE Ticker IN ('^IXIC', '^NSEI', '^GSPC')
            ORDER BY Ticker, Date
            """ 
            df=pd.read_sql(sql,engine)
            st.dataframe(df)    
        elif query_option == "Find the highest closing price for NASDAQ (^IXIC)":
            sql = """SELECT MAX(Close) AS highest_closing_price
            FROM stock_prices
            WHERE Ticker = '^IXIC'"""      
            df=pd.read_sql(sql,engine)
            st.dataframe(df)    
        elif query_option == "List top 5 days with highest price difference for S&P 500 (^GSPC)":
            sql="""
            SELECT Date,High,Low,(High - Low) AS price_difference
            FROM stock_prices
            WHERE Ticker = '^GSPC'
            ORDER BY price_difference DESC
            LIMIT 5
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df) 
        elif query_option == "Get monthly average closing price for each ticker":
            sql = """SELECT Ticker,YEAR(Date) AS year,MONTH(Date) AS month,AVG(Close) AS avg_monthly_close
            FROM stock_prices
            GROUP BY Ticker, YEAR(Date), MONTH(Date)
            ORDER BY Ticker, year, month
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Get average trading volume of NSEI in 2024":
            sql="""
            SELECT AVG(Volume) AS avg_trading_volume_2024
            FROM stock_prices
            WHERE Ticker = '^NSEI'
            AND YEAR(Date) = 2024
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "Compare Bitcoin vs Oil average price in 2025.": 
            sql="""
            SELECT AVG(hp.price_usd) AS btc_avg,
            AVG(op.price) AS oil_avg
            FROM hist_prices hp
            JOIN oil_price op 
            ON hp.date = op.date
            WHERE hp.coin_id = 'bitcoin'
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option == "check if Bitcoin moves with S&P 500":
            sql="""
            SELECT hp.date,hp.price_usd AS btc_price,sp.Close AS sp500_close
            FROM hist_prices hp
            JOIN stock_prices sp
            ON DATE(hp.date) = sp.Date
            WHERE hp.coin_id = 'bitcoin'
            AND sp.Ticker = '^GSPC'
            ORDER BY hp.date
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Compare Ethereum and NASDAQ daily prices for 2025":
            sql="""SELECT hp.date,
            hp.price_usd AS ethereum_price,
            sp.close AS nasdaq_close
            FROM hist_prices hp
            JOIN Stock_prices sp
            ON hp.date = sp.date
            WHERE hp.coin_id = 'ethereum'
            AND sp.ticker = '^IXIC'
            AND YEAR(hp.date) = 2025
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Find days when oil price spiked and compare with Bitcoin price change":
            sql="""SELECT 
            o1.date AS market_date,
            o1.price AS oil_price,
            (o1.price - o2.price) AS oil_price_spike,
            hp.price_usd AS bitcoin_price
            FROM oil_price o1
            JOIN oil_price o2 
            ON o1.date = DATE_ADD(o2.date, INTERVAL 1 DAY)
            JOIN hist_prices hp
            ON DATE(hp.date) = o1.date
            WHERE hp.coin_id = 'bitcoin'
            ORDER BY oil_price_spike DESC
            LIMIT 20
            """
           
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
           
        elif query_option=="Compare top 3 coins daily price trend vs Nifty (^NSEI)":
            sql="""
            SELECT hp.coin_id,
            DATE(hp.date) AS date,
            hp.price_usd,
            sp.Close AS nifty_close
            FROM hist_prices hp

            JOIN (
            SELECT id
            FROM records
            ORDER BY market_cap DESC
            LIMIT 3
            ) top_coins
            ON hp.coin_id = top_coins.id

            JOIN stock_prices sp
            ON DATE(hp.date) = sp.Date

            WHERE sp.Ticker = '^NSEI'
            ORDER BY date
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Compare stock prices (^GSPC) with crude oil prices on the same dates": 
            sql="""SELECT 
            DATE(s.date) AS date,
            s.close AS sp500_price,
            o.price AS oil_price
            FROM stock_prices s
            JOIN oil_price o
            ON DATE(s.date) = o.date
            WHERE s.ticker = '^GSPC'
            ORDER BY date
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Correlate Bitcoin closing price with crude oil closing price (same date)":
            sql="""SELECT DATE(hp.date) AS date,
            hp.price_usd AS btc_price,
            o.price AS oil_price
            FROM hist_prices hp
            JOIN oil_price o
            ON DATE(hp.date) = o.date
            WHERE hp.coin_id = 'bitcoin'
            ORDER BY date"""
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Compare NASDAQ (^IXIC) with Ethereum price trends":
            sql="""SELECT DATE(hp.date) AS date,
            hp.price_usd AS ethereum_price,
            sp.Close AS nasdaq_close
            FROM hist_prices hp
            JOIN stock_prices sp
            ON DATE(hp.date) = sp.Date
            WHERE hp.coin_id = 'ethereum'
            AND sp.Ticker = '^IXIC'
            ORDER BY date"""
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        elif query_option=="Join top 3 crypto coins with stock indices for 2025":
            sql="""
            SELECT hp.coin_id,
            hp.date,
            hp.price_usd,
            sp.ticker,
            sp.close
            FROM hist_prices hp

            JOIN (
            SELECT id
            FROM records
            ORDER BY market_cap DESC
            LIMIT 3
            ) top_coins
            ON hp.coin_id = top_coins.id

            JOIN Stock_prices sp
            ON hp.date = sp.date

            WHERE YEAR(hp.date) = 2025
            ORDER BY hp.coin_id, hp.date"""
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
        
        elif query_option=="Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison":  
            sql="""
            SELECT 
             DATE(hp.date) AS date,
            hp.price_usd AS bitcoin_price,
            op.price AS oil_price,
            sp.Close AS sp500_close
            FROM hist_prices hp

            JOIN oil_price op
            ON DATE(hp.date) = op.date

            JOIN stock_prices sp
            ON DATE(hp.date) = sp.Date

            WHERE hp.coin_id = 'bitcoin'
            AND sp.Ticker = '^GSPC'

            ORDER BY date
            """
            df=pd.read_sql(sql,engine)
            st.dataframe(df)
elif page == "🪙 Crypto analysis":
    st.title("Top 3 Crypto analysis")
    st.write("Select a coin and date range to view price trends")
    coin = st.selectbox(
        "Select Coin",
        ("bitcoin", "ethereum", "tether")
    )

    start_date = st.date_input("Start date", key="p3_start")
    end_date = st.date_input("End date", key="p3_end")
    if st.button("View Price Trend"):
        df = pd.read_sql(
            """
            SELECT
                DATE(last_update) AS date,
                current_price
            FROM records
            WHERE id = %s
              AND DATE(last_update) BETWEEN %s AND %s
            ORDER BY date
            """,
            engine,
            params=(coin, start_date, end_date)
        )
        if df.empty:
            st.warning("No data available for the selected coin and date range.")

        else:

            # --- Table ---
            st.subheader("📊Daily Price Table")
            st.dataframe(df)    

    