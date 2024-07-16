import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import AntdConfigProvider from "./config/AntdConfigProvider.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  // <React.StrictMode>
  <AntdConfigProvider>
    <App />
  </AntdConfigProvider>
  // </React.StrictMode>
);
