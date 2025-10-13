import React, {useEffect, useState} from "react"
import axios from "axios"; // library for making HTTP requests to FastAPI backend
import {
    LineChart,Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,} from "recharts"; // compnents to build charts

function App(){
    const [cities, setCities] = useState([]); // array of all avaialbe cities in drop-down menu
    const [types, setTypes] = useState([]); // array of all avaialbe avocado types in drop-down menu
    const [selectedCity, setSelectedCity] = useState(""); // selected city by user
    const [selectedType, setSelectedType] = useState(""); // selected avocado type by user
    const [forecast, setForecast] = useState([]); // array of forecast data frame from the backend

    // this will only run once when the compnent mounts due to the [] array, and grabs all the cities and types from FastAPI endpoint
    // then res.data.cities  and res.data.types returns a JSON object which then updates the react states setCities and setTypes
    useEffect(() => {
        axios.get("http://localhost:8000/api/cities").then((res) => setCities(res.data.cities));
        axios.get("http://localhost:8000/api/types").then((res) => setTypes(res.data.types));
    }, []);

    // this will run every time the selected city or avocado type is changed and
    // then sends a GET request to /api/forecast/ with quiery paramaters (city and avocadoType), and then based on data frame returend from backend sets the forecast
    useEffect(() => {
        if (selectedCity && selectedType){
            axios.get("http://localhost:8000/api/forecast", {
                params: {city: selectedCity, avocadoType: selectedType},
            }).then((res) => setForecast(res.data));
        }
    }, [selectedCity, selectedType]);

    return (
        <div style={{ padding: "2rem" }}>
            <h1>Avocado Price Forecast</h1>

            {/* Dropdown menus */}
            <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
            >
                <option value="">Select City</option>
                {cities.map((city) => (
                    <option key={city} value={city}>
                        {city}
                    </option>
                ))}
            </select>

            <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                style={{ marginLeft: "1rem" }}
            >
                <option value="">Select Avocado Type</option>
                {types.map((type) => (
                    <option key={type} value={type}>
                        {type}
                    </option>
                ))}
            </select>

            {/* Line chart for the forecast */}
            {forecast.length > 0 && (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart
                        data={forecast}
                        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="Date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="Forecast"
                            stroke="#8884d8"
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="Lower"
                            stroke="#82ca9d"
                            dot={false}
                            strokeDasharray="5 5"
                        />
                        <Line
                            type="monotone"
                            dataKey="Upper"
                            stroke="#82ca9d"
                            dot={false}
                            strokeDasharray="5 5"
                        />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default App;