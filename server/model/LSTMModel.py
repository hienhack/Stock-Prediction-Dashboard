from .ModelBase import ModelBase
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout
import joblib
import numpy as np
from datetime import datetime
import os

class LSTMModel(ModelBase):
    def __init__(self, symbol):
        super().__init__()
        self.T = 60
        self.name = symbol + "-" + "LSTM_";
        self.x_scaler = None
        self.y_scaler = None
    
    def train(self, df, features):
        self.features = features

        x_scaled_data = self.x_scaler.fit_transform(df[features].values)
        y_scaled_data = self.y_scaler.fit_transform(df[:, :4].values)
        
        x_train = []
        y_train = []
        
        for i in range(self.T, len(df)):
            x_train.append(x_scaled_data[i-self.T:i])
            y_train.append(y_scaled_data[i])

        x_train, y_train = np.array(x_train), np.array(y_train)
        
        self.model = self.__create_model(x_train)
        self.model.fit(x_train, y_train, epochs=100, batch_size=32)
    
    def load(self, path):
        # Load the model
        self.model = load_model(path + "/model.h5")
        # Load the scaler
        self.x_scaler = joblib.load(path + "/x_scaler.save")
        self.y_scaler = joblib.load(path + "/y_scaler.save")
        # Load the features
        with open(path + "/features.txt", "r") as f:
            self.features = f.read().split(",")
        print("Model and scaler loaded from", path)
    
    def save(self, base_path):
        # Save the model
        model_name = self.name + self.features.join("_");
        path = os.path.join(base_path, model_name)
        os.makedirs(path, exist_ok=True)
        self.model.save(os.path.join(path, "model.h5"))
        # Save the scaler
        joblib.dump(self.x_scaler, os.path.join(path, "/x_scaler.save"))
        joblib.dump(self.y_scaler, os.path.join(path, "/y_scaler.save"))
        # Save the features
        with open(os.path.join(path, "/features.txt"), "w") as f:
            f.write(",".join(self.features))
        print(f"Model and scaler saved to {path}")

    def predict(self, df):
        x_test = []
        x_scaled_data = self.x_scaler.transform(df[self.features].values)
        for i in range(self.T, len(df)  + 1):
            x_test.append(x_scaled_data[i-self.T:i])
        x_test = np.array(x_test)

        prediction = self.model.predict(x_test)
        prediction = self.y_scaler.inverse_transform(prediction)
        return prediction

    def __create_model(self, x_train):
        model = Sequential()
        model.add(LSTM(units=128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=64, return_sequences=False))
        model.add(Dense(units=4))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model