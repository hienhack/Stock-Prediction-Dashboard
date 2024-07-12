from model.LSTMModel import LSTMModel
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

from datetime import datetime

def load_data():
    # Load the data, the data includes the following columns: Open, High, Low, Close, Adj Close, Volume 
    # respectively according to the order
    df = pdr.get_data_yahoo('AAPL', start='2012-01-01', end=datetime.now())
    return df

# Add technical indicators to the dataset
def addROC(df):
    df['ROC'] = ((df['Close'] - df['Close'].shift(12)) / (df['Close'].shift(12))) * 100
    return df

# Add RSI to the dataset
def addRSI(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def test():
    df = load_data()
    features = ['Open', 'High', 'Low', 'Close']
    model = LSTMModel('AAPL')
    model.train(df, features)
    model.save("./trained")

    # get last 60 days data
    dataToPredict = df[-60:]
    
    prediction = model.predict(dataToPredict)
    print("Prediction:", prediction)

def test_from_load():
    df = load_data()
    model = LSTMModel('AAPL')
    model.load("./trained")
    prediction = model.predict(df[-70:])
    print("Prediction:", prediction)

    plot_data = df[['Open', 'High', 'Low', 'Close']]
    train = plot_data[:-10]
    valid = plot_data[-10:]

    print(prediction.shape)

    for index, col in enumerate(plot_data.columns):
        valid['Prediction'] = prediction[:,index]
        plt.figure(figsize=(16,6))
        plt.title(col)
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price USD ($)', fontsize=18)
        plt.plot(train[col])
        plt.plot(valid[[col, 'Prediction']])
        plt.legend(['Train', 'Valid', 'Prediction'], loc='lower right')
        plt.show()
    

if __name__ == '__main__':
    test();