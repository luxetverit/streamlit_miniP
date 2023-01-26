import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO

def get_stock_info(maket_type=None):
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    if maket_type == 'kospi':         
        marketType = "stockMkt"      
    elif maket_type == 'kosdaq':
        marketType = "kosdaqMkt"    
    elif maket_type == None:         
        marketType = ""
    url = "{0}?method={1}&marketType={2}".format(base_url, method, marketType)     
    df = pd.read_html(url, header=0)[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name, maket_type):     
    df = get_stock_info(maket_type)
    code = df[df['회사명']==company_name]['종목코드'].values    
    code = code[0]
    if maket_type == 'kospi':   
        ticker_symbol = code +".KS"     
    elif maket_type == 'kosdaq':      
        ticker_symbol = code +".KQ" 
    return ticker_symbol

st.title('반도체 주식 데이터 Dashboard')
# tickers =('TSLA','AAPL','MSFT','BTC-USD','ETH-USD','005930.KS')
tickers ={
  'SK hynix':'000660.KS',
  'Samsung Electronics':'005930.KS',
  'NVIDIA Corporation' :'NVDA',
  'QUALCOMM':'QCOM'
}
reversed_ticker = dict(map(reversed,tickers.items()))
dropdown = st.multiselect('select',tickers.keys())
start = st.date_input('Start', value=pd.to_datetime('2019-01-01'))
end = st.date_input('End',value=pd.to_datetime('today'))
if len(dropdown) > 0:
  for i in dropdown:
    df = yf.download(tickers[i],start,end)['Adj Close']
    st.title(reversed_ticker[tickers[i]])
    st.line_chart(df)