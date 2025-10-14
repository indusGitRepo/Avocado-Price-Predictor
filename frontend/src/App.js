import React, {useEffect, useState} from "react"
import axios from "axios"; // library for making HTTP requests to FastAPI backend
import {
    LineChart,Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label} from "recharts"; // compnents to build charts

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
        <div style={{ 
            padding: "2rem", 
            backgroundColor: "#f3fcf0"}}>
            <h1
            style={{
                color: "#144205",     
                fontSize: "2.5rem",
                textAlign: "center",   
                fontFamily: "Arial, sans-serif",
                marginBottom: "5rem",  
                textShadow: "2px 2px 4px rgba(0,0,0,0.2)" 
            }}
            >
            Avocado Price Forecast
            </h1>
            <p
                style={{
                    fontSize: "1rem",
                    color: "#361e00",
                    lineHeight: "1.6",
                    fontFamily: "Arial, sans-serif",
                    margin: "0 auto 9rem auto", 
                    maxWidth: "600px",
                    textAlign: "center", 
                    textIndent: "2em", 
                }}
            >
                This Prophet model uses weekly avocado prices from cities across the USA from 2015-2018, and predicts how much the price of one conventional or organic 
                avocado will cost by city. To use this model select the city you would like to see predictions for, as well as, the type of avocado from the drop down menus. 
                As a result, you will be able to see the average price for a single avocado forecast 8 months from today’s date, as well as the uncertainty of the prediction from the Upper and Lower bounds. The overall forecast predicts by week.
            </p>

            {/* Dropdown menus */}
            <div style={{ textAlign: "center", marginBottom: "5rem" }}>
            <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                borderRadius: "8px",
                border: "1px solid #4CAF50",
                backgroundColor: "#f3fcf0",
                color: "#144205",
                outline: "none",
                cursor: "pointer",
                marginRight: "1rem"
                }}
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
                style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                borderRadius: "8px",
                border: "1px solid #4CAF50",
                backgroundColor: "#f3fcf0",
                color: "#144205",
                outline: "none",
                cursor: "pointer",
                }}
            >
                <option value="">Select Avocado Type</option>
                {types.map((type) => (
                <option key={type} value={type}>
                    {type}
                </option>
                ))}
            </select>
            </div>

            {/* Line chart for the forecast */}
            {forecast.length > 0 && (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart
                        data={forecast}
                        margin={{ top: 50, right: 50, left: 150, bottom: 70 }}
                        style={{ backgroundColor: "rgb(255, 250, 246)", display: "flex", justifyContent: "center", marginTop: "7rem"}}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                        dataKey="Date"
                        tickCount={10}
                        angle={-45}
                        textAnchor="end"
                        minTickGap={15}
                        tickFormatter={(date) =>
                            new Date(date).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            })
                        }
                        >
                        <Label value="Date" offset={-45} position="insideBottom" 
                        style={{ fontWeight: 'bold', fill: '#000000', fontSize: 18}}/>
                        
                        </XAxis>
                        <YAxis
                        >
                        <Label value="Price Per Avocado (USD)"
                        
                        angle={-90}
                        position="left" 
                        style={{ textAnchor: 'middle', fontWeight: 'bold', fill: '#000000', fontSize: 18 }}/>
                        </YAxis>
                        <Tooltip />
                        <Legend 
                        verticalAlign="top" height={36}/>
                        <Line
                            type="monotone"
                            dataKey="Forecast"
                            stroke="#615bcf"
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="Lower"
                            stroke="#43cc78"
                            dot={false}
                            strokeDasharray="5 5"
                        />
                        <Line
                            type="monotone"
                            dataKey="Upper"
                            stroke="#43cc78"
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