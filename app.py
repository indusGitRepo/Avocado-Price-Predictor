# this file is the bridge bewtween data cleaning and forecast logic in python and react front-end
# the react app will call this FASTAPI server through /api/forecast endpoint

from fastapi import FastAPI # create web API's and define routes like /api/cities that the React app can call
from fastapi.middleware.cors import CORSMiddleware # CORS (cross origin resourse sharing) allowes react (localhost3000) and backend (localhost:8000) to communicate
import main # main class with data cleaning and forecasting logic

from fastapi.staticfiles import StaticFiles # allows fastapi to serve static files
from fastapi.responses import FileResponse # allows fastapi to return a single file (index.html) in response to a request
import os # handles file paths for different os's

# create an instance of thr FASTAPI application where app is the object and will handle all HTTP requests
app = FastAPI()

# get the directoyr name of wehre app.py is located, and also point to the frontend build folder
appDirectory = os.path.join(os.path.dirname(__file__), "frontend", "build")

# so that whenever someone requests /static, serve it frontend/build/static
app.mount("/static", StaticFiles(directory=os.path.join(appDirectory, "static")), name="static")

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

# when someone uses the root url "/" serve index.html
@app.get("/")
@app.get("/{full_path:path}")
def reactApp(full_path: str = ""):
    pathIndex = os.path.join(appDirectory, "index.html")
    return FileResponse(pathIndex)

