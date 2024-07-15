from flask import Flask
from flask import request, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room
import socket
from AppSocket import subscribe, unsubscribe

# from model.LSTMModel import LSTMModel
# from model.RNNModel import RNNModel
# from model.XgboostModel import XGBoostModel
# import os

app = Flask(__name__)
app.secret_key = "secret_key"

# def find_model(symbol, features):
#     """
#     Find and load the model for the given symbol and features.
#     Example: find_model('BTC', ['Close', 'ROC', 'Moving Average'])
#     """
#     method_classes = {
#         "LSTM": LSTMModel,
#         "RNN": RNNModel,
#         "XGBoost": XGBoostModel
#     }

#     for method, model_class in method_classes.items():
#         model_name = f"{symbol}-{method}_{'_'.join(features)}"
#         model_path = os.path.join("./trained", model_name)
#         if os.path.exists(model_path):
#             model = model_class(symbol)
#             try:
#                 model.load(model_path)
#                 return model
#             except Exception as e:
#                 print(f"Failed to load model {model_name}: {e}")
#                 return None

#     print(f"No model found for symbol {symbol} with features {features}")
#     return None

# # Khởi tạo model là btcusdt lstm close roc
# model = None

# @app.route('/change-model', methods=['POST'])
# def change_model():
#     '''
#     request body: {
#         model: "LSTM",
#         symbol: "BTCUSDT",
#         features: ["Close", "Roc"]
#         # return 400 if not round
#     }
#     '''
#     # global model = find_model('')
#     pass

@app.route('/current-model')
def get_current_model():
    '''
    return json object:
        {
            model: "LSTM",
            symbol: "BTCUSDT",
            features: ['Close', 'ROC']
        }
    '''
    pass

@app.route('/prediction')
def get_prediction():
    '''
    request url format: /prediction?end=17800212321&limit=10
    
    end: the last time point of the prediciction
    limit: number of time points

    return 
    [[t, o, h, l, c], [t, o, h, l, c], .....]                       (*)


    lấy dữ liệu từ python binance, hoặc yfinance, interval 5m, chú ý đự đoán đúng thời gian, mốc thời gian
    vì ở front e t lấy mốc là 5m, nó trả về 15:00, 15:05,...
    ví dụ điểm thời gian cuối cùng (end) khi đã convert là 15:05 thì phần tử cuối cùng của (*) phải có t = 15:05 (dạng timestamp)
    dùng: global model   để dự đoán
    có thể lưu lại dữ liệu rồi load thêm các mốc mới để tiết kiệm thời gian
    '''
    pass

@app.route('/')
def home():
    return render_template('index.html')

# Route mẫu, call API body: {"tweet": "I am happy"}
@app.route('/analyze', methods=['POST'])
def analyze():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.get_json()
        print(obj["tweet"])
        return "tweet received"
    else:
        return 'Content-Type not supported!n'
    
# python main.py to run