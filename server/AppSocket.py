import socket

'''
Connect to binance websocket
document: https://docs.binance.us/?shell#subscribe-to-a-stream
          https://docs.binance.us/?shell#candlestick-data-stream
interval: 3m
'''

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000) # mock
client_socket.connect(server_address)

# TODO
# This function is generated using Copilot
def subscribe(symbol):
    # Subscribe to a stream
    # symbol: BTCUSDT
    # interval: 3m
    client_socket.sendall(f'{{"method": "SUBSCRIBE", "params": ["{symbol}@kline_3m"], "id": 1}}'.encode())
    print(f'Subscribed to {symbol}@kline_3m')

# TODO
# This function is generated using Copilot
def unsubscribe(symbol):
    # Unsubscribe from a stream
    # symbol: BTCUSDT
    # interval: 3m
    client_socket.sendall(f'{{"method": "UNSUBSCRIBE", "params": ["{symbol}@kline_3m"], "id": 312}}'.encode())
    print(f'Unsubscribed from {symbol}@kline_3m')


# Listen to the stream, the code is generated using Copilot
while True:
    data = client_socket.recv(1024)
    print(data.decode())
    # TODO
    # receive data from binance, parse to object
