
# coding: utf-8

# # Assignment

# 1. Generate a word cloud based on the raw corpus -- I recommend you to use the [Python word_cloud library](https://github.com/amueller/word_cloud).
# With the help of `nltk` (already available in your Anaconda environment), implement a standard text pre-processing pipeline (e.g., tokenization, stopword removal, stemming, etc.) and generate a new word cloud. Discuss briefly the pros and cons (if any) of the two word clouds you generated.

# ## Part 1

# Generate a word cloud based on the raw corpus

# In[285]:

import pandas as pd
import numpy as np
from wordcloud import WordCloud
from IPython.display import Image, display
data = pd.read_csv('hillary-clinton-emails/emails.csv')
data.ix[:,:8].head()


# In[125]:

data.ix[:,8:].head()


# Let's only keep the text which is relevant for the raw body corpus, which is: ExtractedSubject and ExtractedBodyText, which encompass most of what the message should be about.

# In[286]:

data_cut = data[['ExtractedSubject','ExtractedBodyText']].copy()
data_cut


# In[287]:

data_csv = data_cut.to_csv()


# In[167]:

# Credit to - https://github.com/amueller/word_cloud/blob/master/examples/simple.py

# Make the wordcloud
wordcloud = WordCloud().generate(data_csv)
image = wordcloud.to_image()
display(Image('image_raw.png'))
#image.show()


# From here, it's clear that words such as Re, Fw, pm (i.e. referring to time), which are not related to the content of the text itself but rather deal with email processing, are disproportiate in the full picture and should be taken out.

# ## Part 2

# a) implement a standard text pre-processing pipeline (e.g., tokenization, stopword removal, stemming, etc.)

# In[168]:

import re
import nltk


# ## a) Tokenization

# The purpose of tokenization is to chop up long strings into individual words or symbols. This allows for further processing of the words.

# Let's first put all of the values into 1 column called "Text" and get rid of the NaNs. At this point, we do not care to distinguish between the content in the subject and the body.

# In[288]:

for i in data_cut['ExtractedBodyText']:
    data_cut.loc[len(data_cut)] = [i, 'nan']


# In[308]:

data_clean = data_cut.drop('ExtractedBodyText', axis =1)
data_clean.columns = ['Text']
data_clean = data_clean[pd.notnull(data_clean['Text'])]
data_clean


# ### Side-note: Removing capitalization

# Convert all of the strings to lowercase while they are whole, as we'll need it later on.

# In[309]:

for index, row in data_clean.iterrows():
    row['Text'] = row['Text'].lower()
data_clean.head()


# Now let's do some tokenization.

# ### Tokenization

# In[306]:

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')


# In[310]:

data_tokenized = data_clean
for index, row in data_tokenized.iterrows():
    row['Text'] = tokenizer.tokenize(row['Text'])
data_tokenized.columns = ['TokenizedText']
data_tokenized.reset_index(drop=True, inplace=True)
data_tokenized.head()


# You can now see that the sentences / subject lines are broken up into words within a list, which we can now use to check for stopworkds.

# ## b) Removing Stopwords 

# Let's see what are the stopwords that are in the nltk database that we can remove. 

# In[386]:

from nltk.corpus import stopwords # Import the stop word list
stop = stopwords.words('english')


# We will also add "fw", "fwd", "fvv", "re", "pm", and "am" to the stopwords.txt list as they are not helpful and in this context are stopwords.

# In[387]:

print(stopwords.words("english") )


# As a reference to check whether the stopwords have been removed is line 15, where there is "your".

# In[388]:

# Remove stop words from "words"
data_no_stop = data_tokenized
data_no_stop['TokenizedText'] = data_no_stop['TokenizedText'].apply(lambda x: [item for item in x if item not in stop])
data_no_stop


# You can see that the stopword in line 15 is now gone, so we are set!

# ### c) stemming

# We need to change the words into more standard forms to reduce the inflectual forms.

# In[389]:

data_stemming = data_no_stop
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


# In[390]:

for index, row in data_stemming.iterrows():
    for i in row['TokenizedText']:
        i = stemmer.stem(i)

data_stemming


# ### d) generate a new word cloud

# In[393]:

data_csv_new = data_stemming.to_csv()

wordcloud_new = WordCloud().generate(data_csv_new)
image_new = wordcloud_new.to_image()
#display(Image('image_new.png'))
image_new.show()


# ## Discussion 

# 
