import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

function Timeline() {

  const [timelineData, setTimelineData] = useState([]);
  const [riskData, setRiskData] = useState(null);

 const location = useLocation();

const params = new URLSearchParams(location.search);

const initialItem =
  params.get("item") || 900724;

const [itemId, setItemId] =
  useState(initialItem);

  useEffect(() => {

    axios
      .get(`http://127.0.0.1:8000/timeline/${itemId}`)
      .then((response) => {
        setTimelineData(response.data);
      })
      .catch((error) => {
        console.log(error);
      });

      axios
  .get("http://127.0.0.1:8000/inventory-risk")
  .then((response) => {

    const selectedItem = response.data.find(
      item => item.Item == itemId
    );

    setRiskData(selectedItem);

  })
  .catch((error) => {

    console.log(error);

  });
  }, [itemId]);

  return (

    <div>

      <h1 className="page-title">
        Inventory Timeline / Gantt
      </h1>

      {/* ITEM SELECTOR */}

      <div className="card">

        <h3>Select Item</h3>

        <select
          value={itemId}
          onChange={(e) => setItemId(e.target.value)}
        >

          <option value="900724">900724</option>
          <option value="900731">900731</option>
          <option value="900736">900736</option>
          <option value="900738">900738</option>

        </select>

      </div>

      {/* STOCK CHART */}

      <div className="card">

        <h3>Projected Stock Timeline</h3>

        <ResponsiveContainer width="100%" height={400}>

          <LineChart data={timelineData}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="Week" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="ProjectedStock"
              stroke="#38bdf8"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>
      {/* KPI SECTION */}

{riskData && (

  <div className="timeline-kpis">

    <div className="timeline-kpi-card">

      <h2>
        {riskData.OnHand}
      </h2>

      <p>Current Stock</p>

    </div>

    <div className="timeline-kpi-card">

      <h2>
        {riskData.AvgWeeklyUsage.toFixed(0)}
      </h2>

      <p>Avg Weekly Usage</p>

    </div>

    <div className="timeline-kpi-card">

      <h2>
        {riskData.WeeksCoverage.toFixed(1)}
      </h2>

      <p>Weeks Coverage</p>

    </div>

    <div className="timeline-kpi-card">

      <h2>
        {riskData.RiskStatus}
      </h2>

      <p>Current Risk</p>

    </div>

  </div>

)}

      {/* GANTT STYLE RISK BLOCKS */}

 {/* ENTERPRISE GANTT */}

<div className="card">

  <h3>
    Inventory Risk Timeline
  </h3>

  <div className="enterprise-gantt">

    {timelineData.map((week, index) => {

      // Temporary shipment simulation
      const shipmentWeeks = [
        "2026-W24",
        "2026-W28"
      ];

      const ShipmentArrival =
        shipmentWeeks.includes(week.Week);

      return (

        <div
          key={index}
          className="gantt-row-enterprise"
        >

          {/* WEEK LABEL */}

          <div className="gantt-week-label">

            {week.Week}

          </div>

          {/* GANTT BAR */}

          <div className="gantt-bar-container">

           <div
  className={`gantt-bar ${week.Status
    .toLowerCase()
    .replaceAll(" ", "-")}`}

  style={{

    width:

      week.Status === "SAFE"
        ? "100%"

      : week.Status === "RISK"
        ? "70%"

      : week.Status === "CRITICAL"
        ? "45%"

      : "25%"
  }}
>

              <div className="gantt-content">

                <span>
                  {week.Status}
                </span>

                {ShipmentArrival && (

                  <span className="shipment-marker">

                    🚚 Shipment

                  </span>

                )}

              </div>

            </div>

          </div>

        </div>

      );

    })}

  </div>

</div>

    </div>

  );
}

export default Timeline;