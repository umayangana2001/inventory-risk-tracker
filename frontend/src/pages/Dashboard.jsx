import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {

  const [riskData, setRiskData] = useState([]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/inventory-risk")
      .then((response) => {

        setRiskData(response.data);

      })
      .catch((error) => {

        console.log(error);

      });

  }, []);

  // KPI calculations

  const totalItems = riskData.length;

  const riskItems = riskData.filter(
    item => item.RiskStatus === "RISK"
  ).length;

  const criticalItems = riskData.filter(
    item => item.RiskStatus === "CRITICAL"
  ).length;

  const safeItems = riskData.filter(
    item => item.RiskStatus === "SAFE"
  ).length;

  // Top risky items
  const topRiskItems = riskData
    .filter(item => item.WeeksCoverage < 3)
    .sort((a, b) => a.WeeksCoverage - b.WeeksCoverage)
    .slice(0, 5);

  return (

    <div>

      <h1 className="page-title">
        Inventory Intelligence Dashboard
      </h1>

      {/* KPI CARDS */}

      <div className="kpi-grid">

        <div className="kpi-card">
          <h2>{totalItems}</h2>
          <p>Total Items</p>
        </div>

        <div className="kpi-card risk-card">
          <h2>{riskItems}</h2>
          <p>Risk Items</p>
        </div>

        <div className="kpi-card critical-card">
          <h2>{criticalItems}</h2>
          <p>Critical Items</p>
        </div>

        <div className="kpi-card safe-card">
          <h2>{safeItems}</h2>
          <p>Safe Items</p>
        </div>

      </div>

      {/* TOP RISK ITEMS */}

      <div className="card">

        <h2>
          Top Risk Items
        </h2>

        <table className="risk-table">

          <thead>

            <tr>

              <th>Item</th>
              <th>On Hand</th>
              <th>Coverage</th>
              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {topRiskItems.map((item, index) => (

              <tr key={index}>

                <td>

  <a
    href={`/timeline?item=${item.Item}`}
    className="item-link"
  >

    {item.Item}

  </a>

</td>

                <td>{item.OnHand}</td>

                <td>
                  {item.WeeksCoverage.toFixed(2)}
                </td>

                <td>
                  {item.RiskStatus}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default Dashboard;