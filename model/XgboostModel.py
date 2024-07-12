from .ModelBase import ModelBase
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib
import os
import numpy as np

class XGBoostModel(ModelBase):
    def __init__(self, stockName):
        super().__init__()
        self.T = 60
        self.stockName = stockName
        self.method = "XGBoost"
        self.name = None
        self.x_scaler = None
        self.y_scaler = None
        self.model = None
    
    def train(self, data, features):
        self.features = features
        self.name = f"{self.stockName}-{self.method}_{'_'.join(features)}"
        dataset = data[features].values 

        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

        x_scaled_data = self.x_scaler.fit_transform(dataset)
        y_scaled_data = self.y_scaler.fit_transform(data[['Open', 'High', 'Low', 'Close']].values)
        
        x_train = []
        y_train = []
        
        for i in range(self.T, len(dataset)):
            x_train.append(x_scaled_data[i-self.T:i, :])
            y_train.append(y_scaled_data[i, :])

        x_train, y_train = np.array(x_train), np.array(y_train)
        
        # Reshape x_train for XGBoost
        x_train = x_train.reshape(x_train.shape[0], -1)

        self.model = self.__create_model()
        self.model.fit(x_train, y_train)
    
    def load(self, path):
        self.model = XGBRegressor()
        self.model.load_model(os.path.join(path, "model.json"))
        self.x_scaler = joblib.load(os.path.join(path, "x_scaler.joblib"))
        self.y_scaler = joblib.load(os.path.join(path, "y_scaler.joblib"))
        with open(os.path.join(path, "features.txt"), "r") as f:
            self.features = f.read().split(",")
        print("Model and scaler loaded from", path)
    
    def save(self, base_path):
        path = os.path.join(base_path, self.name)
        os.makedirs(path, exist_ok=True)
        self.model.save_model(os.path.join(path, "model.json"))
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

        # Reshape x_test for XGBoost
        x_test = x_test.reshape(x_test.shape[0], -1)

        prediction = self.model.predict(x_test)
        prediction = self.y_scaler.inverse_transform(prediction)
        return prediction

    def __create_model(self):
        model = XGBRegressor(n_estimators=1000, learning_rate=0.01, max_depth=5, subsample=0.8, colsample_bytree=0.8)
        return model
