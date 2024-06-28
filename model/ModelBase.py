from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = None
    
    @abstractmethod
    def train(self, dataset, features):
        """
        Train prediction model
        Dataset: dataset
        Traning features: features
        """
        pass

    @abstractmethod
    def load(self, modelPath):
        """
        Load saved model
        """
        pass
    
    @abstractmethod
    def save(sefl, path):
        """
        Save model
        """
        pass


    @abstractmethod
    def predict(self, dataToPredict):
        """
        Predict candle price
        """
        pass
    