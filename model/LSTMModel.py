from .ModelBase import ModelBase

class LSTMModel(ModelBase):
    def __init__(self):
        super().__init__()
    
    def train(self, dataset, features):
        print("Training LSTM model")
    
    def load(self, modelPath):
        pass
    
    def save(self, path):
        pass

    def predict(self, dataToPredict):
        pass