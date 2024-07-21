from .ModelBase import ModelBase
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os
import numpy as np

class RNNModel(ModelBase):
    def __init__(self, stockName):
        super().__init__()
        self.T = 60
        self.stockName = stockName
        self.method = "RNN"
        self.name = None
        self.x_scaler = None
        self.y_scaler = None
    
    def train(self, data, features):
        self.features = features
        self.name = f"{self.stockName}-{self.method}_{'_'.join(features)}"
        dataset = data[features].values 

        self.x_scaler = MinMaxScaler()
        self.y_scaler = MinMaxScaler()

        x_scaled_data = self.x_scaler.fit_transform(dataset)
        y_scaled_data = self.y_scaler.fit_transform(data[['Open', 'High', 'Low', 'Close']].values)
        
        x_train = []
        y_train = []
        
        for i in range(self.T, len(dataset)):
            x_train.append(x_scaled_data[i-self.T:i, :])
            y_train.append(y_scaled_data[i, :])

        x_train, y_train = np.array(x_train), np.array(y_train)
        
        self.model = self.__create_model(x_train.shape[1:])
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        self.model.fit(x_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

    def load(self, path):
        self.model = load_model(os.path.join(path, "model.h5"))
        self.x_scaler = joblib.load(os.path.join(path, "x_scaler.joblib"))
        self.y_scaler = joblib.load(os.path.join(path, "y_scaler.joblib"))
        with open(os.path.join(path, "features.txt"), "r") as f:
            self.features = f.read().split(",")
        print("Model and scaler loaded from", path)
    
    def save(self, base_path):
        path = os.path.join(base_path, self.name)
        os.makedirs(path, exist_ok=True)
        self.model.save(os.path.join(path, "model.h5"))
        joblib.dump(self.x_scaler, os.path.join(path, "x_scaler.joblib"))
        joblib.dump(self.y_scaler, os.path.join(path, "y_scaler.joblib"))
        with open(os.path.join(path, "features.txt"), "w") as f:
            f.write(",".join(self.features))
        print(f"Model and scaler saved to {path}")

    def predict(self, dataToPredict):
        dataset = dataToPredict[self.features].values
        x_test = []
        x_scaled_data = self.x_scaler.transform(dataset)
        for i in range(self.T, len(dataset)):
            x_test.append(x_scaled_data[i-self.T:i, :])
        x_test = np.array(x_test)

        prediction = self.model.predict(x_test)
        prediction = self.y_scaler.inverse_transform(prediction)
        return prediction

    def __create_model(self, input_shape):
        model = Sequential()
        model.add(SimpleRNN(100, return_sequences=True, input_shape=input_shape))
        model.add(SimpleRNN(100, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(50))
        model.add(Dense(4))

        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
