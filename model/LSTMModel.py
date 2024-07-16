from .ModelBase import ModelBase
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout
import joblib
import numpy as np
from datetime import datetime
import os

class LSTMModel(ModelBase):
    def __init__(self, stockName):
        super().__init__()
        self.T = 60
        self.stockName = stockName
        self.method = "LSTM"
        self.name = None
        self.x_scaler = None
        self.y_scaler = None
    
    def train(self, data, features):
        self.features = features

        self.name = f"{self.stockName}-{self.method}_{'_'.join(features)}"

        # data includes the following columns: Open, High, Low, Close, Adj Close, Volume respectively according to the order
        
        # Keep only the features that we want to use
        dataset = data[features].values

        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

        x_scaled_data = self.x_scaler.fit_transform(dataset)

        # We will predict the next day's Open, High, Low, Close prices
        # Open, High, Low, Close prices are always in the first 4 columns
        y_scaled_data = self.y_scaler.fit_transform(data.values[:, :4])
        
        x_train = []
        # y_train includes the following columns: Open, High, Low, Close according to the order
        y_train = []
        
        for i in range(self.T, len(dataset)):
            x_train.append(x_scaled_data[i-self.T:i, :])
            y_train.append(y_scaled_data[i,:])

        x_train, y_train = np.array(x_train), np.array(y_train)
        
        self.model = self.__create_model(x_train)
        self.model.fit(x_train, y_train, epochs=10, batch_size=32)
    
    def load(self, path):
        self.model = load_model(os.path.join(path, "model.h5"))
        self.x_scaler = joblib.load(os.path.join(path, "x_scaler.save"))
        self.y_scaler = joblib.load(os.path.join(path, "y_scaler.save"))
        with open(os.path.join(path, "features.txt"), "r") as f:
            self.features = f.read().split(",")
        print("Model and scaler loaded from", path)
    
    def save(self, base_path):
        path = os.path.join(base_path, self.name)
        os.makedirs(path, exist_ok=True)
        self.model.save(os.path.join(path, "model.h5"))
        joblib.dump(self.x_scaler, os.path.join(path, "x_scaler.save"))
        joblib.dump(self.y_scaler, os.path.join(path, "y_scaler.save"))
        with open(os.path.join(path, "features.txt"), "w") as f:
            f.write(",".join(self.features))
        print(f"Model and scaler saved to {path}")

    def predict(self, dataToPredict):
        dataset = dataToPredict[self.features].values
        x_test = []
        x_scaled_data = self.x_scaler.transform(dataset)
        for i in range(self.T, len(dataset) + 1):
            x_test.append(x_scaled_data[i-self.T:i, :])
        x_test = np.array(x_test)

        prediction = self.model.predict(x_test)
        prediction = self.y_scaler.inverse_transform(prediction)
        return prediction

    def __create_model(self, x_train):
        model = Sequential()
        model.add(LSTM(units=128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=64, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=64, return_sequences=False))
        model.add(Dense(units=4))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model