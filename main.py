# -----------------------------------------------------------------------------------
# import relevant libraries
import streamlit as st
from datetime import datetime
import yfinance as yf
import pandas as pd
from web_scraping import stock_scrap
import numpy as np
from prophet import Prophet
# -----------------------------------------------------------------------------------
# Streamlit Application
START = '2020-01-01'
current = datetime.today().strftime('%Y-%m-%d')

st.text("Money (That's What I Want)")
st.audio("Money (That's What I Want).mp3",format='audio/mp3', loop=True)
st.title('Stock Market Trend Analysis 2024')
st.write('Welcome to the Stock Market Trend App. This platform is intended for educational purposes only, focusing on Web Scraping and Prophet. Please refrain from using it as financial advice.')
stocks = stock_scrap()
selected_stock = st.selectbox('Stock to analyse', stocks)

def get_data(name):
    data = yf.download(name, START, current)
    return data

load_text = st.text('Loading Data...')
show_data = get_data(selected_stock)
load_text.text('Data extracted sucessfully.')

st.write("Dataset of the Stock (Recent 7 Days)")
st.dataframe(show_data.tail(7))

show_data['Move_Avg (50D)'] = show_data['Close'].rolling(50).mean()
show_data['Move_Avg (200D)'] = show_data['Close'].rolling(200).mean()

# -----------------------------------------------------------------------------------
# Prepare the data for Prophet  
prophet_data = show_data.reset_index()[['Date', 'Close']]
prophet_data.columns = ['ds', 'y']  

# Fit the model  
m = Prophet()
m.fit(prophet_data)

future = m.make_future_dataframe(periods=180)  
forecast = m.predict(future)
 
forecast_combined = forecast[['ds', 'yhat']].tail(180)    
forecast_combined.columns = ['Date', 'Price Prediction (180D)']

combined_data = pd.merge(show_data.reset_index(), forecast_combined, on='Date', how='outer')

plot_data = combined_data[['Date', 'Close', 'Move_Avg (50D)', 'Move_Avg (200D)', 'Price Prediction (180D)']]
plot_data.set_index('Date', inplace=True)

st.write('Closing Price Line Chart')
st.line_chart(plot_data, x_label = 'Date', y_label = 'Closing Price')

# -----------------------------------------------------------------------------------
# Card visuals
def calculate_price_difference(stock_data):
    latest_price = stock_data.iloc[-1]["Close"]
    last_year_price = stock_data.iloc[-365]["Close"]
    price_diff = latest_price - last_year_price
    percent_diff = (price_diff / last_year_price) * 100
    return price_diff, percent_diff

def predicted_difference(latest_close_price, pred_180D):
    return ((pred_180D - latest_close_price) / latest_close_price) * 100

latest_close_price = show_data.iloc[-1]["Close"]
latest_50D = show_data.iloc[-1]['Move_Avg (50D)']
latest_200D = show_data.iloc[-1]['Move_Avg (200D)']
price_difference, percentage_difference = calculate_price_difference(show_data)
pred_180D = plot_data.iloc[-1]['Price Prediction (180D)']
predict_percent = predicted_difference(latest_close_price, pred_180D)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Close Price", f"${latest_close_price:.2f}")
with col2:
    st.metric("Price Difference (YoY)", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
with col3:
    st.metric("Move Avg (50D)", f"${latest_50D:.2f}")
with col4:
    st.metric("Move Avg (200D)", f"${latest_200D:.2f}")
with col5:
    st.metric('Prediction (180D)', f"${pred_180D:.2f}", f"{predict_percent:+.2f}%")

# -----------------------------------------------------------------------------------
# Volume Line Chart
st.write('Volume Line Chart')
st.line_chart(show_data.Volume, x_label= 'Date', y_label='Volume')
# -----------------------------------------------------------------------------------
