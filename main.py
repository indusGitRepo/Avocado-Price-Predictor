# Question number 1: How in-demand are avocados in the US and how much supply is there based on price changes...
    # Will want to show overall average price increase over the years for all cities combined and how much volume there is

    # or Predict Avocado prices for US cities for the next 10 years, as well as all those cities combined.

# the dataset contains average price for a single avocado that week across major US cities, the total # of avocados sold that week in that city, 
# the total number of 4046, 4225, and 4770 avocados sold in that city, total bags, total small bags, total large bags, and total x-large bags sold in that city that week,
# and if the type of avocado was conventional or organic, the year, and the US city. This data is from 2015-2018.

# I want to get rid of some columns that seem redundant/unnessecary...

# year, average price for that year per city, total volume for that year per city, type 

# import the pandas library to work with and manipulate avocado data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet 

# Function to make forecast based on city and avocado type selected by user
def forecastPriceByCityAndType(city, avocadoType):
    citiesData = avocadoDataFrame[(avocadoDataFrame['region'].str.lower() == city.lower()) & (avocadoDataFrame['type'].str.lower() == avocadoType.lower())].copy()

    # date will be the index and for prophet it requires ds (date) and y (target variable)
    citiesData = citiesData.rename(columns={'Date': 'ds', 'AveragePrice': 'y'})
    citiesData['ds'] = pd.to_datetime(citiesData['ds'])
    citiesData['y'] = np.log(citiesData['y'])

    # Prophet model initalization
    model = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=True, changepoint_prior_scale=0.01, n_changepoints=25)

    model.fit(citiesData)

    futureDataFrame = model.make_future_dataframe(periods=36,freq='W')
    forecast = model.predict(futureDataFrame)

    # extract the predicted prices from the forecast and apply it to the predicted mean (predicted prices)
    forecast['yhat'] = np.exp(forecast['yhat'])
    forecast['yhat_lower'] = np.exp(forecast['yhat_lower'])
    forecast['yhat_upper'] = np.exp(forecast['yhat_upper'])

    forecastDataFrame = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    forecastDataFrame = forecastDataFrame.rename(columns={'ds': 'Date', 'yhat': 'Forecast', 'yhat_lower': 'Lower', 'yhat_upper': 'Upper'})

    return forecastDataFrame

def getAvailableCities():
    return availableCities

def getAvailableAvocadoTypes():
    return availableAvocadoTypes

    # confidence interval for each forecasted value (uncertain ranges)
    #forecastConfidenceInterval = forecast.conf_int()
    # fig1 = model.plot(forecast)
    # plt.title(f"Avocado Price Forecast - {city.title()} ({avocadoType})")
    # plt.xlabel("Date")
    # plt.ylabel("Predicted Average Price ($)")
    # plt.tight_layout()
    # plt.show()

    # fig2 = model.plot_components(forecast)
    # plt.tight_layout()
    # plt.show()


    # print(f"\n📈 Predicted prices for {city.title()} ({avocadoType}) — next 36 weeks:\n")
    # print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(36).to_string(index=False))

#import statsmodels.api as sm # for estimating relationships between variables

# Print every value to 3 decimal places
pd.set_option('display.float_format', '{:.3f}'.format)

avocadoDataFrame = pd.read_csv('avocado.csv', index_col=0)

cleanData = ['Date', 'AveragePrice', 'Total Volume', 'type', 'region']

# store the data from avocado.csv into the following variable
avocadoDataFrame = avocadoDataFrame[cleanData].copy()

#averagePricePerYearPerCity = avocadoDataFrame.groupby(['region', 'year', 'type']).agg({'AveragePrice': 'mean', 'Total Volume': 'sum'}).reset_index()

# convert the dat into datetime
avocadoDataFrame['Date'] = pd.to_datetime(avocadoDataFrame['Date'])
avocadoDataFrame = avocadoDataFrame.sort_values('Date')

availableCities = sorted(avocadoDataFrame['region'].unique())
availableAvocadoTypes = sorted(avocadoDataFrame['type'].unique())

# print("\nAvailable cities to forecast prices: ")
# print("|".join(availableCities[:10]), "...")

# print("\nAvailable types of avocado's to forecast prices: ")
# print("|".join(availableAvocadoTypes[:10]), "...")

# anotherForecast = True

# while anotherForecast == True:
    
#     city = input("From the selection above enter the city you would like to see predictions for: ").strip().lower()
#     avocadoType = input("From the selection above enter the type of avocado you would like to see predictions for: ").strip().lower()

#     forecastPriceByCityAndType(city, avocadoType)

#     promptUserAgain = input("Would you like to forecast another city? Type Y for yes and N for No: ").strip().lower()

#     if promptUserAgain == 'y':
#         anotherForecast = True
#     else:
#         anotherForecast = False





