
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[18]:


def get_list_of_university_towns():
    Uni_Town=pd.read_fwf("university_towns.txt",header=None)
    IsState=Uni_Town[0].str.find("edit")>0

    Uni_Town["State"]= Uni_Town[0][IsState]
    
    replace_Dict={"[0-9]":"","edit":"","[\[]":"","[\]]":"","\(.*\)":""}

    for word,init in replace_Dict.items():
        Uni_Town[0]=Uni_Town[0].str.replace(word,init)
    
    for word,init in replace_Dict.items():
        Uni_Town["State"]=Uni_Town["State"].str.replace(word,init)


    Uni_Town[0]=Uni_Town[0].str.strip()
    Uni_Town["State"]=Uni_Town["State"].str.strip()

    Uni_Town=Uni_Town.rename(columns={0:"RegionName"})
    Uni_Town=Uni_Town.ffill()
    Uni_Town=Uni_Town[-IsState]
    

    
    return Uni_Town

get_list_of_university_towns()



# In[19]:


def get_recession_start():
    GDP=pd.read_excel("gdplev.xls",skiprows=219)
    GDP=GDP[GDP.columns[[4,6]]]
    GDP.columns=["Quarter","GDP"]

    GDP["GDP Diff"]= GDP["GDP"].diff()
    GDP.loc[GDP["GDP Diff"]<0, "Negative"]=1

    GDP["Diff_B"]=GDP["Negative"].diff()
    GDP["Diff_F"]=GDP["Negative"].diff(periods=-1)
    res=GDP[(pd.isnull(GDP["Diff_B"])) & (GDP["Diff_F"]==0)]["Quarter"]
    
    return res.to_string(index=False)

get_recession_start()


# In[ ]:





# In[20]:


def get_recession_end():
    GDP=pd.read_excel("gdplev.xls",skiprows=219)
    GDP=GDP[GDP.columns[[4,6]]]
    GDP.columns=["Quarter","GDP"]

    GDP["GDP Diff"]= GDP["GDP"].diff()
    GDP.loc[GDP["GDP Diff"]<0, "Negative"]=1
    GDP.loc[GDP["GDP Diff"]>=0, "Negative"]=0
    GDP["Diff_B"]=GDP["Negative"].diff()
    GDP["Diff_B2"]=GDP["Negative"].diff(periods=2)
    GDP["Diff_B3"]=GDP["Negative"].diff(periods=3)
    res=GDP[(GDP["Diff_B"]==0) & (GDP["Diff_B2"]==-1) & (GDP["Diff_B3"]==-1)]["Quarter"]
       
    return res.to_string(index=False)

get_recession_end()


# In[21]:


def get_recession_bottom():
    GDP=pd.read_excel("gdplev.xls",skiprows=219)
    GDP=GDP[GDP.columns[[4,6]]]
    GDP.columns=["Quarter","GDP"]
    
    start=GDP.index[GDP["Quarter"]==get_recession_start()].tolist()
    end=GDP.index[GDP["Quarter"]==get_recession_end()].tolist()
    recession=pd.DataFrame({"Start":start,"End":end})
    rec_bot=list()
    for maxidx,minidx in recession.itertuples(index=False):
        rec_bot.append(GDP.iloc[GDP.iloc[minidx:maxidx]["GDP"].idxmin()]["Quarter"] )
    return str(rec_bot[0])




get_recession_bottom() 


# In[22]:


def convert_housing_data_to_quarters():
    House= pd.read_csv("City_Zhvi_AllHomes.csv")
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    House["State"]=House["State"].map(states)

    months=[['01','02','03'],['04','05','06'],['07','08','09'],['10','11','12']]
    months_2016=[['01','02','03'],['04','05','06'],['07','08']]

    for year in  [str(x) for x in list(range(2000,2016))] :
        for month in months :
            col = [ year+"-"+month[0],year+"-"+month[1],year+"-"+month[2] ]       
            House[year+"q"+str(months.index(month)+1)] =House[col].mean(axis=1)

    for month in months_2016 :
 
        if months_2016.index(month)==2:
           col = [ "2016-"+month[0],"2016-"+month[1] ] 
           House["2016q"+str(months_2016.index(month)+1)] =House[col].mean(axis=1)
        else:
            col = [ "2016-"+month[0],"2016-"+month[1],"2016-"+month[2] ] 
            House["2016q"+str(months_2016.index(month)+1)] =House[col].mean(axis=1)
  

    House=House.iloc[: ,list(range(1,3)) + list(range(251,318))   ]
    House.set_index(["RegionName","State"],inplace=True)

    
    return House

convert_housing_data_to_quarters()


# In[32]:





# In[23]:


def run_ttest():
    bottom=get_recession_bottom()
    start=get_recession_start()

    House=convert_housing_data_to_quarters()
    House_diff=(House[bottom]-House[start]).to_frame()
    House_diff.reset_index(inplace=True)

    Uni_town=get_list_of_university_towns()

    merged = pd.merge(House_diff, Uni_town,how="outer", on=['RegionName','State'],indicator=True)


    uni=merged.query('_merge == "both"')
    non_uni=merged.query('_merge == "left_only"')

    #uni[:,0:2]#.columns=["RegionName","State","Diff"]
    t,p = ttest_ind(uni[0].dropna(),non_uni[0].dropna())
    different=True if p<0.01 else False
    better="university town" if uni[0].mean()>non_uni[0].mean() else "non-university town"
    
    return (different, p, better)




run_ttest()

