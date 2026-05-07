import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./styles/globals.css";

const stored = typeof window !== "undefined" ? localStorage.getItem("t0-theme") : null;
if (stored === "light" || stored === "dark") {
  document.documentElement.dataset.theme = stored;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
