# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:11:29 2020

@author: NurhanPam2012
"""

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pandas as pd
#import pandas_datareader.data as web
import csv
import time
from datetime import datetime
from random import uniform, randint
import requests
import itertools

# Randimization
MIN_RAND = 1.03
MAX_RAND = 2.54
LONG_MIN_RAND = 20
LONG_MAX_RAND = 30

def smallSleep():
    rand = uniform(MIN_RAND, MAX_RAND)
    time.sleep(rand)

def longSleep():
    rand = uniform(LONG_MIN_RAND, LONG_MAX_RAND)
    time.sleep(rand)



headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Accept-Encoding': 'identity'
}
#'Accept-Encoding': 'identity'
#create DataFrame
df_collection=pd.DataFrame(columns = ['Price','Address','Bedrooms','Bathroom','Square_Footage'])
#df2_collection=pd.DataFrame(columns = ['Price','Address','Bedrooms','Bathroom','Square_Footage'])
city = input('What URL do you want to scrape? (ex:https://www.realtor.com/realestateandhomes-search/Pleasanton_CA/sby-6) \n')

for pageNumber in range(3):
    print("--- Grabbing Page {} ---".format(pageNumber))

    # if (pageNumber%2) == 0:
    # 	if pageNumber != 0:
    # 		time.sleep(30)
    smallSleep()

    if (pageNumber%2) == 0 and pageNumber != 0:
        longSleep()

#    url = "https://www.realtor.com/realestateandhomes-search/Pleasanton_CA/sby-6"

    if pageNumber == 0:
        continue
    elif pageNumber == 1:
#        url = "https://www.realtor.com/realestateandhomes-search/Pleasanton_CA/sby-6"
        url = str(city)
    else:
#        url = "https://www.realtor.com/realestateandhomes-search/Pleasanton_CA/sby-6/pg-{}".format(pageNumber)
        url = str(city)+"/pg-{}".format(pageNumber)
    
    print(url)
    longSleep()
    #get_proxies()
    #if (pageNumber%5)==0:
        #get_proxies()
    #elif pageNumber==1:
        #get_proxies()
    #else:
        #continue

    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'lxml')
    #Create a DataFrame object
    
    for item in soup.select('.component_property-card'):
    
        try:
            print('**********')
            price=(item.select('[data-label=pc-price]')[0].get_text())
            smallSleep()
            address=(item.select('[data-label=pc-address]')[0].get_text())
            smallSleep()
            bbs=(item.select('.property-meta')[0].get_text())
            extbed='bed'
            smallSleep()
            bed = (bbs[:bbs.find(extbed) + len(extbed)])
            extbath='bath'
            smallSleep()
            bath= (bbs[bbs.find(extbed) + len(extbed):bbs.find(extbath) + len(extbath)])
            sqft=(bbs[bbs.find(extbath) + len(extbath):])
            #features=(item.select('.special-feature-list')[0].get_text())
            #smallSleep()
            df_collection= df_collection.append({'Price' : price , 'Address' : address, 'Bedrooms' : bed, 'Bathroom' : bath, 'Square_Footage' : sqft
                                             } , ignore_index=True)#repeats every 20
            print(item.select('[data-label=pc-price]')[0].get_text())
            print(item.select('[data-label=pc-address]')[0].get_text())
            print(item.select('img')[0]['data-src'])
            print(item.select('.summary-wrap')[0].get_text())
            print(item.select('.address')[0].get_text())
            print(item.select('.property-meta')[0].get_text())
            #print(item.select('.special-feature-list')[0].get_text())
            #df2_collection=df2_collection.append(df_collection,ignore_index = True)#1 1,1,2 1,1,2,3
            #df_collection = df_collection[0:0]
        except Exception:
            print('error printing')
    
        #df2_collection=df2_collection.append(df_collection,ignore_index = True) Gives out a repeating pattern, 1, 1,1,2  1,1,2,3
    #df2_collection=df2_collection.append(df_collection,ignore_index = True)#takes the last 20 entries and repeats them over and over,
#df2_collection=df2_collection.append(df_collection,ignore_index = True) takes last 20 entries and repeats them over and over 

writer = pd.ExcelWriter('RealEstate.xlsx')
#write dataframe to excel
df_collection.to_excel(writer)
#save to excel
writer.save()
print('Saving Dataframe to Excel file')

read = pd.read_excel('RealEstate.xlsx')
print(read)

    
