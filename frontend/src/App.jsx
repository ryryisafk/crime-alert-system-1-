import { useEffect, useState } from "react";
import "./App.css";

import SummaryCard from "./components/SummaryCard";
import TrendChart from "./components/TrendChart";
import DistrictChart from "./components/DistrictChart";
import AlertsPanel from "./components/AlertsPanel";
import PredictionPanel from "./components/PredictionPanel";
import CrimeMap from "./components/CrimeMap";

import {
  getDashboardSummary,
  getCrimeByDistrict,
  getMonthlyTrend,
  getHotspots,
  getAlerts,
} from "./api";

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

      .then(([summaryRes, districtRes, monthlyRes, hotspotRes, alertRes]) => {

        setSummary(summaryRes);

        setDistrictData(districtRes);

        setMonthlyData(monthlyRes);

        setHotspots(hotspotRes);

        setAlerts(alertRes);

      })

      .catch((err) => setError(err.message));

  }, []);

  if (error)
    return <h1>{error}</h1>;

  if (!summary)
    return <h1>Loading...</h1>;

  return (

    <div className="dashboard">

      <aside className="sidebar">

        <h2>🚔 Crime AI</h2>

      </aside>

      <main className="content">

        <header className="header">

          <h1>Crime Intelligence Dashboard</h1>

          <p>AI Powered Early Warning System</p>

        </header>

        <section className="summary-grid">

          <SummaryCard
            title="Total Crimes"
            value={summary.total_crimes}
            color="#3b82f6"
          />

          <SummaryCard
            title="Districts"
            value={summary.districts}
            color="#22c55e"
          />

          <SummaryCard
            title="Crime Types"
            value={summary.crime_types}
            color="#f59e0b"
          />

          <SummaryCard
            title="Active Alerts"
            value={alerts.length}
            color="#ef4444"
          />

        </section>
        <TrendChart data={monthlyData}/>
        <DistrictChart data={districtData}/>
        <CrimeMap hotspots={hotspots}/>
        <AlertsPanel alerts={alerts}/>
        <PredictionPanel/>
      </main>

    </div>

  );
}

export default App;