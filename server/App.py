from flask import Flask
from flask import request, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room
import socket

import pandas as pd
from model.LSTMModel import LSTMModel
from model.RNNModel import RNNModel
from model.XgboostModel import XGBoostModel
import os
import requests
import datetime

app = Flask(__name__)
app.secret_key = "secret_key"

model_name = "lstm"
model_features = []
model_symbol = ""
model = None

def find_model(symbol, features):
    """
    Find and load the model for the given symbol and features.
    Example: find_model('BTC', ['Close', 'ROC', 'MA'])
    """
    method_classes = {
        "LSTM": LSTMModel,
        "RNN": RNNModel,
        "XGBoost": XGBoostModel
    }

    for method, model_class in method_classes.items():
        model_name = f"{symbol}-{method}_{'_'.join(features)}"
        model_path = os.path.join("./trained", model_name)
        if os.path.exists(model_path):
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
    

@app.route('/change-model', methods=['POST'])
def change_model():
    global model_name, model_symbol, model_features, model
    data = request.json
    model_name = data.get('model')
    model_symbol = data.get('symbol')
    model_features = data.get('features')
    
    model = find_model(model_symbol, model_features)
    if model:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Model not found"}), 400

@app.route('/current-model')
def get_current_model():
    return jsonify({
        "model": model_name,
        "symbol": model_symbol,
        "features": model_features
    })

@app.route('/prediction')   
def get_prediction():
    global model, model_symbol

    # Fetch data from Binance
    data = fetch_binance_data(symbol=model_symbol)
    if data is None:
        return jsonify({"status": "error", "message": "Failed to fetch Binance data"}), 500

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['t', 'o', 'h', 'l', 'c', 'v', 'T', 'q', 'n', 'V', 'Q', 'B'])
    df = df[['t', 'o', 'h', 'l', 'c']]
    df['t'] = pd.to_datetime(df['t'], unit='ms')

    if model:
        # Ensure column names match the expected names used in the model prediction
        df.rename(columns={'t': 'Datetime'}, inplace=True)
        df.rename(columns={'o': 'Open'}, inplace=True)
        df.rename(columns={'h': 'High'}, inplace=True)
        df.rename(columns={'l': 'Low'}, inplace=True)
        df.rename(columns={'c': 'Close'}, inplace=True)
        
            
        predictions = model.predict(df[['Datetime','Open','High','Low', 'Close']])
        return predictions
    else:
        return jsonify({"status": "error", "message": "No model loaded"}), 400

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
if not os.path.exists("./trained"):
    os.makedirs("./trained")
    
# Load initial model if any
model = find_model(model_symbol, model_features)
