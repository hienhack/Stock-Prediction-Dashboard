import asyncio
import websockets
import json
import csv
import os
from datetime import datetime, timezone

uri = "wss://stream.binance.com:9443/ws"
client_socket = None
latest_kline_data = None  # Global variable to store the latest kline data

async def connect_to_websocket(uri):
    global client_socket
    while True:
        try:
            client_socket = await websockets.connect(uri)
            print(f"Connected to WebSocket: {uri}")
            return
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)

async def subscribe(symbol):
    global client_socket
    subscription_message = json.dumps({
        "method": "SUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_3m"],
        "id": 1
    })
    await client_socket.send(subscription_message)
    print(f'Subscribed to {symbol}@kline_3m')

async def unsubscribe(symbol):
    global client_socket
    unsubscription_message = json.dumps({
        "method": "UNSUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_3m"],
        "id": 312
    })
    await client_socket.send(unsubscription_message)
    print(f'Unsubscribed from {symbol}@kline_3m')

def write_kline_to_csv(symbol, kline_data):
    file_path = f"./data/{symbol}.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Date", "Open", "High", "Low", "Close"])
        
        # Convert timestamp to date
        date = datetime.fromtimestamp(kline_data['t'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        
        writer.writerow([
            date, kline_data['o'], kline_data['h'], kline_data['l'], kline_data['c']
        ])

async def listen_to_stream(symbol):
    global client_socket, latest_kline_data
    try:
        await subscribe(symbol)
        while True:
            message = await client_socket.recv()
            message_dict = json.loads(message)
            if 'k' in message_dict:  # Check if the message contains kline data
                kline_data = message_dict['k']
                latest_kline_data = kline_data
                print(f"Kline Data: {kline_data}")
                write_kline_to_csv(symbol, kline_data)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
        print("Attempting to reconnect...")
        await connect_to_websocket(uri)
        await listen_to_stream(symbol)
    except KeyboardInterrupt:
        await unsubscribe(symbol)
        print("Interrupted, unsubscribing and closing connection")
    finally:
        if client_socket:
            await client_socket.close()

# Function to start WebSocket client
async def start_websocket_client(symbol):
    await connect_to_websocket(uri)
    await listen_to_stream(symbol)

# Test socket connection
symbol = 'BTCUSDT'
asyncio.run(start_websocket_client(symbol))
