import { useEffect, useState } from "react";

import {
    MapContainer,
    TileLayer,
    CircleMarker,
    Popup
} from "react-leaflet";

import { getHotspots } from "../api";

import MarkerClusterGroup from "react-leaflet-cluster";

function CrimeMap() {

    const [hotspots, setHotspots] = useState([]);
    const [crimeFilter, setCrimeFilter] = useState("All");
    console.log("Selected filter:", crimeFilter);
    
    useEffect(() => {

        getHotspots()
            .then(setHotspots)
            .catch(console.error);

    }, []);

    const crimeTypes = [

        "All",

        ...new Set(
            hotspots.map(h => h.crime_type)
        )

    ];

    const getColor = (risk) => {

        switch(risk){

            case "High":
                return "#ef4444";

            case "Medium":
                return "#f59e0b";

            default:
                return "#22c55e";
        }

    };

    const displayedHotspots = hotspots
        .filter(h =>
            crimeFilter === "All" ||
            h.crime_type === crimeFilter
        );

    // Only one marker per district
    const uniqueDistricts = Object.values(
        displayedHotspots.reduce((acc, item) => {

            if (!acc[item.district])
                acc[item.district] = item;

            return acc;

        }, {})
    );


    return (
        <div className="map-container">

        <div className="map-legend">

            <h4>Risk Level</h4>

            <div>
                <span className="legend-dot high"></span>
                High
            </div>

            <div>
                <span className="legend-dot medium"></span>
                Medium
            </div>

            <div>
                <span className="legend-dot low"></span>
                Low
            </div>

        </div>

        <div className="map-controls">

            <select
                value={crimeFilter}
                onChange={(e)=>setCrimeFilter(e.target.value)}
            >

                {crimeTypes.map(type=>(

                    <option
                        key={type}
                        value={type}
                    >

                        {type}

                    </option>

                ))}

            </select>

        </div>

        <MapContainer
            center={[15.3, 76.6]}
            zoom={7}
            style={{
                height: "600px",
                width: "100%",
                borderRadius: "12px"
            }}
        >

            <TileLayer
                attribution='&copy; OpenStreetMap contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {
                <MarkerClusterGroup
                    key={crimeFilter}
                    iconCreateFunction={(cluster) => {
                        const count = cluster.getChildCount();

                        return L.divIcon({
                            html: `<div><span>${count}</span></div>`,
                            className: "custom-cluster",
                            iconSize: L.point(42, 42, true),
                        });
                    }}
                >

                {
                    uniqueDistricts.map((spot, index) => (

                        <CircleMarker

                            key={index}

                            center={[spot.latitude, spot.longitude]}

                            radius={8}

                            fillColor={getColor(spot.risk)}

                            color="white"

                            weight={2}

                            fillOpacity={0.8}

                        >

                            <Popup>

                                <h3>{spot.district}</h3>

                                <hr />

                                <p><strong>Risk:</strong> {spot.risk}</p>

                                <p><strong>Crime Type:</strong> {spot.crime_type}</p>

                                <p><strong>Category:</strong> {spot.crime_category}</p>

                                <p><strong>Cases:</strong> {spot.crime_count}</p>

                                <p><strong>Crime Rate:</strong> {spot.crime_rate}</p>

                                <p><strong>Police Range:</strong> {spot.police_range}</p>

                                <p><strong>Conviction Rate:</strong> {spot.conviction_rate}%</p>

                                <p><strong>Chargesheet Rate:</strong> {spot.chargesheet_rate}%</p>

                                <p><strong>Pendency Rate:</strong> {spot.pendency_rate}%</p>

                            </Popup>

                        </CircleMarker>

                    ))
                }

            </MarkerClusterGroup>
            }

        </MapContainer>

        
        </div>

    );

    

}

export default CrimeMap;