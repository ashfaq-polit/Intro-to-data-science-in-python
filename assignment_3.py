# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:29:44 2020

@author: mahme026
"""

import pandas as pd
import numpy as np

#Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.
#Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
#['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
#Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

#Rename the following list of countries (for use in later questions):
#"Republic of Korea": "South Korea",
#"United States of America": "United States",
#"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
#"China, Hong Kong Special Administrative Region": "Hong Kong"

#There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,e.g.
#'Bolivia (Plurinational State of)' should be 'Bolivia',
#'Switzerland17' should be 'Switzerland'.

#Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.
#Make sure to skip the header, and rename the following list of countries:
#"Korea, Rep.": "South Korea", 
#"Iran, Islamic Rep.": "Iran",
#"Hong Kong SAR, China": "Hong Kong"

#Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.
#Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
#The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
#This function should return a DataFrame with 20 columns and 15 entries.


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

### Question 2 (6.6%)
#The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
#*This function should return a single number.*

entries_lost = merged_file.shape[0] - Top15.shape[0]

#What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
#This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.

avgGDP = Top15[['2006', '2007', '2008', '2009', '2010', '2011', 
                           '2012', '2013', '2014', '2015']].dropna().mean(axis=1)

avgGDP = avgGDP.sort_values(ascending  = False)

#By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
#This function should return a single number.

country_sel = avgGDP.index[5]

span = Top15.loc[country_sel,:]
span['2015'] - span['2006']

#What is the mean Energy Supply per Capita?
#This function should return a single number.

Top15['Energy Supply per Capita'].mean()

#What country has the maximum % Renewable and what is the percentage?
#This function should return a tuple with the name of the country and the percentage.

#Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
#This function should return a tuple with the name of the country and the ratio.

Top15['% Renewable'].idxmax(), Top15['% Renewable'].max()

Top15['self_citation_ratio'] = Top15['Self-citations']/Top15['Citations']
Top15['self_citation_ratio'].idxmax(), Top15['self_citation_ratio'].max()

#Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
#This function should return a single string value.

Top15['population_estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
est_pop = Top15['population_estimate'].sort_values(ascending = False)
populous_country = est_pop.index[2]

#Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
#This function should return a single number.

Top15['citable_docs_per_capita'] = Top15['Citable documents']/Top15['population_estimate']
Top15['citable_docs_per_capita'].corr(Top15['Energy Supply per Capita'])

#Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
#This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.

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

#Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
#This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.

bins = pd.cut(new['% Renewable'],5)

#Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
#e.g. 317615384.61538464 -> 317,615,384.61538464
#This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.

est_pop = est_pop.map('{:,.2f}'.format)
