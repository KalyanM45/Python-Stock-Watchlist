import json
import yfinance as yf

WATCHLIST = 'watchlist.json'

def save_watchlist(tickers):
    with open(WATCHLIST, 'w') as f:
        json.dump(tickers, f)

def load_watchlist():
    try:
        with open(WATCHLIST, 'r') as f:
            tickers = json.load(f)
        return tickers
    except FileNotFoundError:
        return []

def fetch_watchlist(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            row = data.iloc[-1]
            price = row['Close']
            high = row['High']
            low = row['Low']
            volume = row['Volume']
            
            # Updated line: Ensure 'previousClose' is retrieved safely
            prev_close = stock.info.get('previousClose', price)  
            
            change = price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            date_time = row.name.strftime('%Y-%m-%d %H:%M:%S')

            response =  {
                'ticker': ticker,
                'price': f'${price:.2f}',
                'date_time': date_time,
                'high': f'{high:.4f}',
                'low': f'{low:.4f}',
                'volume': f'{volume:.4f}',
                'change': f'{change:.4f}',
                'change_percent': f'{change_percent:.4f}%'
            }

            return response
        else:
            return None
    except Exception as e:
        # Updated line: Added print statement for debugging
        print(f"Error fetching data for {ticker}: {e}")
        return None