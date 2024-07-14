from flask import Flask
from flask import request, render_template, jsonify
from flask_socketio import SocketIO, join_room, leave_room
import socket
from AppSocket import subscribe, unsubscribe

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect();

app = Flask(__name__)
app.secret_key = "secret_key"

server = SocketIO(app)

rooms = {}
models = {}

@server.on('join')
def handle_join(data):
    room = data['room']
    if room not in rooms:
        rooms[room] = 1
        # TODO
        # Find(load) model for the room
        # model = find_model(room)
        # models[room] = model
    else:
        rooms[room] += 1
    join_room(room)

@server.on('leave')
def handle_leave(data):
    room = data['room']
    rooms[room] -= 1
    leave_room(room)

def find_model(room):
    # TODO
    # Find model for the room
    pass

def broadcast(price):
    '''
    TODO
    predict next price
    price: {"s": "BTCUSDT", "l": 50000, h: 51000, c: 50500, o: 49000, t: 1630000000, T: 1630000000}
    data: {
        "message": "NEW_CANDLESTICK",
        "actualPrice": price, 
        "symbol": "BTCUSDT", 
        "predPrice": {
            "l": 50000, 
            "h": 51000, 
            "c": 50500, 
            "o": 49000,
        }
    }
    '''
    # server.emit('message', data, room=data['room'])
    pass

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/candlesticks')
def get_candelsticks():
    ''' 
    TODO
    request: /candlesticks?symbol=btcusdt&feature=close,rsi,roc&model=lstm
    fetch from binance 2000 data points, 3 minutes interval
    can use python-binance: https://python-binance.readthedocs.io/en/latest/market_data.html#id7
    '''
    pass



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