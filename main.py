# the dataset contains average price for a single avocado that week across major US cities, the total # of avocados sold that week in that city, 
# the total number of 4046, 4225, and 4770 avocados sold in that city, total bags, total small bags, total large bags, and total x-large bags sold in that city that week,
# and if the type of avocado was conventional or organic, the year, and the US city. This data is from 2015-2018.

# I want to get rid of some columns that seem redundant/unnessecary...

# year, average price for that year per city, total volume for that year per city, type 


import kaggle

# import the pandas library to work with and manipulate avocado data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Print every value to 3 decimal places
pd.set_option('display.float_format', '{:.3f}'.format)

# store the data from avocado.csv into the following variable
avocadoDataFrame = pd.read_csv('avocado.csv', index_col=0)
avocadoDataFrame['Date'] = pd.to_datetime(avocadoDataFrame['Date'])

avocadoDataFrame['year'] = avocadoDataFrame['Date'].dt.year

averagePricePerYearPerCity = avocadoDataFrame.groupby(['region', 'year'])['AveragePrice'].mean()
print(averagePricePerYearPerCity.unstack())

# print("Overview of columns and data: ")
# avocadoDataFrame.info()

# print("Overview of stats for Date: ")
# print(avocadoDataFrame['Date'].describe())

# print("Overview of stats for the Average Prices: ")
# print(avocadoDataFrame['AveragePrice'].describe())

# print("Overview of stats for the Year: ")
# print(avocadoDataFrame['year'].describe())

# avocadoDataFrame.plot()
# plt.show()

averagePricePerYearPerCity.T.plot(figsize=(15,8))

plt.title('Average Avocado Price Per Year in Major US Cities')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.style.use('seaborn-v0_8-colorblind')
plt.show()
