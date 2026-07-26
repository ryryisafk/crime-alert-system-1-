import { useEffect, useState } from "react";

import {
    predictCrime,
    getDistricts,
    getCrimeTypes
} from "../api";

function PredictionPanel() {

  const [district, setDistrict] = useState("");
  const [crimeType, setCrimeType] = useState("");

  const [districts, setDistricts] = useState([]);
  const [crimeTypes, setCrimeTypes] = useState([]);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  useEffect(() => {

      getDistricts().then(setDistricts);

      getCrimeTypes().then(setCrimeTypes);

  }, []);

  const handlePredict = async () => {

    setLoading(true);

    try {

      const response = await predictCrime({

        district: district,

        crime_type: crimeType

      });


      setResult(response);


    } catch(error){

      console.log(error);

    }

    setLoading(false);

  };


  return (

    <div className="prediction-card">

      <h2>
        🤖 AI Risk Prediction
      </h2>

      <div className="prediction-form">
      <select
          value={district}
          onChange={(e)=>setDistrict(e.target.value)}
      >

          <option value="">
              Select District
          </option>

          {districts.map(d => (

              <option
                  key={d}
                  value={d}
              >
                  {d}
              </option>

          ))}

      </select>


      <select
          value={crimeType}
          onChange={(e)=>setCrimeType(e.target.value)}
      >

          <option value="">
              Select Crime Type
          </option>

          {crimeTypes.map(c => (

              <option
                  key={c}
                  value={c}
              >
                  {c}
              </option>

          ))}

      </select>


      <button onClick={handlePredict} disabled={!district || !crimeType || loading}>

        {loading ? "Predicting..." : "Predict"}

      </button>
      </div>

        {result && (

          <div className="prediction-result">

              <h2>🚨 Risk: {result.risk}</h2>

              <p>
                  <strong>Confidence:</strong> {result.confidence}%
              </p>

              <p>
                  <strong>Warning Score:</strong> {result.warning_score}/100
              </p>

              <hr />

              <h3>📍 Location Details</h3>

              <p><strong>District:</strong> {result.district}</p>

              <p><strong>Police Range:</strong> {result.police_range}</p>

              <p><strong>Crime Type:</strong> {result.crime_type}</p>

              <p><strong>Crime Category:</strong> {result.crime_category}</p>

              <hr />

              <h3>📊 Crime Statistics</h3>

              <p><strong>Crime Count:</strong> {result.crime_count}</p>

              <p><strong>Crime Rate:</strong> {result.crime_rate}</p>

              <p>
                  <strong>Anomaly Detected:</strong>{" "}
                  {result.is_anomaly ? "⚠️ Yes" : "✅ No"}
              </p>

              <hr />

              <h3>🧠 AI Reasoning</h3>

              <ul>
                  {result.reasoning.map((item, index) => (
                      <li key={index}>{item}</li>
                  ))}
              </ul>

              <hr />

              <h3>🛡️ Recommendations</h3>

              <ul>
                  {result.recommendations.map((item, index) => (
                      <li key={index}>{item}</li>
                  ))}
              </ul>

          </div>

          )}


    </div>

  );

}


export default PredictionPanel;