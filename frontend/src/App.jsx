import { useEffect, useState } from "react";
import {
  getDashboardSummary,
  getCrimeByDistrict,
  getMonthlyTrend,
  getHotspots,
  getAlerts,
} from "./api";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [districtData, setDistrictData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      getDashboardSummary(),
      getCrimeByDistrict(),
      getMonthlyTrend(),
      getHotspots(),
      getAlerts(),
    ])
      .then(([summaryRes, districtRes, monthlyRes, hotspotsRes, alertsRes]) => {
        setSummary(summaryRes);
        setDistrictData(districtRes);
        setMonthlyData(monthlyRes);
        setHotspots(hotspotsRes);
        setAlerts(alertsRes);
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <div>Error loading data: {error}</div>;
  if (!summary) return <div>Loading...</div>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Crime Early Warning Dashboard</h1>

      <section>
        <h2>Summary</h2>
        <p>Total crimes: {summary.total_crimes}</p>
        <p>Districts: {summary.districts}</p>
        <p>Crime types: {summary.crime_types}</p>
      </section>

      <section>
        <h2>Crimes by District</h2>
        <ul>
          {districtData.map((d) => (
            <li key={d.district}>
              {d.district}: {d.count}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Monthly Trend</h2>
        <ul>
          {monthlyData.map((m) => (
            <li key={m.month}>
              {m.month}: {m.count}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Hotspots ({hotspots.length})</h2>
        <ul>
          {hotspots.slice(0, 10).map((h, i) => (
            <li key={i}>
              ({h.latitude}, {h.longitude}) — {h.risk} risk
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Alerts</h2>
        {alerts.length === 0 ? (
          <p>No active alerts.</p>
        ) : (
          <ul>
            {alerts.map((a, i) => (
              <li key={i}>
                <strong>{a.risk}</strong> — {a.district} — {a.reason}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;