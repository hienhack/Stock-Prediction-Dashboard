from App import app
from AppSocket import start_websocket_client
import asyncio

if __name__ == "__main__":
    app.run(debug=True)

    # Start the WebSocket client
    # symbol = "BTCUSDT"
    # asyncio.create_task(start_websocket_client(symbol))


    
