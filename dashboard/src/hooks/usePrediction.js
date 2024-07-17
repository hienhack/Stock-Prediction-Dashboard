import { getTimeDiff } from "../helper/dateHelper";
import { useEffect, useState } from "react";
import { api } from "../api";

let intervalID = null;

function usePrediction(model) {
    const [historyPred, setHistoryPred] = useState([]);
    const [newPred, setNewPred] = useState(null);

    useEffect(() => {
        if (!model) return;
        api.get('/prediction')
            .then((res) => {

                setHistoryPred(res.data.map((pred) => { pred.time = pred.time + 25200; return pred; }));
            }).catch((err) => {
                console.log(err);
            });
    }, [model?.symbol, model?.method, model?.features])

    useEffect(() => {
        if (intervalID != null) return;
        const fetchNewPred = () => {
            api.get('/prediction?limit=1')
                .then((res) => {
                    const pred = res.data[res.data.length - 1];
                    pred.time = pred.time + 25200;
                    setNewPred(pred);
                }).catch((err) => {
                    console.log(err);
                });
        }

        const timeout = getTimeDiff();
        console.log("Timeout: ", timeout);
        console.log("time out: ", new Date(Date.now() + timeout))
        setTimeout(() => {
            fetchNewPred();
            intervalID = setInterval(() => fetchNewPred(), 300000);
        }, timeout);
    }, []);

    return [historyPred, newPred];
}

export default usePrediction;