# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:29:44 2020

@author: mahme026
"""

import pandas as pd
import numpy as np

file_name = "Energy_Indicators.xls" # path to file + file name
sheet =  "Energy"# sheet name or sheet number or list of sheet numbers and names

df = pd.read_excel(io=file_name, sheet_name=sheet) 

df = df.drop(df.columns[[0, 1]], axis=1) 

df = df[16:242]

df.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

df = df.reset_index(drop = True)

df['Energy Supply'] = 1000000* df['Energy Supply']

df = df.replace('\.+', np.nan, regex=True)

import re

for i in range(len(df['Country'])):
    cleaned = re.sub('\d+$', '', df['Country'][i])
    start = cleaned.find( '(' )
    end = cleaned.find( ')' )
    if start != -1 and end != -1:
        result = cleaned[0:start]
    else:
        result=cleaned
#    result = re.findall(regex, cleaned)
    df['Country'][i] = result

    
df = df.replace(['United Kingdom of Great Britain and Northern Ireland',
                 'Republic of Korea',
                 'China, Hong Kong Special Administrative Region',
                 'United States of America'],
                ['United Kingdom','Hong Kong','South Korea','United States'])

# df[df['Country'].str.match('South Korea')]
df = df.sort_values('Country', ascending=True)

energy = df

del df

df = pd.read_csv('GDP.csv', skiprows=4)

gdp = df.replace(["Korea, Rep.","Iran, Islamic Rep.","Hong Kong SAR, China"],
                ["South Korea", "Iran", "Hong Kong"])
del df

file_name1 = "scimagojr_country_rank.xlsx" # path to file + file name
sheet1 = "Sheet1"# sheet name or sheet number or list of sheet numbers and names

ScimEn = pd.read_excel(io=file_name1, sheet_name=sheet1)

merged_file = pd.merge(ScimEn, energy, how='left', left_on='Country', right_on='Country')
merged_file = pd.merge(merged_file, gdp, how='left', left_on='Country', right_on='Country Name')

merged_file = merged_file[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                           'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                           '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', 
                           '2012', '2013', '2014', '2015']]    

Top15 = merged_file[0:15]  
Top15 = Top15.set_index('Country')

entries_lost = merged_file.shape[0] - Top15.shape[0]

avgGDP = Top15[['2006', '2007', '2008', '2009', '2010', '2011', 
                           '2012', '2013', '2014', '2015']].dropna().mean(axis=1)

avgGDP = avgGDP.sort_values(ascending  = False)

country_sel = avgGDP.index[5]

span = Top15.loc[country_sel,:]
span['2015'] - span['2006']

Top15['Energy Supply per Capita'].mean()

Top15['% Renewable'].idxmax(), Top15['% Renewable'].max()

Top15['self_citation_ratio'] = Top15['Self-citations']/Top15['Citations']
Top15['self_citation_ratio'].idxmax(), Top15['self_citation_ratio'].max()

Top15['population_estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
est_pop = Top15['population_estimate'].sort_values(ascending = False)
populous_country = est_pop.index[2]

Top15['citable_docs_per_capita'] = Top15['Citable documents']/Top15['population_estimate']
Top15['citable_docs_per_capita'].corr(Top15['Energy Supply per Capita'])

med = Top15['% Renewable'].median()
Top15['Highrenew'] = Top15['% Renewable'].apply(lambda x: 0 if x < med else 1) 
Highrenew = Top15['Highrenew'].sort_values(ascending = True)


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}


df = pd.DataFrame.from_dict(ContinentDict, orient='index')
df.columns = ['Continent']
new = pd.merge(df, Top15, how='outer', left_index=True, right_index=True)
continent_table = new.groupby('Continent')['population_estimate'].agg({'Size':np.count_nonzero,'Sum':np.sum,'Mean':np.mean,'Std':np.std})

bins = pd.cut(new['% Renewable'],5)

est_pop = est_pop.map('{:,.2f}'.format)