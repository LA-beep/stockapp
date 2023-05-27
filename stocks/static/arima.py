import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def get_arima_prediction(ticker):
    # Fetch historical stock price data
    data = yf.download(ticker, period='1y', interval='1d')

    # Convert the data to a time series format
    time_series = pd.Series(data['Close'])

    # Specify a frequency for the time series data
    time_series.index = pd.DatetimeIndex(time_series.index).to_period('D')

    # Split the data into training and testing sets
    train_data = time_series[:-1]  # Use all but the last day for training
    test_data = time_series[-1:]  # Use the last day for testing

    # Apply the ARIMA model
    model = ARIMA(train_data, order=(1, 1, 1))
    fitted_model = model.fit()

    # Forecast the next value
    forecast = fitted_model.forecast(steps=1)
    return forecast[0]

# Example usage
'''ticker = 'AAPL'
prediction = get_arima_prediction(ticker)

print(f"Predicted price for {ticker} today: {prediction}")
'''