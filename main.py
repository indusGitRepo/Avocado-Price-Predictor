import kaggle

# import the pandas library to work with and manipulate avocado data
import pandas as pd

Print every value to 3 decimal places
pd.set_option('display.float_format', '{:.3f}'.format)

# store the data from avocado.csv into the following variable
avocadoDataFrame = pd.read_csv('avocado.csv', index_col=0)

print("Overview of columns and data: ")
avocadoDataFrame.info()

print("Overview of stats for Date: ")
print(avocadoDataFrame['Date'].describe())

print("Overview of stats for the Average Prices: ")
print(avocadoDataFrame['AveragePrice'].describe())

print("Overview of stats for the Year: ")
print(avocadoDataFrame['year'].describe())
