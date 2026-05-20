import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import RiskMonitor from "./pages/RiskMonitor";
import Timeline from "./pages/Timeline";
import Shipments from "./pages/Shipments";
import Alternatives from "./pages/Alternatives";

import "./App.css";

function App() {

  return (

    <BrowserRouter>

      <div className="app-layout">

        {/* SIDEBAR */}

        <div className="sidebar">

          <h2 className="logo">
            Inventory IQ
          </h2>

          <nav>

            <Link to="/">Dashboard</Link>

            <Link to="/risk-monitor">
              Risk Monitor
            </Link>

            <Link to="/timeline">
              Timeline / Gantt
            </Link>

            <Link to="/shipments">
              Shipments
            </Link>

            <Link to="/alternatives">
              Alternatives
            </Link>

          </nav>

        </div>

        {/* MAIN CONTENT */}

        <div className="main-content">

          <Routes>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/risk-monitor"
              element={<RiskMonitor />}
            />

            <Route
              path="/timeline"
              element={<Timeline />}
            />

            <Route
              path="/shipments"
              element={<Shipments />}
            />

            <Route
              path="/alternatives"
              element={<Alternatives />}
            />

          </Routes>

        </div>

      </div>

    </BrowserRouter>

  );
}

export default App;