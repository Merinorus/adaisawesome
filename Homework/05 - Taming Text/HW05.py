
# coding: utf-8

# # 05 - Taming Text

# In[1]:

from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.sentiment import *
import pandas as pd
import numpy as np
import nltk
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
get_ipython().magic('matplotlib inline')


# In[2]:

# import data
directory = 'hillary-clinton-emails/'
aliases = pd.read_csv(directory+'aliases.csv')
email_receivers = pd.read_csv(directory+'EmailReceivers.csv')
emails = pd.read_csv(directory+'Emails.csv')
persons = pd.read_csv(directory+'Persons.csv')


# ### Comparison between extracted body text and raw text

# In[3]:

i = 2
print(emails['ExtractedBodyText'][i], '\n\n END OF BODY TEXT \n\n', emails['RawText'][i])


# By reading a few emails we can see that the extracted body text is just the text that the email sender wrote (as stated on Kaggle) while the raw text gathers the previous emails forwarded or the whole discussion. Note that the extracted body text can sometimes contain NaNs. By including repeated messages in the raw text, you induce bias in the distribution of the words, thus we kept only the body text

# ## 1. Worldclouds

# In[4]:

# raw corpus
text_corpus = emails.ExtractedBodyText.dropna().values
raw_text = ' '.join(text_corpus)

# generate wordcloud
wordcloud = WordCloud().generate(raw_text)
plt.figure(figsize=(15,10))
plt.imshow(wordcloud)
plt.axis('off');


# In[8]:

def preprocess(text, stemmer):
    print('Length of raw text: ', len(raw_text))
    
    # tokenization (need to install models/punk from nltk.download())
    tokens = nltk.word_tokenize(raw_text, language='english')
    print('Number of tokens extracted: ', len(tokens))
    
    # stopwords removal (need to install stopwords corpus in corpora/stopwords)
    # cach stopwords to improve performance (70x speedup)
    cached_stopwords = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in cached_stopwords]
    print('Number of tokens after stopword removal: ', len(filtered_tokens))
    
    # stemming
    if stemmer == 'snowball':
        stemmer = nltk.SnowballStemmer('english')
    elif stemmer == 'porter':
        stemmer = nltk.PorterStemmer('english')
    else: 
        print('choose appropriate stemmer')
    stemmed_filtered_tokens = [stemmer.stem(t) for t in filtered_tokens]
    
    # dump array in text file
    output = ' '.join(stemmed_filtered_tokens)
    with open("preprocessed_text.txt", "w") as text_file:
        text_file.write(output)
        
preprocess(raw_text, 'snowball')


# In[9]:

preprocessed_text = open('preprocessed_text.txt').read()
wordcloud2 = WordCloud().generate(preprocessed_text)
plt.figure(figsize=(15,10))
plt.imshow(wordcloud2)
plt.axis('off');


# ## Comparison between the word clouds
# 
# Looking at the wordcloud generated after having preprocessed the data, it seems that stemming hurt the "performance" of the wordcloud, indeed a number of words have been incorrectly stemmed e.g. department has been reduced to depart, secretary to secretary, message to messag and so on.

# ## 2. Sentiment analysis
# from [this link](https://www.kaggle.com/ampaho/d/kaggle/hillary-clinton-emails/foreign-policy-map-through-hrc-s-emails/code),we added the following words to be removed from the emails:
# * add "RE" because the iso3 code for Reunion islands.. but it appears a lot in emails to indicate the RE(sponses) to previous emails.
# * FM
# * TV is ISO2 code for Tuvalu but also refers to Television
# * AL is a given name and also ISO2 for Albania
# * BEN is a given name and also ISO3 for Benin
# * LA is Los angeles and iso 2 for Lao
# * AQ is abbreviation of "As Quoted" and iso 2 for Antarctica
# 
# After a few runs, we looked at the (unusual) countries extracted. For example the country Saint Pierre and Miquelon is mentionned 631 times, not bad for such a small country. We noticed that an important number of emails have words capitalized and are misinterpreted as ISO2/ISO3 codes for countries. To cope with this we added the following stop words:
# * AND is ISO3 for Andorra
# * AM is ISO2 for Armenia
# * AT is ISO2 for Austria
# * IN is ISO2 for India
# * NO is ISO2 for Norway
# * PM is iSO2 for Saint Pierre and Miquelon
# * TO is ISO2 for Tonga
# * BY is ISO2 for Belarus
# * IE is ISO2 for Ireland (id est)
# * IT is ISO2 for Italy
# * MS is ISO2 for Montserrat

# In[11]:

def find_countries(tokens):
    # find countries in a list of token
    countries = []
    for token in tokens:
        try:
            # search for any alpha_2 country name e.g. US, CH
            country = pycountry.countries.get(alpha_2=token)
            countries.append(country.name)            
        except KeyError:
            try:
                # search for any alpha_3 country name e.g. USA, CHE
                country = pycountry.countries.get(alpha_3=token)
                countries.append(country.name)
            except KeyError:
                try:
                    # search for a country by its name, title() upper cases every first letter but lower cases
                    # the other, hence it is handled last, but it deals with country written in lower case
                    country = pycountry.countries.get(name=token.title())
                    countries.append(country.name)
                except KeyError: pass
    return list(set(countries))


