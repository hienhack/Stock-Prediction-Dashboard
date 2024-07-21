from model.RNNModel import RNNModel
from model.LSTMModel import LSTMModel
from model.XgboostModel import XGBoostModel
import os
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

def fetch_binance_data(symbol="BTCUSDT", interval="5m", start_time=None, end_time=None, limit=1000):
    url = f"https://api.binance.us/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    if start_time:
        params["startTime"] = int(start_time.timestamp() * 1000)
    if end_time:
        params["endTime"] = int(end_time.timestamp() * 1000)
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def addROC(df):
    df['ROC'] = ((df['Close'] - df['Close'].shift(12)) / (df['Close'].shift(12))) * 100
    return df

def addRSI(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def addMovingAverage(df):
    df['Moving Average'] = df['Close'].rolling(window=60).mean()
    return df

def prepare_data_from_binance(symbol):
    # Fetch historical data from Binance for the last 1 month with 5m interval
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    data = []
    while start_time < end_time:
        print(f"Fetching data from {start_time} to {end_time} for {symbol}...")
        new_data = fetch_binance_data(symbol=symbol, interval="5m", start_time=start_time, end_time=end_time, limit=1000)
        if not new_data:
            print("No new data fetched. Exiting loop.")
            break
        data.extend(new_data)
        print(f"Fetched {len(new_data)} rows.")
        last_timestamp = new_data[-1][0]
        start_time = datetime.fromtimestamp(last_timestamp / 1000) + timedelta(minutes=5)  # Update start_time to fetch next batch
    
    if not data:
        raise ValueError(f"No data found from Binance for {symbol}")
    
    df = pd.DataFrame(data, columns=['t', 'o', 'h', 'l', 'c', 'v', 'T', 'q', 'n', 'V', 'Q', 'B'])
    df = df[['t', 'o', 'h', 'l', 'c']]
    df.set_index('t', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms', utc=True)  # Convert to datetime
    df.rename(columns={'t': 'Datetime'}, inplace=True)
    df.rename(columns={'o': 'Open'}, inplace=True)
    df.rename(columns={'h': 'High'}, inplace=True)
    df.rename(columns={'l': 'Low'}, inplace=True)
    df.rename(columns={'c': 'Close'}, inplace=True)

    # Convert all columns to numeric and handle errors
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()

    df = addROC(df)
    df = addRSI(df)
    df = addMovingAverage(df)
    df = df.dropna()
    
    # Print the DataFrame to check the data
    print(df.head(10))  # Print first 10 rows of the DataFrame
    print(df.describe())  # Print summary statistics of the DataFrame
    
    return df

def train_and_save_model(df, model_class, stock, features, base_path="./trained"):
    model = model_class(stock)
    model.train(df, features)
    model.save(base_path)

def plot_prediction(df, model, features):
    dataToPredict = df[-70:]
    prediction = model.predict(dataToPredict)
    plot_data = df[['Open', 'High', 'Low', 'Close']]
    train = plot_data[:-10]
    valid = plot_data[-10:].copy()

    for index, col in enumerate(plot_data.columns):
        valid[f'{col}_Prediction'] = prediction[-10:, index]

        # Tính toán các độ đo
        mae = mean_absolute_error(valid[col], valid[f'{col}_Prediction'])
        mse = mean_squared_error(valid[col], valid[f'{col}_Prediction'])
        rmse = np.sqrt(mse)
        r2 = r2_score(valid[col], valid[f'{col}_Prediction'])

        plt.figure(figsize=(16, 6))
        plt.title(f"{col} - MAE: {mae:.4f}, MSE: {mse:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price USD ($)', fontsize=18)
        plt.plot(train[col])
        plt.plot(valid[[col, f'{col}_Prediction']])
        plt.legend(['Train', 'Valid', 'Prediction'], loc='lower right')
        plt.show()

        print(f"{col} - MAE: {mae:.4f}, MSE: {mse:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

def visualize_model(symbol, stock, model_class, features):
    df = prepare_data_from_binance(symbol)
    model = model_class(stock)
    model_name = f"{stock}-{model_class.__name__.replace('Model', '')}_{'_'.join(features)}"
    model_path = os.path.join("./trained", model_name)
    model.load(model_path)
    plot_prediction(df, model, features)

def main():
    symbols = ["BTCUSDT", "ADAUSDT", "ETHUSDT"]
    for symbol in symbols:
        df = prepare_data_from_binance(symbol)
        stock = symbol

        # Sử dụng 3000 cột dữ liệu gần nhất để huấn luyện
        if len(df) > 6000:
            df = df[-6000:]

        feature_sets = [
            ['Close'],
            ['ROC'],
            ['RSI'],
            ['Moving Average'],
            ['Close', 'ROC'],
            ['Close', 'RSI'],
            ['Close', 'Moving Average'],
            ['ROC', 'RSI'],
            ['ROC', 'Moving Average'],
            ['RSI', 'Moving Average'],
            ['Close', 'ROC', 'RSI'],
            ['Close', 'ROC', 'Moving Average'],
            ['ROC', 'RSI', 'Moving Average'],
            ['Close', 'ROC', 'RSI', 'Moving Average']
        ]

        for features in feature_sets:
            train_and_save_model(df, RNNModel , stock, features)
            train_and_save_model(df, LSTMModel, stock, features)
            train_and_save_model(df, XGBoostModel, stock, features)

if __name__ == '__main__':
    main()
