from isyatirimhisse import StockData
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def calculate_drawdown(symbol, start_date, exchange='0', return_type='2'):
    stock_data = StockData()
    df = stock_data.get_data(
        symbols=symbol,
        start_date=start_date,
        exchange=exchange,
        return_type=return_type
    )[['DATE', 'CLOSING_TL']]

    df = df.rename(columns={'CLOSING_TL': 'RETURN'})
    df['DATE'] = pd.to_datetime(df['DATE'])

    df['Cumulative Returns'] = (1 + df['RETURN']).cumprod()
    df['Maximum Peak'] = df['Cumulative Returns'].cummax()
    df['Drawdown'] = df['Cumulative Returns'] / df['Maximum Peak'] - 1

    df.to_excel(f'{symbol}_drawdown.xlsx', index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(df['DATE'], df['Drawdown'], linewidth=2, color='red', alpha=0.7, label='Drawdown')
    plt.fill_between(df['DATE'], df['Drawdown'], where=df['Drawdown'] < 0, color='red', alpha=0.3)
    max_drawdown = df['Drawdown'].min()
    plt.axhline(y=max_drawdown, color='black', linestyle='--', label=f'Max Drawdown: {abs(max_drawdown):.2%}')
    plt.title(f'{symbol} Stock Drawdown Chart')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

symbol = 'TUPRS'
calculate_drawdown(symbol, start_date='23-01-2023')