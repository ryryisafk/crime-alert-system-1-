function AlertsPanel({ alerts }) {

  return (

    <div className="alerts-card">

      <h2>AI Generated Alerts</h2>

      <div className="alerts-container">

        {alerts.map((alert, index) => (

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

    </div>

  );

}

export default AlertsPanel;
