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

avocadoDataFrame = pd.read_csv('avocado.csv', index_col=0)

cleanData = ['year', 'AveragePrice', 'Total Volume', 'type', 'region']

# store the data from avocado.csv into the following variable
avocadoDataFrame = avocadoDataFrame[cleanData].copy()
#avocadoDataFrame['Date'] = pd.to_datetime(avocadoDataFrame['Date'])

#avocadoDataFrame['year'] = avocadoDataFrame['Date'].dt.year

averagePricePerYearPerCity = avocadoDataFrame.groupby(['region', 'year', 'type']).agg({'AveragePrice': 'mean', 'Total Volume': 'sum'}).reset_index()

#averageForEachRegionAllYears = averagePricePerYearPerCity.mean(axis=1)

print(averagePricePerYearPerCity)

# albanymean = avocadoDataFrame[(avocadoDataFrame['region'] == 'Albany') & (avocadoDataFrame['year'] == 2015) & (avocadoDataFrame['type'] == 'conventional')]
# result = albanymean['AveragePrice'].mean()
# print("it issssssssssssss")
# print(result)
# print("\nTotal Average \n")

# dummy = averageForEachRegionAllYears.reset_index()
# dummy.columns = ('Region', 'Average Price')

# midPoint = len(dummy) // 2 + len(dummy) % 2
# leftHalf = dummy.iloc[:midPoint].reset_index(drop=True)
# rightHalf = dummy.iloc[midPoint:].reset_index(drop=True)

# leftHalf.columns = ['Region', 'Average Price']
# rightHalf.columns = ['Region', 'Average Price']

# splitDisplay = pd.concat([leftHalf, rightHalf], axis=1)
# print(splitDisplay)

# # print("Overview of columns and data: ")
# # avocadoDataFrame.info()

# # print("Overview of stats for Date: ")
# # print(avocadoDataFrame['Date'].describe())

# # print("Overview of stats for the Average Prices: ")
# # print(avocadoDataFrame['AveragePrice'].describe())

# # print("Overview of stats for the Year: ")
# # print(avocadoDataFrame['year'].describe())

# # avocadoDataFrame.plot()
# # plt.show()

# for i in range(54):


# axis = averagePricePerYearPerCity.T.plot(marker='o', figsize=(14,8))

# axis.set_title("Average Avocado Price Per Year in Major US Cities")
# axis.set_xlabel('Year')
# axis.set_ylabel('Average Price')

# axis.legend(title="Major US Cities", title_fontsize=12, fontsize=10, loc="upper left", ncol=2)

# plt.grid(True)
# plt.tight_layout()
# plt.style.use('seaborn-v0_8-colorblind')
# plt.show()


