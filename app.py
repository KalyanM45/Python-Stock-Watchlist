from flask import Flask, render_template, request, redirect, url_for, flash
from utils import load_watchlist, save_watchlist, fetch_watchlist

app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/', methods=['GET', 'POST'])
def index():
    tickers = load_watchlist()
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper()
        if not ticker:
            flash('Please Enter a Ticker', 'error')
        else:
            response = fetch_watchlist(ticker)
            if response:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)
                    flash(f'{ticker} added to watchlist', 'success')
                else:
                    flash(f'{ticker} already in watchlist', 'info')
            else:
                flash(f'Problem with {ticker}', 'error')

            return redirect(url_for('index'))
    else:
        stocks_data = []
        for ticker in tickers:
            response = fetch_watchlist(ticker)
            if response:
                stocks_data.append(response)

        return render_template('index.html', stocks_data=stocks_data)
        
@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlist()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f'{ticker} removed from watchlist', 'success')
    else:
        flash(f'{ticker} not in watchlist', 'info')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)