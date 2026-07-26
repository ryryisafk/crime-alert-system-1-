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

      {
        result && (

          <div className="prediction-result">

            <h3>
              Risk: {result.predicted_risk}
            </h3>


            <p>
              Confidence:
              {" "}
              {(result.confidence * 100).toFixed(1)}%
            </p>

          </div>

        )
      }


    </div>

  );

}


export default PredictionPanel;