
# coding: utf-8

# Question 2) Find all the mentions of world countries in the whole corpus, 
# using the pycountry utility (HINT: remember that there will be different surface forms 
# for the same country in the text, e.g., Switzerland, switzerland, CH, etc.) 
# Perform sentiment analysis on every email message using the demo methods 
# in the nltk.sentiment.util module. Aggregate the polarity information of all 
# the emails by country, and plot a histogram (ordered and colored by polarity level) 
# that summarizes the perception of the different countries. Repeat the aggregation and plotting steps using different demo methods from the sentiment analysis module.
# Can you find substantial differences?

# In[51]:

import pandas as pd
import pycountry
from nltk.sentiment import *
import numpy as np
import matplotlib.pyplot as plt
import codecs
import math
import re
import string



# Pre Process the Data, Dropping Irrelevant Columns

# In[204]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[205]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)
emails.head()


# In[206]:

emails_cut = emails[['ExtractedBodyText']].copy()
emails_cut.head()


# In[207]:

emails_cut = emails_cut.dropna()
emails_cut.head()


# Now we must tokenize the data...

# In[208]:

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
tokenizer = RegexpTokenizer(r'\w+')


# In[209]:

emails_tokenized = emails_cut.copy()
for index, row in emails_tokenized.iterrows():
    row['ExtractedBodyText'] = tokenizer.tokenize(row['ExtractedBodyText'])
emails_tokenized.columns = ['TokenizedText']
emails_tokenized.reset_index(drop=True, inplace=True)
emails_tokenized.head()


# Figure out what words to remove...

# In[210]:

words_delete = ['IT', 'RE','LA','AND', 'AM', 'AT', 'IN', 'I', 'ME', 'DO', 
                'A', 'AN','BUT', 'IF', 'OR','AS','OF','BY', 'TO', 'UP','ON','ANY', 'NO', 'NOR', 'NOT','SO',
                'S', 'T','DON','D', 'LL', 'M', 'O','VE', 'Y','PM', 'TV','CD','PA','ET', 'BY', 'IE','MS', 'MP', 'CC', 
                'GA','VA', 'BI','CV', 'AL','VAT', 'VA','AI', 'MD', 'SM', 'FM', 'EST', 'BB', 'BRB', 'AQ', 'MA', 'MAR', 'JAM', 'BM', 
                'Lybia', 'LY', 'LBY', 'MC', 'MCO', 'MO', 'MAC', 'NC', 'PG', 'PNG', 'SUR', 'VI', 'lybia', 'ARM'] 
emails_final = emails_tokenized.copy()
emails_final['TokenizedText'] = emails_final['TokenizedText'].apply(lambda x: [item for item in x if item not in words_delete])
emails_final.head()


# Create list of countries

# In[211]:

countries_cited = []
for emails in emails_final['TokenizedText']:
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

# In[212]:

#List with Unique Entries of Countries Cited
final_countries = list(set(countries_cited))
size = len(final_countries)
final_countries


# In[213]:

#Create New DataFrame for the Counts
Country_Sent = pd.DataFrame(index=range(0,size),columns=['Country', 'Count'])
Country_Sent['Country']=final_countries
Country_Sent.head()


# In[214]:

count_list = []
for country in Country_Sent['Country']:
    count = countries_cited.count(country)
    count_list.append(count)
    
Country_Sent['Count']=count_list
Country_Sent.head()



# In[215]:

#Take Out Countries with Less than 20 Citations
Country_Sent= Country_Sent[Country_Sent['Count'] > 14]
Country_Sent = Country_Sent.reset_index(drop=True)
Country_Sent.head()


# In[216]:

#plot to see frequencies
Country_Sent.plot.bar(x='Country', y='Count')
plt.show()

#We have repeatedly plotted this, identifying weird occurances (small countries with high counts), 
#and then elimitating them from the data set and repating the process


# In[217]:

