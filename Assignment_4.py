
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


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

# In[ ]:





# In[2]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind
    import re

    # Use this dictionary to map state names to two letter acronyms
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


    state_names = [];
    for key in states : 
        print(key, states[key])
        state_name = states[key]
        state_names.append(state_name)


    df = pd.read_csv('university_towns.txt', sep='\t', lineterminator='\r',header = None)
    df = re.sub("\(.*\)","",df[0][0])
    #df = re.sub("\[.*\]","",df[0][0])
    df = df.splitlines()
    df = pd.DataFrame(df)
    df.columns = ['Name']

    #df['City'] = []    

    df['State'] = df[df['Name'].str.contains("edit")]
    df['Name'] = df[~df['Name'].str.contains("edit")]

    for i in range(1, len(df)):
        if pd.isnull(df.loc[i]['State']): 
            df.loc[i]['State'] = df.loc[i-1]['State'] 

    df = df.dropna()
    #https://stackoverflow.com/questions/20894525/how-to-remove-parentheses-and-all-data-within-using-pandas-python
    df['Name'] = df['Name'].str.replace(r"\[.*\]","")  
    df['State'] = df['State'].str.replace(r"\[.*\]","")

    #https://stackoverflow.com/questions/53141240/pandas-how-to-swap-or-reorder-columns
    cols = list(df.columns)
    a, b = cols.index('State'), cols.index('Name')
    cols[b], cols[a] = cols[a], cols[b]
    df = df[cols]

    df.columns = ['State','RegionName']
    return df


# In[3]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    recession_start = df1[(df1['Difference'].shift(1)>0) & (df1['Difference']<0) & (df1['Difference'].shift(-1)<0)]
    recession_start = recession_start.dropna()   
    return recession_start['Quarter']
    


# In[4]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    recession_end = df1[(df1['Difference'].shift(1)<0) & (df1['Difference'].shift(2)<0) 
                & (df1['Difference']>0) & (df1['Difference'].shift(-1)>0)]
    recession_end = recession_end.dropna()      
    return recession_end['Quarter']  
    


# In[5]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    recession_period = df1.loc[recession_start.index[0]:recession_end.index[0],:]
    recession_min = recession_period['Difference'].idxmin()
    recession_bottom = df1.loc[recession_min,:]['Quarter']
    return recession_bottom


# In[6]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    
    df2 = pd.read_csv('City_house_price.csv')
    #https://www.geeksforgeeks.org/how-to-drop-one-or-multiple-columns-in-pandas-dataframe/
    df2 = df2.drop(df2.loc[:,'1996-01-31':'1999-12-31'].columns,axis=1)
    df2 = df2.drop(df2.loc[:,'2016-10-31':].columns,axis=1)
    df2 = df2.drop(['RegionID','SizeRank','RegionType','StateName','Metro','CountyName'],axis=1)
    df2.set_index(['State', 'RegionName'],inplace=True)
    df2 = df2.dropna()
    #df2.sort_index(inplace=True)
    df2.columns = pd.to_datetime(df2.columns)
    #df2.columns = pd.PeriodIndex(df2.columns, freq='Q')
    #df2_up = df2.groupby((np.arange(len(df2.columns)) // 3) + 1, axis=1).sum()
    #https://stackoverflow.com/questions/40497199/how-to-convert-monthly-data-to-quarterly-in-pandas
    df2_up = df2.groupby(pd.PeriodIndex(df2.columns, freq='Q'), axis=1).mean()
    return df2_up


# In[7]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    df3=df.copy(deep=True)
    states_new = {v: k for k, v in states.items()}
    df3['State']= df3['State'].map(states_new) 
    #df3["Unique"] = df3["State"][~df3["State"].isin(df2["State"])]
    #df2_up["Unique"] = df2_up["RegionName"][~df2_up["RegionName"].isin(df3["RegionName"])]

    uni = pd.merge(df2_up, df3, how='right', left_index=True, right_index=True,
                           on=['RegionName','State'])
    uni.dropna()

    non_uni = df2_up[~df2_up['RegionName'].isin(df3['RegionName'])]
    #non_uni = df2_up.loc[~((df2_up.State.isin(df3['State']))&(df2_up.RegionName.isin(df3['RegionName']))),:]

    recession_start = recession_start.iloc[0] 
    recession_start = pd.to_datetime(recession_start).to_period('Q')
    recession_bottom = pd.to_datetime(recession_bottom).to_period('Q')
    before_recession = before_recession.iloc[0]
    before_recession = pd.to_datetime(before_recession).to_period('Q')
    #
    uni_recession = uni.loc[:,before_recession:recession_bottom]
    uni_recession['price_ratio'] = uni_recession.loc[:,before_recession]/uni_recession.loc[:,recession_bottom]
    non_uni_recession = non_uni.loc[:,before_recession:recession_bottom]

    stat,p_value = ttest_ind(uni_recession['price_ratio'], non_uni_recession['price_ratio'])
    if p_value>.01:
        x = min(uni_recession['price_ratio'].mean,non_uni_recession['price_ratio'].mean)
    else: x = None
    return stat,p,x


# In[ ]:




