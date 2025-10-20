# this file is the bridge bewtween data cleaning and forecast logic in python and react front-end
# the react app will call this FASTAPI server through /api/forecast endpoint

from fastapi import FastAPI # create web API's and define routes like /api/cities that the React app can call
from fastapi.middleware.cors import CORSMiddleware # CORS (cross origin resourse sharing) allowes react (localhost3000) and backend (localhost:8000) to communicate
import main # main class with data cleaning and forecasting logic

# create an instance of thr FASTAPI application where app is the object and will handle all HTTP requests
app = FastAPI()

# add CORS middleware to the fastapi app and allow all origins, HTTP methods, and headers to make requests to this API ( change when in production '*' to more limited access)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,allow_methods=["*"], allow_headers=["*"])

# get endpoint /api/cities where @app.get() makes this function a route, so when
# the react front-end makes a get request to this endpoint the getCities() function will run
@app.get("/api/cities")

# grab available sorted list of cities from main.py and return it as a JSON object
def getCities():
    return {"cities": main.availableCities}

@app.get("/api/types")
def getTypes():
    return {"types": main.availableAvocadoTypes}

# based on the city and type selected by user on front-end, this function returns a dataframe with the forecast (JSON FRIENDLY)
@app.get("/api/forecast")
def forecast(city: str, avocadoType: str):
    forecastData, seasonalityData = main.forecastPriceByCityAndType(city, avocadoType)
    return {
        "forecast": forecastData.to_dict(orient="records"),
        "seasonality": seasonalityData.to_dict(orient="records")
    }

