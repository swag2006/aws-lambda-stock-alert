import yfinance as yf
import ta
import os
from ta.trend import EMAIndicator, MACD

# Read period & interval from env (with sensible defaults)
PERIOD   = os.environ.get('DATA_PERIOD',   '7d')
INTERVAL = os.environ.get('DATA_INTERVAL', '1h')

def fetch_stock_data(ticker):
    # no more hard‑coded args
    return yf.download(ticker, period=PERIOD, interval=INTERVAL)


def calculate_indicators(data):
    close = data['Close'].squeeze()    # ensure a Series
    data['EMA9'] = EMAIndicator(close=close, window=9).ema_indicator()
    data['EMA21'] = EMAIndicator(close=close, window=21).ema_indicator()
    macd = MACD(close=close)
    data['MACD_Histogram'] = macd.macd_diff()
    return data

def check_signals(data):
    prev_ema9   = data['EMA9'].iat[-2]
    prev_ema21  = data['EMA21'].iat[-2]
    curr_ema9   = data['EMA9'].iat[-1]
    curr_ema21  = data['EMA21'].iat[-1]
    curr_hist   = data['MACD_Histogram'].iat[-1]

    buy  = (prev_ema9 <= prev_ema21) and (curr_ema9 > curr_ema21) and (curr_hist > 0)
    sell = (prev_ema9 >= prev_ema21) and ((curr_ema9 < curr_ema21) or (curr_hist < 0))
    return buy, sell

def lambda_handler(event, context):
    # read tickers from env var
    stocks = [s.strip() for s in os.environ['STOCKS'].split(',')]

    buys, sells = [], []
    for ticker in stocks:
        data = fetch_stock_data(ticker)
        if data.empty or len(data) < 22:
            continue

        data = calculate_indicators(data)
        buy, sell = check_signals(data)

        if buy:
            buys.append(ticker)
        if sell:
            sells.append(ticker)

    # build formatted text
    if not buys and not sells:
        body = "No signals"
    else:
        lines = []
        if buys:
            lines.append("✅ BUY:  " + ", ".join(buys))
        if sells:
            lines.append("❌ SELL: " + ", ".join(sells))
        body = "\n".join(lines)

    return {
        'statusCode': 200,
        'body': body
    }