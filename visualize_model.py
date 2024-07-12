from model.LSTMModel import LSTMModel
from model.RNNModel import RNNModel
from model.XgboostModel import XGBoostModel
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

import os
from datetime import datetime

def load_data():
    df = yf.download('BTC-USD', start='2012-01-01', end=datetime.now())
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
    df = addROC(df)
    df = addRSI(df)
    df = addMovingAverage(df)
    df = df.dropna()
    return df

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

if __name__ == '__main__':
    stock = 'BTC'
    visualize_model(stock,XGBoostModel , ['Close', 'ROC', 'RSI', 'Moving Average'])
