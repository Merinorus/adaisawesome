
# coding: utf-8

# Question 2) Find all the mentions of world countries in the whole corpus, 
# using the pycountry utility (HINT: remember that there will be different surface forms 
# for the same country in the text, e.g., Switzerland, switzerland, CH, etc.) 
# Perform sentiment analysis on every email message using the demo methods 
# in the nltk.sentiment.util module. Aggregate the polarity information of all 
# the emails by country, and plot a histogram (ordered and colored by polarity level) 
# that summarizes the perception of the different countries. Repeat the aggregation and plotting steps using different demo methods from the sentiment analysis module.
# Can you find substantial differences?

# In[105]:

import pandas as pd
import pycountry
import nltk
from nltk.sentiment import *
import numpy as np
import matplotlib.pyplot as plt
import codecs
import math
import re
import string
import nltk.data



# In[107]:

nltk.download()


# Pre Process the Data, Dropping Irrelevant Columns

# In[16]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[17]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)
emails.head()


# In[18]:

emails_cut = emails[['ExtractedBodyText']].copy()
emails_cut.head()


# In[19]:

emails_cut = emails_cut.dropna()
emails_cut.head()


# Now we must tokenize the data...

# In[20]:

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
tokenizer = RegexpTokenizer(r'\w+')


# In[21]:

emails_tokenized = emails_cut.copy()
for index, row in emails_tokenized.iterrows():
    row['ExtractedBodyText'] = tokenizer.tokenize(row['ExtractedBodyText'])
emails_tokenized.columns = ['TokenizedText']
emails_tokenized.reset_index(drop=True, inplace=True)
emails_tokenized.head()


# Figure out what words to remove...

# In[81]:

words_delete = ['IT', 'RE','LA','AND', 'AM', 'AT', 'IN', 'I', 'ME', 'DO', 
                'A', 'AN','BUT', 'IF', 'OR','AS','OF','BY', 'TO', 'UP','ON','ANY', 'NO', 'NOR', 'NOT','SO',
                'S', 'T','DON','D', 'LL', 'M', 'O','VE', 'Y','PM', 'TV','CD','PA','ET', 'BY', 'IE','MS', 'MP', 'CC', 
                'GA','VA', 'BI','CV', 'AL','VAT', 'VA','AI', 'MD', 'SM', 'FM', 'EST', 'BB', 'BRB', 'AQ', 'MA', 'MAR', 'JAM', 'BM', 
                'Lybia', 'LY', 'LBY', 'MC', 'MCO', 'MO', 'MAC', 'NC', 'PG', 'PNG', 'SUR', 'VI'] 
# from part one we can see some words (from stopwords) that may end up as country abbreviations 
#as well as analysis of weird data we got down the line
#also weird errors occuring with Lybia, so it was excluded (odd given a lot of the controversy was about Lybia...)

emails_no_stop = emails_tokenized.copy()
emails_no_stop['TokenizedText'] = emails_no_stop['TokenizedText'].apply(lambda x: [item for item in x if item not in words_delete])
emails_no_stop.tail()


# In[82]:

#Make sure to Capitalize all words
for email in emails_no_stop['TokenizedText']:
    for word in email:
        word.title()
        
emails_no_stop['TokenizedText'].head()


# Create list of countries

# In[83]:

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


# Organize List and Count Occurrence of Each Country

# In[84]:

#List with Unique Entries of Countries Cited
final_countries = list(set(countries_cited))
size = len(final_countries)
final_countries


# In[85]:

#Create New DataFrame for the Counts
Country_Sent = pd.DataFrame(index=range(0,size),columns=['Country', 'Count'])
Country_Sent['Country']=final_countries
Country_Sent.head()


# In[86]:

count_list = []
for country in Country_Sent['Country']:
    count = countries_cited.count(country)
    count_list.append(count)
    
Country_Sent['Count']=count_list
Country_Sent.head()



# In[87]:

#Take Out Countries with Less than 20 Citations
Country_Sent= Country_Sent[Country_Sent['Count'] > 14]
Country_Sent.head()


# In[88]:

#plot to see frequencies
Country_Sent.plot.bar(x='Country', y='Count')
plt.show()

#We have repeatedly plotted this, identifying weird occurances (small countries with high counts), 
#and then elimitating them from the data set and repating the process


# In[89]:

#create a list with all possible names of the countries above
countries_used = []
for country in Country_Sent['Country']:
    country_names = pycountry.countries.get(name=country)
    countries_used.append(country_names.name)
    countries_used.append(country_names.alpha_2)
    countries_used.append(country_names.alpha_3)

countries_used


# Now we check sentiment on emails around these names

# In[119]:

sentiments = []
vader_analyzer = SentimentIntensityAnalyzer()

for country in countries_used:
    country_names=[]
    try:
        country_name = pycountry.countries.get(alpha_2=country)
        country_names.append(country_name.alpha_2)    
    except KeyError:
            try:
                country_name = pycountry.countries.get(alpha_3=country)
                country_names.append(country_name.alpha_3)
            except KeyError:
                try:
                    country_name = pycountry.countries.get(name=country)
                    country_names.append(country_name.name)
                except KeyError:
                    country_names.append('NaN')
    country_score =[]
    for name in country_names:
        for email in emails_no_stop['TokenizedText']:
            if name in email:
                sentiment = vader_analyzer.polarity_scores(str_email)
                print(sentiment)
                score = sentiment['compound']
                country_score.append(score)
            else: pass
        if len(country_score) !=0: 
            sentiment_score = sum(country_score) / float(len(country_score))
            sentiments.append(sentiment_score)
        else:
            sentiment_score = 9999
            sentiments.append(sentiment_score)
        
        

            
sentiments
            
              
        


# In[ ]:

text = ['I hate going to th pa]

