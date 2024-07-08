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
    df = pdr.get_data_yahoo('AAPL', start='2012-01-01', end=datetime.now())
    dataset = df.values
    return df, dataset

def test():
    df, dataset = load_data()
    model = LSTMModel('AAPL')
    model.train(dataset, ['Open', 'High', 'Low', 'Close'])
    model.save("./trained")

    # get the last 60 days data
    data = dataset[-60:, :]
    prediction = model.predict(dataset[-60:, :])
    print("Prediction:", prediction)

def test_from_load():
    df, dataset = load_data()
    model = LSTMModel('AAPL')
    model.load("./trained")
    prediction = model.predict(dataset[-70:, :])

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
    # test()
    test_from_load()