#create a list with all possible names of the countries above
countries_used_name = []
countries_used_alpha_2 =[]
countries_used_alpha_3 =[]

for country in Country_Sent['Country']:
    country_names = pycountry.countries.get(name=country)
    countries_used_name.append(country_names.name)
    countries_used_alpha_2.append(country_names.alpha_2)
    countries_used_alpha_3.append(country_names.alpha_3)

Country_Sent['Alpha_2']=countries_used_alpha_2
Country_Sent['Alpha_3']=countries_used_alpha_3

Country_Sent.head()


# In[218]:

len(Country_Sent)


# Now we check sentiment on emails around these names

# In[170]:

sentiments = []
vader_analyzer = SentimentIntensityAnalyzer()

size = len(Country_Sent['Alpha_2'])
for i in range(1,size):
    country_score =[]
    for email in emails_no_stop['TokenizedText']:
        if Country_Sent['Alpha_2'][i] in email or Country_Sent['Alpha_3'][i] in email or Country_Sent['Country'][i] in email:
            str_email = ' '.join(email)
            sentiment = vader_analyzer.polarity_scores(str_email)
            score = sentiment['compound']
            country_score.append(score)
        else: pass
    if len(country_score)!=0:
        sentiment_score = sum(country_score) / float(len(country_score))
        sentiments.append(sentiment_score)
    else:
        sentiments.append(999)

                   
              
        


# In[220]:

#error in iteration, must drop NZ because it was not taken into account in the sentiments analysis
Country_Sent = Country_Sent.drop(Country_Sent.index[[0]])

len(Country_Sent)


# In[222]:

#add sentiment list to data frame
Country_Sent['Sentiment'] = sentiments
Country_Sent.head()


# In[224]:

#delete any row with sentiment value of 999
Country_Sent = Country_Sent[Country_Sent['Sentiment'] != 999]
Country_Sent.head()


# In[226]:

#reorder dataframe in ascending order of sentiment
Country_Sent.sort_values(['Sentiment'], ascending=True, inplace=True)
Country_Sent.head()


# In[254]:

#reorder index
Country_Sent = Country_Sent.reset_index(drop=True)

Country_Sent.head()


# Now we make a color gradient for the histogram

# In[267]:

#We must normalize the sentiment scores and create a gradient based on that (green, blue & red gradient)
#first we sort the ones that are below zero, than the ones above zero
color_grad = []
size = len(Country_Sent['Sentiment'])

for i in range(0,size):
    if Country_Sent['Sentiment'][i] < 0:
        high = 0
        low = np.min(sentiments)
        rg = high-low
        new_entry = -(low-Country_Sent['Sentiment'][i])/rg
        red = 1 - new_entry
        if new_entry != 0:
            color_grad.append((red,0,new_entry))
        else: 
            color_grad.append((red,0,0))
    else:
        high = np.max(sentiments)
        low = 0
        rg2 = high-low
        new_entry = -(Country_Sent['Sentiment'][i]-low)/rg2
        green = 1 - new_entry
        if new_entry != 0:
            color_grad.append((0,green,new_entry))        
        else: 
            color_grad.append((0,green,0))
        

Country_Sent['color_grad'] = color_grad        
Country_Sent.head()


# In[268]:

#Now we create the bar plot based on this palette
import seaborn as sns

plot = sns.barplot(x='Country', y='Sentiment', data=Country_Sent, orient='vertical', palette=color_grad)
plt.ylabel('Country Sentiment');
plt.show()


# In[252]:

#Now we create a bar plot with an automatic gradient based on sentiment
size = len(Country_Sent['Sentiment'])
plt.figure(figsize=(30,20))
grad = sns.diverging_palette(10, 225, n=32)
plot = sns.barplot(x='Country', y='Sentiment', data=Country_Sent, orient='vertical', palette = grad )
plt.xticks(rotation=60);
plt.ylabel('Country Sentiment');
plt.show()


# In[ ]:



