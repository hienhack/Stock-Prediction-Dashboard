import { useEffect, useRef, useState } from "react";
import { api } from '../api';

function useSelectModel() {
    const [method, setMethod] = useState(null);
    const [features, setFeatures] = useState([]);
    const [symbol, setSymbol] = useState(null);
    const [model, setModel] = useState(null);

    useEffect(() => {
        api.get("/current-model").then((res) => {
            setMethod(res.data.model);
            setFeatures(res.data.features);
            setSymbol(res.data.symbol);
            setModel(res.data);
        }).catch((err) => {
            console.log(err);
        });
    }, []);

    useEffect(() => {
        if (!method || features.length === 0 || !symbol) return;

        api.post("/change-model", { model: method, features, symbol })
            .then((res) => {
                setModel(res.data);
            })
            .catch((err) => {
                console.log(err);
            });

        const newModel = { method, features, symbol };

        setModel(newModel);

    }, [method, symbol, features]);

    return { method, setMethod, setFeatures, features, symbol, setSymbol, model };
}

export default useSelectModel;