import yfinance as yf
import pandas as pd

# List of NSE stock tickers with their respective sectors
nse_tickers_sectors = {
    "RELIANCE.NS": "Energy",
    "TCS.NS": "Information Technology",
    "INFY.NS": "Information Technology",
    "HDFCBANK.NS": "Banking and Financial Services",
    "ICICIBANK.NS": "Banking and Financial Services",
    "SBIN.NS": "Banking and Financial Services",
    "HINDUNILVR.NS": "Consumer Goods",
    "BHARTIARTL.NS": "Telecommunications",
    "ITC.NS": "Consumer Goods",
    "LT.NS": "Cement and Construction",
    "ASIANPAINT.NS": "Consumer Goods",
    "MARUTI.NS": "Automobiles",
    "AXISBANK.NS": "Banking and Financial Services",
    "WIPRO.NS": "Information Technology",
    "HCLTECH.NS": "Information Technology",
    "BAJFINANCE.NS": "Banking and Financial Services",
    "KOTAKBANK.NS": "Banking and Financial Services",
    "TATAMOTORS.NS": "Automobiles",
    "SUNPHARMA.NS": "Healthcare and Pharmaceuticals",
    "ULTRACEMCO.NS": "Cement and Construction",
    "ADANIENT.NS": "Energy",
    "NTPC.NS": "Energy",
    "POWERGRID.NS": "Energy",
    "TATASTEEL.NS": "Metals and Mining",
    "JSWSTEEL.NS": "Metals and Mining",
    "HDFCLIFE.NS": "Banking and Financial Services",
    "TECHM.NS": "Information Technology",
    "MARICO.NS": "Consumer Goods",
    "BRITANNIA.NS": "Consumer Goods",
    "DRREDDY.NS": "Healthcare and Pharmaceuticals",
    "DIVISLAB.NS": "Healthcare and Pharmaceuticals",
    "EICHERMOT.NS": "Automobiles",
    "DMART.NS": "Retail",
    "MOTHERSON.NS": "Automobiles",
    "BAJAJ-AUTO.NS": "Automobiles",
    "HEROMOTOCO.NS": "Automobiles",
    "BHARATFORG.NS": "Automobiles",
    "UPL.NS": "Chemicals",
    "HINDALCO.NS": "Metals and Mining",
    "INDUSINDBK.NS": "Banking and Financial Services",
    "GRASIM.NS": "Cement and Construction",
    "BAJAJFINSV.NS": "Banking and Financial Services",
    "BPCL.NS": "Energy",
    "IOC.NS": "Energy",
    "CIPLA.NS": "Healthcare and Pharmaceuticals",
    "LUPIN.NS": "Healthcare and Pharmaceuticals",
    "M&M.NS": "Automobiles",
    "SBILIFE.NS": "Banking and Financial Services",
    "ZEEL.NS": "Media"
}

# Fetch stock data for each ticker
data = []
serial_number = 1  # Initialize serial number

for ticker, sector in nse_tickers_sectors.items():
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="max")  # Fetch historical data to get the date range
    
    if not hist.empty:
        data_from = hist.index.min().date()
        data_to = hist.index.max().date()
    else:
        data_from = data_to = "N/A"
    
    # Append data with serial number and stock name
    data.append({
        'Serial Number': serial_number,
        'Ticker': ticker,
        'Name': info.get('shortName', 'N/A'),
        'Sector': sector,
        'Market Cap': info.get('marketCap', 'N/A'),
        'Volume': info.get('volume', 'N/A'),
        'Previous Close': info.get('regularMarketPreviousClose', 'N/A'),
        'PE Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        'Data Available From': data_from,
        'Data Available To': data_to
    })
    serial_number += 1  # Increment serial number

# Create DataFrame
df = pd.DataFrame(data)

# Convert 'Market Cap' to numeric and handle errors
df['Market Cap'] = pd.to_numeric(df['Market Cap'], errors='coerce')

# Sort by market capitalization (ascending)
df_sorted = df.sort_values(by='Market Cap', ascending=True)

# Save the results to a CSV file
csv_filename = 'nse_stock_data_with_name_sector_date_range.csv'
df_sorted.to_csv(csv_filename, index=False)

# Display a confirmation message
print(f"CSV file with stock name, sector, date range, and serial number has been created and saved as {csv_filename}")

# Optionally, display the sorted DataFrame
print(df_sorted)
