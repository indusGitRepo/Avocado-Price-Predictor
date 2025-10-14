# Question number 1: How in-demand are avocados in the US and how much supply is there based on price changes...
    # Will want to show overall average price increase over the years for all cities combined and how much volume there is

    # or Predict Avocado prices for US cities for the next 8 months, and let the user pick which city they would like to forecast from

# the dataset contains average price for a single avocado that week across major US cities, the total # of avocados sold that week in that city, 
# the total number of 4046, 4225, and 4770 avocados sold in that city, total bags, total small bags, total large bags, and total x-large bags sold in that city that week,
# and if the type of avocado was conventional or organic, the year, and the US city. This data is from 2015-2018.

# I want to get rid of some columns that seem redundant/unnessecary...

# year, average price for that year per city, total volume for that year per city, type 

# import the pandas library to manipulate and analyize avocado data
import pandas as pd

# copmute and derive calculations on the data set using numpy
import numpy as np

# Open source libary from meta for forecasting time-series data
from prophet import Prophet 

# Function to make forecast based on city and avocado type selected by user
def forecastPriceByCityAndType(city, avocadoType):

    # need to make both the user input and region and type from actual data set lowercase to match
    citiesData = avocadoDataFrame[(avocadoDataFrame['region'].str.lower() == city.lower()) & (avocadoDataFrame['type'].str.lower() == avocadoType.lower())].copy()

    # prophet requres ds the data variable in the to_datetime format and a numeric y variable which in this case will be the average price
    citiesData = citiesData.rename(columns={'Date': 'ds', 'AveragePrice': 'y'})

    # convert the date format to make it acceptable by prophet
    citiesData['ds'] = pd.to_datetime(citiesData['ds'])

    # log the avergae prices to have more symmetric distribution and better future forecasting
    citiesData['y'] = np.log(citiesData['y'])

    # propet model initalization where I want to capture yearly and weekly patterns from the data set
    # selecting a more conservative model for better predictions with changepoint scale being 0.01 < 0.05 and number of changepoints 25
    model = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=True, changepoint_prior_scale=0.01, n_changepoints=25)

    model.fit(citiesData)

    # predict future prices 8 months away that are all one week apart starting from the date the user selected both city and type
    startDate = pd.Timestamp.today().normalize() # today's date
    futureDate = pd.date_range(start=startDate, periods=36, freq='W')
    futureDataFrame = pd.DataFrame({'ds': futureDate})
    forecast = model.predict(futureDataFrame)

    # extract the predicted prices from the forecast and apply it to the predicted mean (predicted prices)
    forecast['yhat'] = np.exp(forecast['yhat'])
    forecast['yhat_lower'] = np.exp(forecast['yhat_lower']) # lower uncertaintiy level
    forecast['yhat_upper'] = np.exp(forecast['yhat_upper']) # higher uncertaintiy lebel

    forecastDataFrame = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    forecastDataFrame = forecastDataFrame.rename(columns={'ds': 'Date', 'yhat': 'Forecast', 'yhat_lower': 'Lower', 'yhat_upper': 'Upper'})

    return forecastDataFrame

# helper functions for FastAPI
def getAvailableCities():
    return availableCities

def getAvailableAvocadoTypes():
    return availableAvocadoTypes

# Print every value to 3 decimal places
pd.set_option('display.float_format', '{:.3f}'.format)

# read the csv file and store it in the avocado data frame
avocadoDataFrame = pd.read_csv('avocado.csv', index_col=0)

# clean data will only include what is needed for the model as seen below
cleanData = ['Date', 'AveragePrice', 'Total Volume', 'type', 'region']

# store the data from avocado.csv into the following variable
avocadoDataFrame = avocadoDataFrame[cleanData].copy()

# convert the date into datetime
avocadoDataFrame['Date'] = pd.to_datetime(avocadoDataFrame['Date'])
avocadoDataFrame = avocadoDataFrame.sort_values('Date')

availableCities = sorted(avocadoDataFrame['region'].unique())
availableAvocadoTypes = sorted(avocadoDataFrame['type'].unique())





