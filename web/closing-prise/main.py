import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

symbol = st.sidebar.text_input('Hisse Senedi Sembolü', value='XU100')
st.title( symbol + ' Hisse Senedi Grafiği')
start_date = st.sidebar.date_input('Başlangıç Tarihi', value=datetime(2023, 1, 1))
end_date = st.sidebar.date_input('Bitiş Tarihi', value=datetime.now())

df = yf.download(symbol + '.IS', start=start_date, end=end_date)

st.subheader('Hisse Senedi Fiyatları')
st.line_chart(df['Close'])

st.subheader(symbol + ' Hisse Senedi Verileri')
st.write(df)

for i in range(1,250):
    ema = df['Close'][-i:]
    Sum = sum(ema)/len(ema)
    #dfsum = pd.DataFrame(Sum)
    #st.line_chart(dfsum)
    st.subheader(symbol + ' ' + str(i) + ' Gün Kapanış Ortalaması')
    st.write(round(Sum,2))