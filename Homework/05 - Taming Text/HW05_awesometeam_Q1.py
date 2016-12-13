
# coding: utf-8

# # Assignment

# 1. Generate a word cloud based on the raw corpus -- I recommend you to use the [Python word_cloud library](https://github.com/amueller/word_cloud).
# With the help of `nltk` (already available in your Anaconda environment), implement a standard text pre-processing pipeline (e.g., tokenization, stopword removal, stemming, etc.) and generate a new word cloud. Discuss briefly the pros and cons (if any) of the two word clouds you generated.

# ## Part 1

# Generate a word cloud based on the raw corpus

# In[47]:

import pandas as pd
import numpy as np
from wordcloud import WordCloud
from IPython.display import Image, display
data = pd.read_csv('hillary-clinton-emails/emails.csv')
data.ix[:,:8].head()


# In[48]:

data.ix[:,8:].head()


# ### Trial 1) - Rawy Extracted Subject and ExtractedBodyText 

# Let's only keep the text which is relevant for the raw body corpus, which is: ExtractedSubject and ExtractedBodyText, which encompass most of what the message should be about.

# In[49]:

data_cut = data[['ExtractedSubject','ExtractedBodyText']].copy()
data_cut


# In[50]:

data_csv = data_cut.to_csv()


# In[51]:

# Credit to - https://github.com/amueller/word_cloud/blob/master/examples/simple.py

# Make the wordcloud
wordcloud = WordCloud().generate(data_csv)
image = wordcloud.to_image()
display(Image('image_raw.png'))
#image.show()


# From here, it's clear that words such as Re, Fw, pm (i.e. referring to time), which are not related to the content of the text itself but rather deal with email processing, are disproportiate in the full picture and should be taken out.

# ## Part 2

# a) implement a standard text pre-processing pipeline (e.g., tokenization, stopword removal, stemming, etc.)

# In[52]:

import re
import nltk


# ## a) Tokenization

# The pirpose of tokenization is to chop up long strings into individual words or symbols. This allows for further processing of the words.

# In[67]:

from nltk import word_tokenize
data_clean = data_cut.replace(np.nan,' ', regex=True)


# In[55]:

data_clean['tokenized_subj'] = data_clean.apply(lambda row: nltk.word_tokenize(row['ExtractedSubject']), axis=1)
data_clean['tokenized_sents'] = data_clean.apply(lambda row: nltk.word_tokenize(row['ExtractedBodyText']), axis=1)
data_clean


# You can now see that the sentences / subject lines are broken up into words (or symbols) within a list, which we can now use to check for stopworkds.

# ## b) Removing Stopwords 

# Let's see what are the stopwords that are in the nltk database that we can remove. 

# In[56]:

from nltk.corpus import stopwords # Import the stop word list
stop = stopwords.words('english')
print(stopwords.words("english") )


# As a reference to check whether the stopwords have been removed is line 15, where there is "your".

# In[57]:

# Remove stop words from "words"
data_clean2 = data_clean
data_clean2['tokenized_subj'] = data_clean2['tokenized_subj'].apply(lambda x: [item for item in x if item not in stop])
data_clean2['tokenized_sents'] = data_clean2['tokenized_sents'].apply(lambda x: [item for item in x if item not in stop])
data_clean2


# You can see that the stopword in line 15 is now gone, so we are set!

# ### c) stemming

# We need to change the words into more standard forms to reduce the inflectual forms.

# In[66]:

data_clean3 = data_clean2
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


# In[65]:

for w in data_clean3[["tokenized_subj"]]:
    stemmer.stem(w)
    
for w in data_clean3[["tokenized_sents"]]:
    stemmer.stem(w)

data_clean3


# ### d) generate a new word cloud

# In[14]:

type (data_csv_new)


# In[13]:

wordcloud = WordCloud().generate(data_csv_new)
image = wordcloud.to_data_csv_newimage()
#display(Image('image_raw.png'))
image.show()


# In[ ]:




# ## Discussion 

# 
