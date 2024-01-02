import pandas as pd
import yfinance as yf
import mplfinance as mpf

ticker = 'TUPRS.IS'
df = yf.download(
    tickers=ticker,
    start='2023-09-01',
    interval='1d',
    progress=False
)

def ATR(df, window):
    atr = pd.DataFrame()
    tr = pd.DataFrame()
    tr['H-L'] = df['High'] - df['Low']
    tr['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    tr['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    tr['TR'] = tr[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    atr['ATR'] = tr['TR'].rolling(window=window, min_periods=1).mean()
    return atr

def RSI(df, window, buy_threshold, sell_threshold):
    rsi = pd.DataFrame()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi['RSI'] = 100 - (100 / (1 + rs))
    rsi['BUY'] = buy_threshold
    rsi['SELL'] = sell_threshold
    return rsi

atr_window = 14
atr = ATR(df, atr_window)

rsi_window = 14
rsi_buy_threshold = 30
rsi_sell_threshold = 70
rsi = RSI(df, rsi_window, rsi_buy_threshold, rsi_sell_threshold)

plots = [
    mpf.make_addplot((atr['ATR']), color='purple', ylabel=f'ATR ({atr_window})', secondary_y=False, panel=2),
    mpf.make_addplot((rsi['RSI']), color='#ff8800', ylabel=f'RSI ({rsi_window}, {rsi_buy_threshold}, {rsi_sell_threshold})', secondary_y=False, panel=3),
    mpf.make_addplot((rsi['BUY']), color='green', secondary_y=False, panel=3),
    mpf.make_addplot((rsi['SELL']), color='red', secondary_y=False, panel=3),
]

mpf.available_styles()
#gui for backend 
mpf.plot(
    data=df,
    type='candle',
    style='tradingview',
    mav=(5,20),
    volume=True
)

mpf.plot(
    df,
    type='candle',
    style='yahoo',
    mav=(5,20),
    volume=True,
    addplot=plots,
    panel_ratios=(3,3,3,3),
    figscale=2
)