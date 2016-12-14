
# coding: utf-8

# Question 2) Find all the mentions of world countries in the whole corpus, 
# using the pycountry utility (HINT: remember that there will be different surface forms 
# for the same country in the text, e.g., Switzerland, switzerland, CH, etc.) 
# Perform sentiment analysis on every email message using the demo methods 
# in the nltk.sentiment.util module. Aggregate the polarity information of all 
# the emails by country, and plot a histogram (ordered and colored by polarity level) 
# that summarizes the perception of the different countries. Repeat the aggregation and plotting steps using different demo methods from the sentiment analysis module.
# Can you find substantial differences?

# In[73]:

import pandas as pd
import pycountry
from nltk.sentiment import *
import numpy as np
import matplotlib.pyplot as plt




# Pre Process the Data, Dropping Irrelevant Columns

# In[74]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[75]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)
emails.head()


# In[76]:

emails_cut = emails[['ExtractedBodyText']].copy()
emails_cut.head()


# In[77]:

emails_cut = emails_cut.dropna()
emails_cut.head()


# Now we must tokenize the data...

# In[79]:

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
tokenizer = RegexpTokenizer(r'\w+')


# In[80]:

emails_tokenized = emails_cut.copy()
for index, row in emails_tokenized.iterrows():
    row['ExtractedBodyText'] = tokenizer.tokenize(row['ExtractedBodyText'])
emails_tokenized.columns = ['TokenizedText']
emails_tokenized.reset_index(drop=True, inplace=True)
emails_tokenized.head()


# Figure out what words to remove...

# In[146]:

words_delete = ['IT', 'RE','LA','AND', 'AM', 'AT', 'IN', 'I', 'ME', 'DO', 
                'A', 'AN','BUT', 'IF', 'OR','AS','OF','BY', 'TO', 'UP','ON','ANY', 'NO', 'NOR', 'NOT','SO',
                'S', 'T','DON','D', 'LL', 'M', 'O','VE', 'Y','PM', 'TV','CD','PA','ET', 'BY', 'IE','MS', 'MP', 'CC', 
                'GA','VA', 'BI','CV', 'AL','VAT', 'VA','AI', 'MD', 'SM', 'FM', 'EST', 'BB', 'BRB', 'AQ', 'MA', 'MAR', 'JAM', 'BM'] 
# from part one we can see some words (from stopwords) that may end up as country abbreviations 
#as well as analysis of weird data we got down the line

emails_no_stop = emails_tokenized.copy()
emails_no_stop['TokenizedText'] = emails_no_stop['TokenizedText'].apply(lambda x: [item for item in x if item not in words_delete])
emails_no_stop.tail()


# Create list of countries

# In[147]:

countries_cited = []
for emails in emails_no_stop['TokenizedText']:
    for word in emails:
        try:
            country_name = pycountry.countries.get(alpha_2=word)
            countries_cited.append(country_name.name)
        except KeyError:
            try:
                country_name = pycountry.countries.get(alpha_3=word)
                countries_cited.append(country_name.name)
            except KeyError:
                try:
                    country = pycountry.countries.get(name=word)
                    countries_cited.append(country_name.name)
                except KeyError: pass
countries_cited           


# Organize List and Count Occurrence of Each Country

# In[148]:

#List with Unique Entries of Countries Cited
final_countries = list(set(countries_cited))
size = len(final_countries)
final_countries


# In[149]:

#Create New DataFrame for the Counts
Country_Sent = pd.DataFrame(index=range(0,size),columns=['Country', 'Count'])
Country_Sent['Country']=final_countries
Country_Sent.head()


# In[150]:

count_list = []
for country in Country_Sent['Country']:
    count = countries_cited.count(country)
    count_list.append(count)
    
Country_Sent['Count']=count_list
Country_Sent.head()



# In[151]:

#Take Out Countries with Less than 20 Citations
Country_Sent= Country_Sent[Country_Sent['Count'] > 14]
Country_Sent.head()


# In[152]:

#plot to see frequencies
Country_Sent.plot.bar(x='Country', y='Count')
plt.show()

#We have repeatedly plotted this, identifying weird occurances (small countries with high counts), 
#and then elimitating them from the data set and repating the process


# In[158]:

#create a list with all possible names of the countries above
countries_used = []
for country in Country_Sent['Country']:
    country_names = pycountry.countries.get(name=country)
    countries_used.append(country_names.name)
    countries_used.append(country_names.alpha_2)
    countries_used.append(country_names.alpha_3)

countries_used


# Now we check sentiment on emails around these names

# In[159]:

for emails in emails_no_stop['TokenizedText']:
    for word in emails:
        test = countries_used.isin(word)
        if test is False: continue
        else:
            country = pycountry.countries.get(word)
            country_name = (country.name)
            if sentiment_analyzer =='vader':
                sentiment = vader_analyzer.polarity_scores(word)
                score = Country_Sent['Sentiment']
              
        


# In[ ]:



