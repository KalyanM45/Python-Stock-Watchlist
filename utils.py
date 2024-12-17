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
    
def get_day_suffix(day):
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix

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

            # Format the date to "16th Dec 24 12:00 AM"
            date_time_obj = row.name
            day = date_time_obj.day
            suffix = get_day_suffix(day)
            date_time = date_time_obj.strftime(f"{day}{suffix} %b'%y %I:%M %p")

            # Get the company name
            company_name = stock.info.get('longName', 'N/A')


            response =  {
                'ticker': ticker,
                'company_name': company_name,
                'price': f'${price:.2f}',
                'date_time': date_time,
                'high': f'{high:.2f}',
                'low': f'{low:.2f}',
                'volume': f'{volume:.2f}',
                'change': f'{change:.2f}',
                'change_percent': f'{change_percent:.2f}%'
            }

            return response
        else:
            return None
    except Exception as e:
        # Updated line: Added print statement for debugging
        print(f"Error fetching data for {ticker}: {e}")
        return None