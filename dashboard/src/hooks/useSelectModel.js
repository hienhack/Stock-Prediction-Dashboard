import { useEffect, useRef, useState } from "react";
import { api } from '../api'

function useSelectModel() {
    const [method, setMethod] = useState("LSTM");
    const [features, setFeatures] = useState(["Close"]);
    const [symbol, setSymbol] = useState("BTCUSDT");
    const [model, setModel] = useState(null);

    useEffect(() => {
        // api.get("/current-model").then((res) => {
        //     setMethod(res.data.method);
        //     setFeatures(res.data.features);
        //     setSymbol(res.data.symbol);
        // }).catch((err) => {
        //     console.log(err);
        // });
        setModel({
            method: "LSTM",
            features: ["Close"],
            symbol: "BTCUSDT"
        });
    }, []);

    useEffect(() => {
        if (!method || features.length === 0 || !symbol) return;

        // api.post("/change-model", { method, features, symbol })
        //     .then((res) => {
        //         setModel(res.data);
        //      })
        //     .error((err) => {
        //         console.log(err);
        //     });

        const newModel = { method, features, symbol };

        setModel(newModel);

    }, [method, symbol, features]);

    return { method, setMethod, setFeatures, features, symbol, setSymbol, model };
}

export default useSelectModel;