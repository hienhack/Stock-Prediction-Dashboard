from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = None
        self.name = None
    
    @abstractmethod
    def train(self, dataset, features):
        """
        Train prediction model
        Dataset: dataset
        Training features: features
        """
        pass

    @abstractmethod
    def load(self, modelPath):
        """
        Load saved model
        """
        pass
    
    @abstractmethod
    def save(self, path):
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
