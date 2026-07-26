import { useState } from "react";
import { predictCrime } from "../api";


function PredictionPanel() {

  const [district, setDistrict] = useState("");
  const [crimeType, setCrimeType] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);


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


      <input
        placeholder="District"
        value={district}
        onChange={(e)=>setDistrict(e.target.value)}
      />


      <input
        placeholder="Crime Type"
        value={crimeType}
        onChange={(e)=>setCrimeType(e.target.value)}
      />


      <button onClick={handlePredict}>

        {loading ? "Predicting..." : "Predict"}

      </button>


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