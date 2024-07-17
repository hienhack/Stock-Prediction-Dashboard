import { useEffect, useRef, useState } from "react";
import { api } from '../api';

function useSelectModel() {
    const [model, setModel] = useState(null);
    const [changing, setChanging] = useState(false);

    useEffect(() => {
        api.get("/current-model").then((res) => {
            setModel(res.data);
        }).catch((err) => {
            console.log(err);
        });
    }, []);

    const changeModel = (model) => {
        setModel(model);
        api.post("/change-model", model)
            .then((res) => {
                setModel(res.data);
            })
            .catch((err) => {
                console.log(err);
            }).finally(() => {
                setChanging(false);
            })
    }

    return { model, changeModel, changing };
}

export default useSelectModel;