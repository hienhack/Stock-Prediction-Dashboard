import asyncio
import websockets
import json

uri = "wss://stream.binance.com:9443/ws"
client_socket = None

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

async def subscribe( symbol):
    # Subscribe to a stream
    # symbol: BTCUSDT
    # interval: 3m
    global client_socket
    subscription_message = json.dumps({
        "method": "SUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_3m"],
        "id": 1
    })
    await client_socket.send(subscription_message)
    print(f'Subscribed to {symbol}@kline_3m')

async def unsubscribe( symbol):
    # Unsubscribe from a stream
    # symbol: BTCUSDT
    # interval: 3m
    global client_socket
    unsubscription_message = json.dumps({
        "method": "UNSUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_3m"],
        "id": 312
    })
    await client_socket.send(unsubscription_message)
    print(f'Unsubscribed from {symbol}@kline_3m')

async def listen_to_stream(symbol):
    global client_socket
    try:
        await subscribe(symbol)
        while True:
            message = await client_socket.recv()
            message_dict = json.loads(message)
            if 'k' in message_dict:  # Check if the message contains kline data
                kline_data = message_dict['k']
                print(f"Kline Data: {kline_data}")
                # Process kline_data further if needed
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
        print("Attempting to reconnect...")
        await connect_to_websocket(uri)
        await listen_to_stream()
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