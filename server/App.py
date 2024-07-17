from flask import Flask
from flask import request, render_template, jsonify
from flask_cors import CORS, cross_origin

import pandas as pd
from model.LSTMModel import LSTMModel
from model.RNNModel import RNNModel
from model.XgboostModel import XGBoostModel
import os
import requests
from datahelper import prepare_data
from itertools import permutations



app = Flask(__name__)
CORS(app)
app.secret_key = "secret_key"

def find_model(symbol, method, features):
    print("--------------------Find model-------------------")
    print(symbol, method, features)
    method_classes = {
        "LSTM": LSTMModel,
        "RNN": RNNModel,
        "XGBoost": XGBoostModel
    }

    model_class = method_classes.get(method)
    if not model_class:
        print(f"No method class found for method: {method}")
        return None

    for perm in permutations(features):
        model_name = f"{symbol}-{method}_{'_'.join(perm)}"
        model_path = os.path.join("../trained", model_name)
        print('Trying model path:', model_path)
        if os.path.exists(model_path):
            print(f"Found model: {model_path}")
            model = model_class(symbol)
            try:
                model.load(model_path)
                return model
            except Exception as e:
                print(f"Failed to load model {model_name}: {e}")
                return None

    print(f"No model found for symbol {symbol} with features {features}")
    return None

def fetch_binance_data(symbol="BTCUSDT", interval="5m", limit=200):
    url = f"https://api.binance.us/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

model_name = "XGBoost"
model_features = ['Close']
model_symbol = "BTCUSDT"
model = find_model(model_symbol, model_name, model_features)
print("Find model ....")

@app.route('/change-model', methods=['POST'])
def change_model():
    global model_name, model_symbol, model_features, model
    data = request.json
    model_name = data.get('method')
    model_symbol = data.get('symbol')
    model_features = data.get('features')
    
    model = find_model(model_symbol, model_name, model_features)
    if model:
        return jsonify({"method": model_name, "symbol": model_symbol, "features": model_features}), 200
    else:
        return jsonify({"status": "error", "message": "Model not found"}), 400

@app.route('/current-model')
def get_current_model():
    return jsonify({
        "method": model_name,
        "symbol": model_symbol,
        "features": model_features
    })

@app.route('/prediction')
def get_prediction():
    global model, model_symbol
    limit = request.args.get('limit')

    if not model:
        return jsonify({"status": "error", "message": "No model loaded"}), 400

    # Fetch data from Binance
    data = fetch_binance_data(symbol=model_symbol)
    if data is None:
        return jsonify({"status": "error", "message": "Failed to fetch Binance data"}), 500

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['t', 'o', 'h', 'l', 'c', 'v', 'T', 'q', 'n', 'V', 'Q', 'B'])
    df = df[['t', 'o', 'h', 'l', 'c']]
    df.set_index('t', inplace=True)

    # Ensure column names match the expected names used in the model prediction
    df.rename(columns={'t': 'Datetime'}, inplace=True)
    df.rename(columns={'o': 'Open'}, inplace=True)
    df.rename(columns={'h': 'High'}, inplace=True)
    df.rename(columns={'l': 'Low'}, inplace=True)
    df.rename(columns={'c': 'Close'}, inplace=True)

    df = prepare_data(df)
    
     # Perform prediction
    predictions = model.predict(df)
    predDate = df.index.tolist()
    predDate.append(predDate[-1] + 300000)

    # get the last limit predictions
    if limit:
        predictions = predictions[-int(limit):]
        predDate = predDate[-int(limit):]
    else:
        predDate = predDate[-len(predictions):]

    result = []
    for i in range(len(predictions)):
        result.append({
            "time": predDate[i] / 1000,
            "open": float(predictions[i][0]),
            "high": float(predictions[i][1]),
            "low": float(predictions[i][2]),
            "close": float(predictions[i][3]),
        })

    return jsonify(result), 200
    
        

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.get_json()
        print(obj["tweet"])
        return "tweet received"
    else:
        return 'Content-Type not supported!'

# Ensure models directory exists
if not os.path.exists("../trained"):
    os.makedirs("../trained")