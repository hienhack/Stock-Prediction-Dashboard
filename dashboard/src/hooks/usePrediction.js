import { getDistance } from "../helper/dateHelper";
import { useEffect, useRef, useState } from "react";
import { api } from "../api";

function usePrediction(model) {
    const [historyPred, setHistoryPred] = useState([]);
    const [newPred, setNewPred] = useState(null);
    const interval = useRef(null);

    useEffect(() => {
        if (!model) return;
        api.get('/prediction')
            .then((res) => {
                setHistoryPred(res.data);
                console.log(res.data);
            }).catch((err) => {
                console.log(err);
            });
        // if (!model) return;
        // console.log("fetching history prediction: ", model.symbol);
        // setTimeout(() => {
        //     axios
        //         .get(
        //             `https://api.binance.us/api/v3/klines?symbol=${model.symbol}&interval=5m&limit=1000`
        //         )
        //         .then((res) => {
        //             const fetchedData = res.data.map((tf) => {
        //                 const [time, open, high, low, close] = tf.map((e) => Number(e));
        //                 return { time: time / 1000, open: open - 2000, high: high - 2000, low: low - 2000, close: close - 2000 };
        //             });
        //             setHistoryPred(fetchedData);
        //         })
        //         .catch((err) => {
        //             console.log(err);
        //         });
        // }, 2000);


    }, [model?.symbol, model?.method, model?.features])

    useEffect(() => {
        if (historyPred.length === 0) return;
        const lastTime = historyPred[historyPred.length - 1].time;
        const timeout = getDistance(lastTime);
        setTimeout(() => {
            interval.current = setInterval(() => {
                api.get('/prediction?limit=1')
                    .then((res) => {
                        setNewPred(res.data[res.data.length - 1]);
                    }).catch((err) => {
                        console.log(err);
                    });
            }, 5000);
        }, timeout);

        return () => {
            clearInterval(interval.current);
        };
    }, [historyPred]);

    return [historyPred, newPred];
}

export default usePrediction;