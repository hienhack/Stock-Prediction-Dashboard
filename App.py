from model.LSTMModel import LSTMModel

def test():
    model = LSTMModel()
    model.train("dataset", "features")

if __name__ == '__main__':
    test()