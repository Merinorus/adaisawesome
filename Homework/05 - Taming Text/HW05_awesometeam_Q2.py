
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

# In[118]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[119]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)
emails.head()


# In[120]:

emails_cut = emails[['ExtractedBodyText']].copy()
emails_cut.head()


# In[121]:

emails_cut = emails_cut.dropna()
emails_cut.head()


# Now we must tokenize the data...

# In[122]:

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
tokenizer = RegexpTokenizer(r'\w+')


# In[123]:

emails_tokenized = emails_cut.copy()
for index, row in emails_tokenized.iterrows():
    row['ExtractedBodyText'] = tokenizer.tokenize(row['ExtractedBodyText'])
emails_tokenized.columns = ['TokenizedText']
emails_tokenized.reset_index(drop=True, inplace=True)
emails_tokenized.head()


# Figure out what words to remove...

# In[124]:

#Make sure to Capitalize all words
#for email in emails_no_stop['TokenizedText']:
 #   size = len(email)
#  for i in range (0,size):
   #     wn = email[i].title()
    #    email[i] = wn
    

#emails_no_stop.head()



# In[128]:

words_delete = ['IT', 'RE','LA','AND', 'AM', 'AT', 'IN', 'I', 'ME', 'DO', 
                'A', 'AN','BUT', 'IF', 'OR','AS','OF','BY', 'TO', 'UP','ON','ANY', 'NO', 'NOR', 'NOT','SO',
                'S', 'T','DON','D', 'LL', 'M', 'O','VE', 'Y','PM', 'TV','CD','PA','ET', 'BY', 'IE','MS', 'MP', 'CC', 
                'GA','VA', 'BI','CV', 'AL','VAT', 'VA','AI', 'MD', 'SM', 'FM', 'EST', 'BB', 'BRB', 'AQ', 'MA', 'MAR', 'JAM', 'BM', 
                'Lybia', 'LY', 'LBY', 'MC', 'MCO', 'MO', 'MAC', 'NC', 'PG', 'PNG', 'SUR', 'VI', 'lybia', 'ARM'] 
emails_final = emails_tokenized.copy()
emails_final['TokenizedText'] = emails_final['TokenizedText'].apply(lambda x: [item for item in x if item not in words_delete])
emails_final.head()


# Create list of countries

# In[129]:

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

# In[130]:

#List with Unique Entries of Countries Cited
final_countries = list(set(countries_cited))
size = len(final_countries)
final_countries


# In[131]:

#Create New DataFrame for the Counts
Country_Sent = pd.DataFrame(index=range(0,size),columns=['Country', 'Count'])
Country_Sent['Country']=final_countries
Country_Sent.head()


# In[132]:

count_list = []
for country in Country_Sent['Country']:
    count = countries_cited.count(country)
    count_list.append(count)
    
Country_Sent['Count']=count_list
Country_Sent.head()



# In[163]:

#Take Out Countries with Less than 20 Citations
Country_Sent= Country_Sent[Country_Sent['Count'] > 14]
Country_Sent = Country_Sent.reset_index(drop=True)
Country_Sent.head()


# In[164]:

#plot to see frequencies
Country_Sent.plot.bar(x='Country', y='Count')
plt.show()

#We have repeatedly plotted this, identifying weird occurances (small countries with high counts), 
#and then elimitating them from the data set and repating the process


# In[165]:

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


# Now we check sentiment on emails around these names

# In[ ]:

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


# In[ ]:

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

                   
              
        


# In[ ]:

#add sentiment list to data frame
Country_Sent['Sentiment'] = sentiments
#delete any row with sentiment value of 999
Country_Sent = Country_Sent[Country_Sent['Sentiment'] != 999]
#reorder dataframe in ascending order of sentiment
df.sort_values(['Sentiment'], ascending=True, inplace=True)
#reorder index
Country_Sent = Country_Sent.reset_index(drop=True)


# Now we make a color gradient for the histogram

# In[ ]:

#We must normalize the sentiment scores and create a gradient based on that (green, blue & red gradient)
#first we sort the ones that are below zero, than the ones above zero
Country_Sent['color_grad'] =[]
size = len(Country_Sent['Sentiment'])

for i in range(1,size):
    if Country_Sent['Sentiment'][i] < 0:
        high = 0
        low = np.min(sentiments)
        rg = high-low
        new_entry = (low-entry)/rg
        red = 1 - new_entry
        Country_Sent['color_grad'][i]=(red,0,new_entry)
    else:
        high = np.max(sentiments)
        low = 0
        rg = high-low
        new_entry = (entry-low)/rg
        green = 1 - new_entry
        Country_Sent['color_grad'][i]= (0,green,new_entry)

Country_Sent.head()


# In[ ]:

#Now we create the bar plot based on this palette
import seaborn as sns
plot = sns.barplot(x='Country', y='Sentiment', data=Country_Sent, orient='vertical', palette=Country_Sent['color_grad'])
plt.ylabel('Country Sentiment');
plt.show()


# In[ ]:

#Now we create a bar plot with an automatic gradient based on sentiment
size = len(Country_Sent['Sentiment'])
grad = sns.palplot(sns.diverging_palette(10, 145, n=size))plot = sns.barplot(x='Country', y='Sentiment', data=Country_Sent, orient='vertical', palette=grad)
plt.ylabel('Country Sentiment');
plt.show()

