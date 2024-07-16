import { useEffect, useRef, useState } from 'react';
import { ws, subscribe, unsubscribe } from '../Socket';
import axios from 'axios';

function useActualData(symbol) {
    const [newCandle, setNewCandle] = useState();
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!symbol) return;
        // fetch historical data
        axios
            .get(
                `https://api.binance.us/api/v3/klines?symbol=${symbol}&interval=5m&limit=1000`
            )
            .then((res) => {
                const fetchedData = res.data.map((tf) => {
                    const [time, open, high, low, close] = tf.map((e) => Number(e));
                    return { time: time / 1000, open, high, low, close };
                });
                setData(fetchedData);
            })
            .catch((err) => {
                console.log(err);
            });

        // subscribe to the symbol stream
        subscribe(symbol);

        const evnetHandler = (event) => {
            const message = JSON.parse(event.data);
            console.log("message: ", message);
            if (message.k) {
                const { t, o, h, l, c, s } = message.k;
                console.log(s);
                setNewCandle({ time: t / 1000, open: Number(o), high: Number(h), low: Number(l), close: Number(c) });
            }
        }

        ws.addEventListener('message', function (event) {
            evnetHandler(event);
        });

        return () => {
            ws.removeEventListener('message', function (event) {
                evnetHandler(event);
            });
            unsubscribe(symbol);
        };
    }, [symbol]);

    return [data, newCandle];
}

export default useActualData;