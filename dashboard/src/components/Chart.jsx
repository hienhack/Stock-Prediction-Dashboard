import { createChart, ColorType } from "lightweight-charts";
import { useEffect, useRef, useState } from "react";
import usePrediction from "../hooks/usePrediction";
import useActualData from "../hooks/useAuctalData";

function Chart({ showPred, model }) {
  const containerRef = useRef();
  const [data, newCandle] = useActualData(model?.symbol);
  // const [data, setData] = useState([]);
  // const [newCandle, setNewCandle] = useState(null);
  const [historyPred, newPred] = usePrediction(model);
  const [actualSeries, setActualSeries] = useState(null);
  const [predSeries, setPredSeries] = useState(null);
  const predDataRef = useRef([]);

  // Initialize the chart
  useEffect(() => {
    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "#f8fafc" },
        textColor: "#475569",
      },
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
      timeScale: {
        timeVisible: true,
      },
    });
    chart.timeScale().fitContent();
    chart.timeScale().scrollToPosition(5);

    const series = chart.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });
    setActualSeries(series);

    const predSeries = chart.addCandlestickSeries({
      upColor: "#22c55eb3",
      downColor: "#ef4444b3",
      borderVisible: false,
      wickUpColor: "#22c55eb3",
      wickDownColor: "#ef4444b3",
    });
    setPredSeries(predSeries);
  }, []);

  useEffect(() => {
    if (data.length == 0 || !actualSeries) return;

    actualSeries.setData(data);
  }, [data, actualSeries]);

  useEffect(() => {
    if (!newCandle || !actualSeries) return;
    actualSeries.update(newCandle);
  }, [newCandle, actualSeries]);

  useEffect(() => {
    if (historyPred.length == 0 || !predSeries) return;

    predDataRef.current = historyPred;
    if (showPred) predSeries.setData(historyPred);
  }, [historyPred, predSeries]);

  useEffect(() => {
    if (!newPred || !predSeries) return;
    predDataRef.current.push(newPred);
    predSeries.update(newPred);
  }, [newPred, predSeries]);

  useEffect(() => {
    if (!predSeries) return;
    if (!showPred) {
      predSeries.setData([]);
    } else {
      predSeries.setData(predDataRef.current);
    }
  }, [showPred, predSeries]);

  return <div className="h-[580px]" ref={containerRef}></div>;
}

export default Chart;
