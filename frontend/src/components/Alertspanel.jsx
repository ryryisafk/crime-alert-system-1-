import { useState } from "react";

function AlertsPanel({ alerts }) {
  const [showAll, setShowAll] = useState(false);

  return (

    <div className="alerts-card">

      <h2>AI Generated Alerts</h2>

      <div className="alerts-container">

        {(showAll ? alerts : alerts.slice(0, 2)).map((alert, index) => (

          <div
            className="alert-item"
            key={index}
          >

            <div className="alert-header">

              <span className="risk">
                🚨 {alert.risk}
              </span>

              <span>
                {alert.district}
              </span>

            </div>


            <h3>
              {alert.crime_type}
            </h3>


            <p>
              {alert.reason}
            </p>


          </div>

        ))}

      </div>
          {alerts.length > 2 && (

      <button
        className="view-all-btn"
        onClick={() => setShowAll(!showAll)}
      >
        {showAll
          ? "Show Less"
          : `View All (${alerts.length})`}
      </button>

    )}

    </div>

  );

}

export default AlertsPanel;
