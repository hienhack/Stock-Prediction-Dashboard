from model.LSTMModel import LSTMModel
from model.RNNModel import RNNModel
from model.XgboostModel import XGBoostModel
import yfinance as yf
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

yf.pdr_override()

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

def load_data():
    # Tải dữ liệu với khoảng thời gian 5 phút trong 1 tháng gần nhất
    df = yf.download(tickers='BTC-USD', period='1mo', interval='5m')
    return df

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
    df['Moving Average'] = df['Close'].rolling(window=14).mean()
    return df

def prepare_data():
    df = load_data()
    if df.empty:
        raise ValueError("No data found. Please check the period and interval values.")
    df = addROC(df)
    df = addRSI(df)
    df = addMovingAverage(df)
    df = df.dropna()
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
        plt.figure(figsize=(16, 6))
        plt.title(col)
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price USD ($)', fontsize=18)
        plt.plot(train[col])
        plt.plot(valid[[col, f'{col}_Prediction']])
        plt.legend(['Train', 'Valid', 'Prediction'], loc='lower right')
        plt.show()

def visualize_model(stock, model_class, features):
    df = prepare_data()
    model = model_class(stock)
    model_name = f"{stock}-{model_class.__name__.replace('Model', '')}_{'_'.join(features)}"
    model_path = os.path.join("./trained", model_name)
    model.load(model_path)
    plot_prediction(df, model, features)

def main():
    df = prepare_data()
    stock = 'BTCUSDT'

    # Sử dụng 3000 cột dữ liệu gần nhất để huấn luyện
    if len(df) > 3000:
        df = df[-3000:]

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
        train_and_save_model(df, LSTMModel, stock, features)
        # train_and_save_model(df, LSTMModel, stock, features)

if __name__ == '__main__':
    # stock = 'BTCUSDT'
    # visualize_model(stock,RNNModel , ['Close', 'ROC'])
    main()
