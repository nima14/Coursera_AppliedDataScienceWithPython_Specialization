
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **sports or athletics** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **sports or athletics**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **sports or athletics**?  For this category we are interested in sporting events or athletics broadly, please feel free to creatively interpret the category when building your research question!
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[ ]:

#https://www.kaggle.com/unsdsn/world-happiness?select=2016.csv
#http://hdr.undp.org/en/data
import sys
get_ipython().system('{sys.executable} -m pip install --upgrade nbformat;')


# In[2]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
# !{sys.executable} -m pip install plotly;
import plotly.express as px

get_ipython().magic('matplotlib notebook')

#Read Education
Edu_df=pd.read_csv("Data_Project/Education index.csv")

#Get the neccessary columns & remove unnecessary records
ColNames=list( Edu_df.columns[Edu_df.columns.str.match('^[0-9]+') ] )

ColNames.insert(0, "Country")
Edu_df=Edu_df[ColNames]
Edu_df= Edu_df.iloc[1:]
Edu_df
Edu_df=pd.melt(Edu_df,id_vars="Country", 
                var_name="Year", 
                value_name="Education_Rate")

Edu_df['Country']=Edu_df['Country'].str.strip()
Edu_df['Year']=pd.to_numeric(Edu_df['Year']) 

Edu_df=Edu_df[Edu_df['Year']>=2015]

years=[2015,2016,2017,2018]

#Read GDP & Happiness Index
    
    
file_name_prefix="Data_Project/datasets_894_813759_"


GDP_2015=pd.read_csv(file_name_prefix+'2015'+'.csv')
GDP_2015=GDP_2015[['Country','Happiness Score','Economy (GDP per Capita)']]
GDP_2015['Year']=2015
GDP_2015.columns=['Country','HappinessScore','GDP_per_Capita','Year']

GDP_2016=pd.read_csv(file_name_prefix+'2016'+'.csv')
GDP_2016=GDP_2016[['Country','Happiness Score','Economy (GDP per Capita)']]
GDP_2016['Year']=2016
GDP_2016.columns=['Country','HappinessScore','GDP_per_Capita','Year']


GDP_2017=pd.read_csv(file_name_prefix+'2017'+'.csv')
GDP_2017=GDP_2017[['Country','Happiness.Score','Economy..GDP.per.Capita.']]
GDP_2017['Year']=2017
GDP_2017.columns=['Country','HappinessScore','GDP_per_Capita','Year']

GDP_2018=pd.read_csv(file_name_prefix+'2018'+'.csv')
GDP_2018=GDP_2018[['Overall rank','Country or region','Score','GDP per capita']]
GDP_2018['Year']=2018
GDP_2018.columns=['rank','Country','HappinessScore','GDP_per_Capita','Year']


#Filter records in GDPs
GDP_2018=GDP_2018[GDP_2018['rank']<=20]
GDP_2018=GDP_2018[['Country','HappinessScore','GDP_per_Capita','Year']]


GDP_2015=GDP_2015[GDP_2015['Country'].isin(GDP_2018['Country'])]
GDP_2016=GDP_2016[GDP_2016['Country'].isin(GDP_2018['Country'])]
GDP_2017=GDP_2017[GDP_2017['Country'].isin(GDP_2018['Country'])]


#Combine different DFs
GDP_df=GDP_2018.append([GDP_2015,GDP_2016,GDP_2017])

df=GDP_df.merge(Edu_df,on=['Country','Year'])
df=df.sort_values(by=['Year'])

continents = {'Finland': 'Europe(Scandinavia)',
               'Norway':'Europe(Scandinavia)',
             'Denmark': 'Europe(Scandinavia)',
              'Iceland': 'Europe(Scandinavia)',
              'Switzerland': 'Europe',
              'Netherlands': 'Europe',
              'Canada': 'North America',
              'New Zealand': 'Oceania',
              'Sweden': 'Europe(Scandinavia)',
              'Australia': 'Oceania',
              'United Kingdom': 'Europe',
              'Austria': 'Europe',
              'Costa Rica': 'Central America',
              'Ireland': 'Europe',
              'Germany': 'Europe',
              'Belgium': 'Europe',
              'Luxembourg': 'Europe',
              'United States': 'North America',
              'Israel': 'Asia',
              'United Arab Emirates':'Asia'
             }

colors={'Europe(Scandinavia)':'cyan',
       'Europe':'coral',
       'North America':'slategrey',
       'Oceania':'hotpink',
        'Central America':'orange',
        'Asia':'yellowgreen'
       }
countries={'United Arab Emirates':'UAE',
           'United Kingdom':'UK',
           'United States':'USA'
           }
 
df['Education_Rate']=df['Education_Rate'].astype('float64')
df['Continent']=df['Country'].map(continents)
df['Color']=df['Continent'].map(colors)
df['Country']=df['Country'].replace(countries)



px.scatter(df, x="Education_Rate", y="HappinessScore", animation_frame="Year", animation_group="Country"
           ,size="GDP_per_Capita", color="Continent", hover_name="Country",
           range_x=[0.7,1], range_y=[6.5,7.8], opacity=0.7,
           title="GDP,Happiness Index & Education Rate in Different Years",
            labels={
                     "Education_Rate": "Education Rate",
                     "HappinessScore": "Happiness Score",
                     "Continent": "Continent"
                 }
           
           )