# In[23]:

def foreign_policy(emails, sentiment_analyzer):
    start_time = time.time()
    words_to_be_removed = ["RE", "FM", "TV", "LA", "AL", "BEN", "AQ", "AND", "AM", "AT", "IN", "NO", "PM", "TO",
                          "BY", "IE", "IT", "MS"]
    vader_analyzer = SentimentIntensityAnalyzer()
    foreign_policy = {}
    cached_stopwords = set(stopwords.words('english'))
    cached_stopwords.update(words_to_be_removed)
    i=0

    for email in emails: # TODO: regex instead of tokens lookup parce que ca prend trop de teeeeemps
        #print('{:d} / {:d} emails processed'.format(i, len(emails)))
        tokens = nltk.word_tokenize(email, language='english')
        tokens = [word for word in tokens if word not in cached_stopwords]
        # country lookup in tokens
        countries = find_countries(tokens)
        i +=1
        if not countries: continue
        
        if sentiment_analyzer =='vader':
            sentiment = vader_analyzer.polarity_scores(email)
            score = sentiment['compound']
        #elif sentiment_analyzer ==''
              
        for country in countries:
            if not country in foreign_policy.keys():
                foreign_policy.update({country: [score, 1]})
            else:
                foreign_policy[country][0] += score
                foreign_policy[country][1] += 1
    for country, value in foreign_policy.items():
        foreign_policy.update({country: [(value[0]/value[1]), value[1]]})
    print("--- %d seconds elapsed ---" % (time.time() - start_time))
    return foreign_policy


# In[40]:

result = foreign_policy(text_corpus, sentiment_analyzer='vader')


# In[42]:

result


# In[54]:

pycountry.countries.get(name='Honduras')


# In[80]:

def create_palette(sentiments):
    color_palette = []
    minimum = np.min(sentiments)
    maximum = np.max(sentiments)
    for sentiment in sentiments:
        rescaled = (sentiment-minimum) / (maximum - minimum)
        g = rescaled
        r = 1 - g
        color_palette.append((r,g,0))
    return color_palette


# ### Plotting the foreign policy

# In[87]:

df = pd.DataFrame.from_dict(result, orient='index')
df.reset_index(inplace=True)
df.columns =['Country', 'Sentiment', 'Count']
df = df[df['Count'] > 15]
df = df.sort_values('Sentiment', ascending=False)
gradient = create_palette(df['Sentiment'].values)
plt.figure(figsize=(15,7))
plot = sns.barplot(x='Country', y='Count', data=df, orient='vertical', palette=gradient)
plt.xticks(rotation=45);
plt.ylabel('Sentiment towards country');


# In[45]:

pycountry.countries.get(name='Palau')


# In[26]:

test_sentence = "and here I am AM TO speaking of France"
test_sentence = "This is a typical sentence, with don't. Punkts, something e.g. words US, U.S.A"
cached_stopwords = set(stopwords.words('english'))
words_to_be_removed = ["RE", "FM", "TV", "LA", "AL", "BEN", "AQ", "AND", "AM", "AT"]
cached_stopwords.update(words_to_be_removed)
tokens = nltk.word_tokenize(test_sentence)
#tokens = [word for word in tokens if word not in cached_stopwords]
countries = find_countries(tokens)
print(tokens)


# In[ ]:

test_sentence = 'This is a very pleasant day.'
#test_sentence = 'this is a completely neutral sentence'
polarity = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
vader_analyzer = SentimentIntensityAnalyzer()
tokens = nltk.word_tokenize(test_sentence)
#tokens.remove('is')
result = ' '.join(tokens)
sentiment = vader_analyzer.polarity_scores(result)
#mean = -sentiment['neg'] + sentiment['pos']
#print(sentiment, mean)
np.max(sentiment.values())


# In[ ]:

test_set = ['nice nice good USA US switzerland', 'bad good bad bad bad libya', 'Switzerland good nice nice']
words_to_be_removed = ["RE", "FM", "TV", "LA", "AL", "BEN", "AQ"]
vader_analyzer = SentimentIntensityAnalyzer()
country_counts = {}
country_sentiments = {}
foreign_policy = {}
for email in test_set:
    tokens = nltk.word_tokenize(email, language='english')
    tokens = [word for word in tokens if word not in words_to_be_removed]
    clean_email = ' '.join(tokens)
    sentiment = vader_analyzer.polarity_scores(clean_email)
    score = sentiment['compound']
    # country lookup in raw text 
    countries = find_countries(tokens)
    for country in countries:
        if not country in foreign_policy.keys():
            foreign_policy.update({country: [score, 1]})
        else:
            foreign_policy[country][0] += score
            foreign_policy[country][1] += 1

for country, value in foreign_policy.items():
    foreign_policy.update({country: [(value[0]/value[1]), value[1]]})

