
# coding: utf-8

# ## Assignment:

# Using the models.ldamodel module from the gensim library, run topic modeling over the corpus. Explore different numbers of topics (varying from 5 to 50), and settle for the parameter which returns topics that you consider to be meaningful at first sight.

# ### Finding a compromise

# The goal is to do topic modeling over all the mails. In other words, we have to find recurrent topic or themes that may appear in the conversations.
# They are several way to analyse the mails content, starting by these two "naive" ways:
# - put all the extrated mails in only one document
# - put each extracted mail in a separate document
# 
# But both of these ways have major drawbacks:
# - doing topic modelling on a single document would show the most frequent words, so the result should be the same as if we wanted to make a word cloud
# - a lot of mail are very small, a few words sometimes, so doing topic analysis here would not be extremely meaningful

# So we have to find a compromise: make multiple documents, each of them long enough to be analysed.
# One of the best options would be create the entire conversations with the mail history, so we can extract main topic from each conversation. While it makes sense, it's actually pretty time-consuming to obtain the conversations.

# What we will do here is simply put each mail in a separate document, excluding mails that are too small to be analysed.

# ### Extracting keywords

# In[204]:

import pandas as pd
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re # regular expressions
import matplotlib.pyplot as plt
import numpy as np


# In[205]:

# We reuse data from question 1 that already did a lot of cleaning operations !
emails_cleaned = pd.read_pickle("ilovepickefiles_stemming.pickle")


# In[206]:

emails_cleaned.head()


# During the topic modeling, we still see some words that don't really fit in any topic (eg: would) so we remove some of them intentionally.

# In[207]:

ignore_list = ['00', '10', '15', '30', 'also', 'would']


# In[208]:

#for mail in emails_cleaned.TokenizedText


# We put all the mails in a text table in order to prepare the corpus to be analysed. We exclude mails that are too small.

# In[209]:

min_mail_size = [2, 3, 4, 5, 6, 10, 15, 20, 50];
print("Total number of mail: " + str(emails_cleaned.size))
for i in min_mail_size:
    text = []
    for mail in emails_cleaned.TokenizedText:
        if (len(mail) >= i):
            text.append(mail)
    ratio = len(text) / emails_cleaned.size * 100
    print("Mails with at least " + str(i) + " tokens represent " + str(ratio).zfill(4) + " % of the total.")


# We choose keep mails with at least 5 tokens: we can have sentences that might make sense, while keeping 40 % of the mails. This is about 5000 mails, so we should be able to extract some topics from them.

# In[210]:

MIN_MAIL_SIZE = 5


# In[211]:

text = []
for mail in emails_cleaned.TokenizedText:
    # Take only mails that are long enough
    if (len(mail) >= MIN_MAIL_SIZE):
        # Remove unwanted words
        mail_filtered = mail
        for word in mail_filtered:
            if word in ignore_list:
                mail_filtered.remove(word)
        text.append(mail_filtered)
ratio = len(text) / emails_cleaned.size * 100


# Now, we convert all the mails' words in numbers, each number corresponding to a word. In other words, we convert our table of mail in a corpus, so we will be able to do topic modeling on it.

# In[212]:

text_dictionary = corpora.Dictionary(text)
corpus = [text_dictionary.doc2bow(t) for t in text] 


# Now, time to do the modeling. We will play with the topic number in order to have a consistent result.
# Let's try with different numbers. First 5, then 10, 25 and finally 50 topics:

# In[213]:

def show_topics(lda_model):
    for i in range(lda_model.num_topics):
        topic_words = [word for word, _ in lda_model.show_topic(i, topn = 15)]
        print('Topic ' + str(i+1) + ': ', end = ' ')
        for word in topic_words:
            print(word, end = ' ')
        print("")


# In[214]:

lda_model = models.LdaMulticore(corpus, id2word = text_dictionary, num_topics = 5)
show_topics(lda_model)


# In[215]:

lda_model = models.LdaMulticore(corpus, id2word = text_dictionary, num_topics = 10)
show_topics(lda_model)


# In[216]:

lda_model = models.LdaMulticore(corpus, id2word = text_dictionary, num_topics = 25)
show_topics(lda_model)


# In[217]:

lda_model = models.LdaMulticore(corpus, id2word = text_dictionary, num_topics = 50)
show_topics(lda_model)


# ### Observations

# First to note, there is some unwanted word cropping ("secretariat" becomes "secretari"), but it is still readable and shouldn't give totally different results.

# The goal was to group words such as they relate to the same topic. The results are not concluding: regardless of the number of topic, the same words always reappear: "obama", "state", "secretariat", "call"... It's difficult to put a different name on a lot of topic, because they all look alike a lot.
# For sure, we can tell an "administrative" topic is recurrent: state, secretariat, call, obama, office... The result isn't so exciting !
