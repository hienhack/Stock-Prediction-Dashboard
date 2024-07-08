from .ModelBase import ModelBase
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout
import joblib
import numpy as np
from datetime import datetime

class LSTMModel(ModelBase):
    def __init__(self, stockName):
        super().__init__()
        self.T = 60
        self.name = "LSTM_" + stockName + "_" + str(datetime.now().date());
        self.x_scaler = None
        self.y_scaler = None
    
    def train(self, dataset, features):
        # dataset includes the following columns: Open, High, Low, Close, Adj Close, Volume according to the order
        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

        x_scaled_data = self.x_scaler.fit_transform(dataset)
        y_scaled_data = self.y_scaler.fit_transform(dataset[:,0:4])
        
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
        # Load the model
        self.model = load_model(path + "/model.h5")
        # Load the scaler
        self.x_scaler = joblib.load(path + "/x_scaler.save")
        self.y_scaler = joblib.load(path + "/y_scaler.save")
        print("Model and scaler loaded from", path)
    
    def save(self, path):
        # Save the model
        self.model.save(path + "/model.h5")
        # Save the scaler
        joblib.dump(self.x_scaler, path + "/x_scaler.save")
        joblib.dump(self.y_scaler, path + "/y_scaler.save")
        print(f"Model and scaler saved to {path}")

    def predict(self, dataToPredict):
        x_test = []
        x_scaled_data = self.x_scaler.transform(dataToPredict)
        for i in range(self.T, len(dataToPredict)):
            x_test.append(x_scaled_data[i-self.T:i])
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