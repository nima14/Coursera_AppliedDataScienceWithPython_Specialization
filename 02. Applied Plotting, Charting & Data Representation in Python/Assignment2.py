
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[3]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[5]:

get_ipython().magic('matplotlib notebook')
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import datetime as DT
import matplotlib.dates as mdates
import numpy as np



#Read Data
data=pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

#Data Cleansing
data["Date"]=pd.to_datetime(data['Date'])

data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day
data['M-D']=data['Date'].dt.strftime('%b-%d')

    #Just to have a format like year-MonthName-Day
data['M-D']='2000-'+data['M-D']
data['M-D']=pd.to_datetime(data['M-D'])
 
    #Remove 29 Feb
data= data[-((data["Month"]==2) & (data["Day"]==29))]

#Create 2 dataFrames: Before 2015 & 2015
data2015out=data[data['Year']<2015]
data2015=data[data['Year']==2015]


#Min & Max temperature in every day before 2015 (Group By Day)
gb2015out=data2015out.groupby(['Month','Day','M-D'])["Data_Value"].agg(["min", "max"])
gb2015out.reset_index(inplace=True)

#Min & Max temperature in every day in 2015 (Group By Day)
gb2015=data2015.groupby(['Month','Day'])["Data_Value"].agg(["min", "max"])
gb2015.reset_index(inplace=True)

#Join before 2015 & 2015 dataFrame
gbAll=gb2015out.merge(gb2015,on=["Month","Day"])
gbAll.columns=["Month","Day","M-D","Min2015out","Max2015out","Min2015","Max2015"]

#Get the records which were in 2015 & were greater than max or lower than min temperature before 2015
gt2015=gbAll[gbAll["Max2015"]>gbAll["Max2015out"]][["Month","Day","Max2015","M-D"]]
gt2015.columns=["Month","Day","Temp","M-D"]

lt2015=gbAll[gbAll["Min2015"]<gbAll["Min2015out"]][["Month","Day","Min2015","M-D"]]
lt2015.columns=["Month","Day","Temp","M-D"]

Exception2015=pd.concat([gt2015,lt2015])


#plt.figure()
fig = plt.figure(figsize=(9, 4))

locator = mdates.MonthLocator()  # locator: every month
fmt = mdates.DateFormatter('%b') #show month_names

ax = fig.add_subplot(111)

ax.plot(gb2015out["M-D"],gb2015out["min"],label="Minimum Temp (2005-2014)",color='paleturquoise')
ax.plot(gb2015out["M-D"],gb2015out["max"],label="Maximum Temp (2005-2014)",color='pink')

ax.fill_between(gb2015out["M-D"].dt.to_pydatetime(),gb2015out["min"],gb2015out["max"],
                color='grey', alpha='0.3')


ax.plot(Exception2015["M-D"],Exception2015["Temp"],'o',color='black',markersize=3,label='Record Break Temps in 2015')
ax.legend(frameon=False)

X = plt.gca().xaxis


#Set locator & month_name format
X.set_major_locator(locator)
X.set_major_formatter(fmt)

plt.ylabel('Temperature (tenths of degrees C)', fontweight='bold')
plt.title('Minimum & Maximum Temperatures (2005-2014) & Extreme Temperatures In 2015', fontweight='bold')

plt.show()


# In[ ]:



