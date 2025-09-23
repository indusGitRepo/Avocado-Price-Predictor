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

import statsmodels.api as sm # for estimating relationships between variables

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

# Doing prediction just for the city Albany and the type of avaocado will be conventional
city = "Albany"
avocadoType = "conventional"

citiesData = avocadoDataFrame[(avocadoDataFrame['region'] == city) & (avocadoDataFrame['type'] == avocadoType)]

# date will be the index
citiesData = citiesData.set_index('Date')

# set the dependent variable (the one that we will be predicting) which is going to be the price
y = citiesData['AveragePrice']

# ARIMA model from statsmodels' time series analysis (TSA) where y is the target variable (average price for one city)
# the order is has the following paramaters -> first - autoregressive terms (looking one week back to see how the previous price influences current price)
# the second paramater is the differencing (takes the difference in price between consecutive weeks)
# the third paramater is the moving average term (difference between predicted and actual last week value)
model = sm.tsa.ARIMA(y, order=(1,1,1))
results = model.fit()

print(results.summary())

# Forecast 520 weeks ahead (10 years)
forecast = results.get_forecast(steps=520)

# extract the predicted prices from the forecast and apply it to the predicted mean (predicted prices)
forecastMean = forecast.predicted_mean

# confidence interval for each forecasted value (uncertain ranges)
forecastConfidenceInterval = forecast.conf_int()

plt.figure(figsize=(14,6))
plt.plot(y, label='Historical')
plt.plot(forecastMean, label='Forecast', color='red')
plt.fill_between(forecastConfidenceInterval.index,
                 forecastConfidenceInterval.iloc[:,0],
                 forecastConfidenceInterval.iloc[:,1], color='pink', alpha=0.3)
plt.title(f"Avocado Price Forecast ({city}, {avocadoType})")
plt.xlabel("Date")
plt.ylabel("Average Price")
plt.legend()
plt.show()


# averagePricePerYearPerCity['log_price'] = np.log(averagePricePerYearPerCity['AveragePrice'])
# averagePricePerYearPerCity['log_volume'] = np.log(averagePricePerYearPerCity['Total Volume'])

# # declare a list that will store elasticity for price and volume by region
# elasticity = []

# # go through each region 
# for region, group in averagePricePerYearPerCity.groupby('region'):

#     # the logged price is the independent variable x and sm.add_constant is used to add an intercept to the model
#     x = sm.add_constant(group['log_price'])

#     # dependent variable because it is what will be predicted based on price
#     y = group['log_volume']

#     # create an OLS regression model to predict the volume for the linear regression model "line of best fit" and the .fit() also estimates slope and intercept
#     model = sm.OLS(y, x).fit()

#     # model.parms represents the slope of the line and that elasticity value will be added to the elasticity list alongside the region name
#     elasticity.append({"region": region, "elasticity": model.params['log_price']})

# # convert the list into a dataframe to do data manipulation more easily
# elasticityDataFrame = pd.DataFrame(elasticity)

# # print the first few results
# print(elasticityDataFrame.head())

# # sort elasticity values from smallest to largest and plot the results using a bar graph
# elasticityDataFrame.sort_values('elasticity').plot(
#     x='region', y='elasticity', kind='bar', figsize=(12,6), legend=False
# )

# # adding a horizontal line at y=0 to see if there are any negative values
# plt.axhline(0, color='black', linestyle='--')

# plt.title("USA Avacado Price Elasticity by Region")

# plt.ylabel("Elasticity")
# plt.show()




# # Elascity for Albany









# axis = averagePricePerYearPerCity.T.plot(marker='o', figsize=(14,8))

# axis.set_title("Average Avocado Price Per Year in Major US Cities")
# axis.set_xlabel('Year')
# axis.set_ylabel('Average Price')

# axis.legend(title="Major US Cities", title_fontsize=12, fontsize=10, loc="upper left", ncol=2)

# plt.grid(True)
# plt.tight_layout()
# plt.style.use('seaborn-v0_8-colorblind')
# plt.show()


