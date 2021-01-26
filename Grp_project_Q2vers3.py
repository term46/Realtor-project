# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:36:04 2020

@author: Stephen
"""

import numpy as np
import pandas as pd
import os
import re
from pandas import DataFrame
from scipy import stats

os.chdir('C:/Users/Stephen/Desktop/BAN 612/Project')

file = pd.read_csv('data.csv')

#DATA CLEANSING PROCEDURES----------------------------------------------------

#Code for the types of data present in the DataFrame
#dataTypeSeries = file.dtypes
#print(dataTypeSeries)
#code to check datatype for file2
#dataTypeSeries2 = pleasanton.dtypes
#print(dataTypeSeries2)

#copy of dataframe for testing purposes
#file2 = file.copy()

#INDEX 236 value missing

#removing the houses listed multiple times
file = file.drop_duplicates(subset=None, keep='first', inplace=False)

#removing the space in the column names
file.columns = file.columns.map(lambda x: x.replace(' ', ''))

#code to strip the $,space and comma from the dataset
file['price'] = file['price'].str.strip('$')
file['price'] = file['price'].str.strip(' ')
file['total'] = file['total'].str.strip('$')
file['total'] = file['total'].str.strip(' ')

#code to remove the commas from all commas
file = file.replace(',','', regex=True)

#code to remove commas from just a particular column
file['price'] = file.price.replace(',','',regex=True)
file['total'] = file.total.replace(',','',regex=True)

#code to convert a column to a float/int
file['price'] = file.price.astype(float)
file['total'] = file.total.astype(float)
file['total'] = file.total.astype(int)

#Taking the "Current" and "2019" house prices from the collateral column and splitting it then appending it into the file-----------------------------------------------------------
#test = file_cleaned.copy() #copying the dataframe for testing purposes
file['Collateral'] = file['Collateral'].str.replace('$','') #removing the $ symbol
file2 = file['Collateral'] #saving the file as just the collateral column
file2 = file2.dropna(axis=0)#removes the nan values from the file
file2_df = file2.apply(lambda x: pd.Series(x.split(' '))) #splitting into 3 columns and dividing by the space
file2_df.rename(columns={0:'Current',1:'2015',2:'C2019'},inplace=True) #renaming the 3 new rows
Current = file2_df[['Current']] #dataframe with just the current house prices
house_price_2019 = file2_df[['C2019']] #Dataframe with just the calculation for what the house is worth in 2019
#merging the Current and 2019 house prices from the Collateral column into a separate column
file = file.join(house_price_2019) #merging the 2019 house prices to the file 
file = file.join(Current) #merging the current house price to the file
file= file.dropna(subset=['Current']) #looking at column called current and removing the 'nan' values from the whole dataframe
file= file.dropna(subset=['C2019']) #Removing the 'nan' values from the file
file['Current'] = file.Current.astype(int) #changing data type of 'Current' column to integer
file['C2019'] = file.C2019.astype(int) #changing data type of '2019' column to integer

#Create a box plot to remove the outliers-------------------------------------
file.boxplot(column='total') #to see if there are outliers
#removed the outliers with a z-score above 3.0
file['z_score']=stats.zscore(file['total'])
file_cleaned = file.loc[file['z_score'].abs()<=3]

#Condo lot size to 0
file.lot[file['type']=='Condo']=0
file.lot[file['type']=='Mfd/Mobile Home']=0
file.isnull().sum()
#remove random 10-Sep from elementaryschool column
file.isin(['10-Sep']).any()
file.loc[file['elementaryschool'] == '10-Sep']
file['elementary school'] = file['elementaryschool'].replace(['10-Sep'],np.nan)
#remove the word cars from the garage column
file['garage'] = file['garage'].str.replace(r'\D', '')
#fill nan values in garage with 0
file['garage'].fillna(0, inplace=True)
file = file.astype({'total' : 'int64', 'garage' : 'int32'})
#.iloc[:,[13,14,15]] = house_sample.iloc[:,[13,14,15]].astype(np.float64)

#TESTING
from sklearn.impute import SimpleImputer
#take the average of the column and fill in the missing data
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(file2.iloc[:,[2,7,13,14,15]]) #bath,built,elementary school, middle school, high school
file2.iloc[:,[2,7,13,14,15]] = imputer.transform(file2.iloc[:,[2,7,13,14,15]]).round(1)



#DATA ANALYSIS PROCEDURES-----------------------------------------------------

#filtering by city
pleasanton = file[file.city.str.contains('Pleasanton|Livermore|Dublin',case=True)]
san_mateo = file[file.city.str.contains('San Mateo', case=True)]
santa_clara = file[file.city.str.contains('Santa Clara', case=True)]
san_francisco = file[file.city.str.contains('San Francisco', case=True)]
hayward = file[file.city.str.contains('Hayward', case=True)]
oakland = file[file.city.str.contains('Oakland', case=True)]

#calculation of average sale price
pleasanton_avgsale = int(pleasanton[['total']].mean())
san_mateo_avgsale = int(san_mateo[['total']].mean())
santa_clara_avgsale = int(santa_clara[['total']].mean())
san_francisco_avgsale = int(san_francisco[['total']].mean())
hayward_avgsale = int(hayward[['total']].mean())
oakland_avgsale = int(oakland[['total']].mean())

#calculation of average square footage per city using totalprice/total sq foot
pleasanton_avgsqft = int((pleasanton['total'].sum()/pleasanton['square'].sum()))
san_mateo_avgsqft = int((san_mateo['total'].sum()/san_mateo['square'].sum()))
santa_clara_avgsqft = int((santa_clara['total'].sum()/santa_clara['square'].sum()))
san_francisco_avgsqft = int((san_francisco['total'].sum()/san_francisco['square'].sum()))
hayward_avgsqft = int((hayward['total'].sum()/hayward['square'].sum()))
oakland_avgsqft = int((oakland['total'].sum()/oakland['square'].sum()))

#calculating house price for 2019
pleasanton19= pd.DataFrame(columns=['2019new'])
pleasanton19['2019new'] = (pleasanton['total']/1.007)
pleasanton = pleasanton.join(pleasanton19)
pleasanton['2019new']= pleasanton['2019new'].astype('int')

san_mateo19= pd.DataFrame(columns=['2019new'])
san_mateo19['2019new'] = (san_mateo['total']/1.01)
san_mateo = san_mateo.join(san_mateo19)
san_mateo['2019new']= san_mateo['2019new'].astype('int')

santa_clara19= pd.DataFrame(columns=['2019new'])
santa_clara19['2019new'] = (santa_clara['total']/1.027)
santa_clara = santa_clara.join(santa_clara19)
santa_clara['2019new']= santa_clara['2019new'].astype('int')

san_francisco19= pd.DataFrame(columns=['2019new'])
san_francisco19['2019new'] = (san_francisco['total']/1.006)
san_francisco = san_francisco.join(san_francisco19)
san_francisco['2019new']= san_francisco['2019new'].astype('int')

hayward19= pd.DataFrame(columns=['2019new'])
hayward19['2019new'] = (hayward['total']/1.042)
hayward = hayward.join(hayward19)
hayward['2019new']= hayward['2019new'].astype('int')

oakland19= pd.DataFrame(columns=['2019new'])
oakland19['2019new'] = (oakland['total']/1.045)
oakland = oakland.join(oakland19)
oakland['2019new']= oakland['2019new'].astype('int')

#calculating mean % difference between 2020 listing price compared to 2019 collater predicted price
cities_df = [pleasanton, san_mateo, santa_clara, san_francisco, hayward, oakland]
cities2 = ['pleasanton','san_mateo','santa_clara','san_francisco','hayward','oakland']
meanlist = []

for city in cities_df:
    for house in city:
        city['%dif'] = abs(((city['total'] - city['Current'])/city['total'])*100)
    
    mean = city['%dif'].mean()
    meanlist.append(mean)
    
citymeans = dict(zip(cities2,meanlist))
#Affordability Calculator-----------------------------------------------------
# monthly_payment = 0
# annual_interest = 0
# insurance = 0
# loan = 0
# loan_length = 0
# house_afford = 0
# gross_month_income = 0
# down_payment = 0

# def affordability(cost2,rate2):
#     annual_interest = (rate2 / 100)/12 #rename variable to monthly interest
#     insurance = 850
#     loan = cost2*0.80
#     down_payment = cost2 * 0.20
#     #print(loan)
#     loan_length = 360
#     monthly_payment = (annual_interest * loan * ((1 + annual_interest) ** loan_length) / (((1+annual_interest) ** loan_length) - 1))+insurance
#     gross_month_income = (monthly_payment/.28) #monthly_expense = house + property tax (28% total)
#     return gross_month_income, monthly_payment, down_payment

# while True:
#     cost = input("What is the price of the house you're trying to purchase? \n")
#     try:
#         cost2 = int(cost)
#         break;
#     except:
#         print("Please input a valid price")
# while True:
#     rate = input('What is your interest percentage rate on your loan? \n')
#     try:
#         rate2 = float(rate)
#         break;
#     except:
#         print('Please input a valid interest rate: (IE: 3.03 to represent 3.03%)')
  
# a, b, c = affordability(cost2,rate2)

# print('With a down payment of 20% of the purchase price, which is: {:.2f}'.format(c),'Your gross monthly household income needs to be at least: {:.2f}'.format(a), 
#       'The monthly payment for the house you\'re looking to buy: {:.2f}'.format(b))



#Test code
# from tensorflow import keras
# input_ = keras.layers.Input(Shape=X_train.shape[1:])
# hidden1= keras.layers.Dense(30, activation='relu')(input_)
# hidden2= keras.layers.Dense(30, activation='relu')(hidden1)
# concat = keras.layers.Concatenate()([input_, hidden2])
# output = keras.layers.Dense(1)(concat)
# model = keras.Model(inputs=[input_], outputs=[output])



