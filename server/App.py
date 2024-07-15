from flask import Flask
from flask import request, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room
import socket

import pandas as pd
from AppSocket import subscribe, unsubscribe
from model.LSTMModel import LSTMModel
from model.RNNModel import RNNModel
from model.XgboostModel import XGBoostModel
import os

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

    end = int(request.args.get('end'))
    limit = int(request.args.get('limit'))

    # Read historical data from CSV
    try:
        df = pd.read_csv(f'{model_symbol}.csv')
    except FileNotFoundError:
        return jsonify({"status": "error", "message": f"No data found for {model_symbol}"}), 404

    # Assuming YourModelClass has a predict method
    if model:
        try:
            # Prepare data for prediction
            data_to_predict = df.iloc[-limit:]  # Get the last 'limit' rows
            predictions = model.predict(data_to_predict)

            # Format predictions as required ([[t, o, h, l, c], [t, o, h, l, c], ...])
            prediction_list = []
            for prediction in predictions:
                prediction_list.append([prediction['t'], prediction['o'], prediction['h'], prediction['l'], prediction['c']])

            return jsonify(prediction_list)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
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
