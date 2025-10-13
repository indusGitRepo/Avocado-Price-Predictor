import React, {userEffect, useState} from "react":
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
            axios.get("http://localhost:8000/api/forecast/", {
                parms: {city: selectedCity, avocadoType: selectedType},
            }).then((res) => setForecast(res.data));
        }
    }, [selectedCity, selectedType]);

    return(
        <div style={{padding: "2rem"}}>
            <h1>Avocado Price Forecast</h1>
            {/* Dropdown menus */}
            <select>
                
            </select>
        </div>
    )

}