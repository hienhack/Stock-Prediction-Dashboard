const BINANCE_WS_BASE_URL = 'wss://stream.binance.com:9443/ws';

// Create a WebSocket connection to the base URL
const ws = new WebSocket(BINANCE_WS_BASE_URL);

ws.addEventListener('open', function open() {
    console.log('Connected to Binance WebSocket server');
});

ws.addEventListener('error', function error(err) {
    console.error('WebSocket error:', err);
});

// Function to subscribe to a specific symbol's stream
function subscribe(symbol) {
    const streamName = `${symbol.toLowerCase()}@kline_5m`;
    const subscribeMessage = {
        method: "SUBSCRIBE",
        params: [streamName],
        id: 1
    };

    const interval = setInterval(() => {
        console.log("Waiting for WebSocket connection...");
        if (ws.readyState !== WebSocket.OPEN) return;
        ws.send(JSON.stringify(subscribeMessage));
        console.log(`Subscribed to ${streamName}`);
        clearInterval(interval);
    }, 1000);
}

function unsubscribe(symbol) {
    const streamName = `${symbol.toLowerCase()}@kline_5m`;
    const unsubscribeMessage = {
        "method": "UNSUBSCRIBE",
        "params": [streamName], // Fixed to use toLowerCase()
        "id": 2 // Using a different ID for unsubscribe action
    };

    const interval = setInterval(() => {
        console.log("Waiting for WebSocket connection...");
        if (ws.readyState !== WebSocket.OPEN) return;
        ws.send(JSON.stringify(unsubscribeMessage));
        console.log(`unsubscribed to ${streamName}`);
        clearInterval(interval);
    }, 1000);
}

window.addEventListener('beforeunload', () => {
    ws.close();
    console.log('WebSocket connection closed');
});

// Export the functions and the WebSocket connection
export { subscribe, unsubscribe, ws };