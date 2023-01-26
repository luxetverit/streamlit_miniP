import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO

st.title('주식 정보 웹 앱')

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

df = get_stock_info('kospi')
df

stock_name = st.sidebar.text_input("회사이름과 기간 입력", "NAVER")

ticker_symbol = get_ticker_symbol(stock_name, "kospi")  
ticker_data = yf.Ticker(ticker_symbol)

start = st.date_input('Start', value=pd.to_datetime('2019-01-01'))
end = st.date_input('End',value=pd.to_datetime('today'))

df = ticker_data.history(start=start, end=end)
df.index = df.index.date
st.subheader(f"[{stock_name}] 주가 데이터")
st.dataframe(df.head())

st.line_chart(df['Close'])