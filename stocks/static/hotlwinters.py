import yfinance as yf
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def get_holt_winters_prediction(ticker):
    # Fetch historical stock price data
    data = yf.download(ticker, period='1y', interval='1d')

    # Convert the data to a time series format
    time_series = pd.Series(data['Close'])

    # Specify a frequency for the time series data
    time_series.index = pd.DatetimeIndex(time_series.index).to_period('D')

    # Split the data into training and testing sets
    train_data = time_series[:-1]  # Use all but the last day for training
    test_data = time_series[-1:]  # Use the last day for testing

    # Adjust seasonal period based on the length of the training data
    seasonal_period = min(30, len(train_data)-1)

    # Apply the Holt-Winters Method
    model = ExponentialSmoothing(train_data, trend='add', seasonal='add', seasonal_periods=seasonal_period)
    fitted_model = model.fit()

    # Forecast the next value
    forecast = fitted_model.forecast(steps=1)
    return forecast[0]

# Example usage
'''ticker = 'AAPL'
prediction = get_holt_winters_prediction(ticker)

print(f"Predicted price for {ticker} today: {prediction}")'''