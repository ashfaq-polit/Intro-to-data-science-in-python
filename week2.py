
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # The Series Data Structure

# In[1]:


import pandas as pd
get_ipython().magic('pinfo pd.Series')


# In[3]:


animals = ['Tiger', 'Bear', 'Moose']
pd.Series(animals)


# In[4]:


numbers = [1, 2, 3]
pd.Series(numbers)


# In[5]:


animals = ['Tiger', 'Bear', None]
pd.Series(animals)


# In[6]:


numbers = [1, 2, None]
pd.Series(numbers)


# In[2]:


import numpy as np
np.nan == None


# In[8]:


np.nan == np.nan


# In[10]:


np.isnan(np.nan)


# In[11]:


sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[12]:


s.index


# In[13]:


s = pd.Series(['Tiger', 'Bear', 'Moose'], index=['India', 'America', 'Canada'])
s


# In[14]:


sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports, index=['Golf', 'Sumo', 'Hockey'])
s


# # Querying a Series

# In[15]:


sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[17]:


s.iloc[3]


# In[16]:


s.loc['Golf']


# In[18]:


s[3]


# In[19]:


s['Golf']


# In[20]:


sports = {99: 'Bhutan',
          100: 'Scotland',
          101: 'Japan',
          102: 'South Korea'}
s = pd.Series(sports)


# In[22]:


s.iloc[0] #This won't call s.iloc[0] as one might expect, it generates an error instead


# In[5]:


s = pd.Series([100.00, 120.00, 101.00, 3.00])
s


# In[24]:


total = 0
for item in s:
    total+=item
print(total)


# In[2]:


import numpy as np

total = np.sum(s)
print(total)


# In[26]:


#this creates a big series of random numbers
s = pd.Series(np.random.randint(0,1000,10000))
s.head()


# In[27]:


len(s)


# In[6]:


get_ipython().run_cell_magic('timeit', '-n 100', 'summary = 0\nfor item in s:\n    summary+=item')


# In[7]:


get_ipython().run_cell_magic('timeit', '-n 100', 'summary = np.sum(s)')


# In[8]:


s+=2 #adds two to each item in s using broadcasting
s.head()


# In[9]:


for label, value in s.iteritems():
    s.set_value(label, value+2)
s.head()


# In[14]:


get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\nfor label, value in s.iteritems():\n    s.loc[label]= value+2')


# In[11]:


get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\ns+=2')


# In[15]:


s = pd.Series([1, 2, 3])
s.loc['Animal'] = 'Bears'
s


# In[16]:


original_sports = pd.Series({'Archery': 'Bhutan',
                             'Golf': 'Scotland',
                             'Sumo': 'Japan',
                             'Taekwondo': 'South Korea'})
cricket_loving_countries = pd.Series(['Australia',
                                      'Barbados',
                                      'Pakistan',
                                      'England'], 
                                   index=['Cricket',
                                          'Cricket',
                                          'Cricket',
                                          'Cricket'])
all_countries = original_sports.append(cricket_loving_countries)


# In[17]:


original_sports


# In[18]:


cricket_loving_countries


# In[19]:


all_countries


# In[20]:


all_countries.loc['Cricket']


# # The DataFrame Data Structure

# In[ ]:


import pandas as pd
purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})
df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
df.head()


# In[ ]:


df.loc['Store 2']


# In[ ]:


type(df.loc['Store 2'])


# In[ ]:


df.loc['Store 1']


# In[ ]:


df.loc['Store 1', 'Cost']


# In[ ]:


df.T


# In[ ]:


df.T.loc['Cost']


# In[ ]:


df['Cost']


# In[ ]:


df.loc['Store 1']['Cost']


# In[ ]:


df.loc[:,['Name', 'Cost']]


# In[ ]:


df.drop('Store 1')


# In[ ]:


df


# In[ ]:


copy_df = df.copy()
copy_df = copy_df.drop('Store 1')
copy_df


# In[ ]:


get_ipython().magic('pinfo copy_df.drop')


# In[ ]:


del copy_df['Name']
copy_df


# In[ ]:


df['Location'] = None
df


# # Dataframe Indexing and Loading

# In[ ]:


costs = df['Cost']
costs


# In[ ]:


costs+=2
costs


# In[ ]:


df


# In[3]:


get_ipython().system('cat olympics.csv')


# In[4]:


df = pd.read_csv('olympics.csv')
df.head()


# In[5]:


df = pd.read_csv('olympics.csv', index_col = 0, skiprows=1)
df.head()


# In[6]:


df.columns
for col in df.columns:
    print(col)


# In[13]:


