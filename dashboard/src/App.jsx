import { useEffect, useState } from "react";
import { Select, Tooltip } from "antd";
import { HiOutlineChevronDown } from "react-icons/hi";
import Chart from "./components/Chart";
import { FEATURE_OPTIONS, METHOD_OPTIONS } from "./config/Constant";
import useSelectModel from "./hooks/useSelectModel";
import SelectSymbol from "./components/SelectSymbol";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa6";

function App() {
  const [showPrediction, setShowPrediction] = useState(true);
  const { method, setMethod, setFeatures, features, symbol, setSymbol, model } =
    useSelectModel();

  useEffect(() => {
    console.log("Model have changed: ", model?.symbol);
  }, [model]);

  return (
    <div className="min-h-screen bg-slate-50 py-5">
      <div className="w-4/5 max-w-screen-2xl mx-auto">
        <SelectSymbol symbol={symbol} setSymbol={setSymbol} />
        <div className="mt-2.5 flex items-end justify-end">
          <div className="flex items-end space-x-4">
            <div>
              <h6 className="text-slate-600 font-medium text-sm mb-1">
                Features
              </h6>
              <Select
                className="min-w-[150px]"
                suffixIcon={<HiOutlineChevronDown />}
                mode="multiple"
                placeholder="Select features"
                defaultValue={features}
                options={FEATURE_OPTIONS}
                onChange={(e) => setFeatures(e)}
              />
            </div>
            <div>
              <h6 className="text-slate-600 font-medium text-sm mb-1">
                Method
              </h6>
              <Select
                labelInValue
                className="w-[100px]"
                suffixIcon={<HiOutlineChevronDown />}
                defaultValue={method}
                options={METHOD_OPTIONS}
                onChange={(e) => setMethod(e.value)}
              />
            </div>
            <Tooltip
              title={showPrediction ? "Hide Prediction" : "Show Prediction"}
            >
              <button
                className="size-[38px] border border-gray-300 rounded-md flex items-center justify-center hover:bg-gray-100"
                onClick={() => setShowPrediction(!showPrediction)}
              >
                {showPrediction ? (
                  <FaRegEye className="text-gray-800 size-[18px]" />
                ) : (
                  <FaRegEyeSlash className="text-gray-500 size-[18px]" />
                )}
              </button>
            </Tooltip>
          </div>
        </div>
        <div className="mt-10">
          <Chart showPred={showPrediction} model={model} symbol={symbol} />
        </div>
      </div>
    </div>
  );
}

export default App;