for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold' + col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver' + col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze' + col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#' + col[1:]}, inplace=True) 

df=df.drop('Totals')

df = df.drop(df['Gold'])
df.head()


# # Querying a DataFrame

# In[19]:


df['Gold'] > 0

df[df['Gold']==df['Gold'].max()].index

df[abs(df['Gold']-df['Gold.1'])==abs(df['Gold']-df['Gold.1']).max()].index



# In[8]:



df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
df[abs(df['Gold']-df['Gold.1'])/df['Gold.2']==abs(df['Gold']-df['Gold.1'])/df['Gold.2'].max()].index


# In[15]:



df['Gold']


# In[11]:


df['Gold'].count()
df.count()


# In[18]:


only_gold = df.dropna()
only_gold.head()
only_gold.count()

df.Series = [];
for i in df.index:
    Points = df['Gold.2'][i]*3 + df['Silver.2'][i]*2 + df['Bronze.2'][i]*1
    df.Series.append(Points)
df.Series


# In[13]:


only_gold = df[df['Gold'] > 0]
only_gold.head()


# In[39]:


len(df[(df['Gold'] > 0) | (df['Gold.1'] > 0)])


# In[40]:


df[(df['Gold.1'] > 0) & (df['Gold'] == 0)]


# # Indexing Dataframes

# In[14]:


df.head()


# In[15]:


df['country'] = df.index
df = df.set_index('Gold')
df.head()


# In[16]:


df = df.reset_index()
df.head()


# In[1]:


import pandas as pd
df = pd.read_csv('census.csv')
df.head()


# In[6]:


import numpy as np
state = df['STNAME'].unique()
state
len(state)
            
count = np.zeros(len(state))
count

max_county = df['STNAME'].value_counts()
max_county




       


# In[6]:


df=df[df['SUMLEV'] == 50]
df.head()


# In[44]:


columns_to_keep = ['STNAME',
                   'CTYNAME',
                   'BIRTHS2010',
                   'BIRTHS2011',
                   'BIRTHS2012',
                   'BIRTHS2013',
                   'BIRTHS2014',
                   'BIRTHS2015',
                   'POPESTIMATE2010',
                   'POPESTIMATE2011',
                   'POPESTIMATE2012',
                   'POPESTIMATE2013',
                   'POPESTIMATE2014',
                   'POPESTIMATE2015']
df = df[columns_to_keep]
df.head()


# In[41]:


A=[]
for i in range(len(state)):
    select_state = df.loc[df['STNAME'] == state[i]] 
    top_three = select_state.sort(['CENSUS2010POP'], ascending=[False]).head(3).sum()
    top_three['CENSUS2010POP']
    A.append(top_three['CENSUS2010POP'])

pd.Series(A)
ind = A.index(max(A))

state[ind]




# In[77]:


max_cty = df[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']]
max_cty

resultmax = df.loc[:, max(["POPESTIMATE2010", "POPESTIMATE2011","POPESTIMATE2012","POPESTIMATE2013","POPESTIMATE2014","POPESTIMATE2015"])]
               
resultmin = df.loc[:, min(["POPESTIMATE2010", "POPESTIMATE2011","POPESTIMATE2012","POPESTIMATE2013","POPESTIMATE2014","POPESTIMATE2015"])]
               
resultmin

diff = abs(resultmax - resultmin)
diff
diff.idxmax()

cty = df["CTYNAME"]
cty[diff.idxmax()]

   
A = df[df['CTYNAME'].str.startswith("Washington")]
A

B = A[(A['REGION'] == 2) | (A['REGION'] == 1)]
B

C = B[(B['POPESTIMATE2015']-B['POPESTIMATE2014'])>0]
C

C[['STNAME','CTYNAME']]





# In[47]:


df.loc['Michigan', 'Washtenaw County']
df = df.set_index(['STNAME','CTYNAME'])
df.head()

df.loc[ [('Michigan', 'Washtenaw County'),
         ('Michigan', 'Wayne County')] ]


# # Missing values

# In[20]:


df = pd.read_csv('log.csv')
df


# In[53]:


census_df.sort(['STNAME', 'CENSUS2010POP'], ascending=[True, False])

unique = census_df['STNAME'].unique()

unique

for i in range(len(unique)):
    locate = df.loc[df['STNAME'] == unique[i], 'CENSUS2010POP'].sum()

locate



# In[21]:


df = df.set_index('time')
df = df.sort_index()
df


# In[22]:


df = df.reset_index()
df = df.set_index(['time', 'user'])
df


# In[23]:


df = df.fillna(method='ffill')
df.head()


# In[ ]:




