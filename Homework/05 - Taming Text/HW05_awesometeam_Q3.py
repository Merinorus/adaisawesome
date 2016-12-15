
# coding: utf-8

# The goal is to do topic modeling over all the mails. In other words, we have to find recurrent topic or themes that may appear in the conversations.
# They are several way to analyse the mails content, starting by these two "naive" ways:
# - put all the extrated mails in only one document
# - put each extracted mail in a separate document
# 
# But both of these ways have major drawbacks:
# - doing topic modelling on a single document would show the most frequent words, so the result should be the same as if we wanted to make a word cloud
# - a lot of mail are very small, a few words sometimes, so doing topic analysis here would be meaningless

# So we have to find a compromise: make multiple documents, each of them long enough to be analysed.
# One option would be create the entire conversations with the mail history, so we can extract main topic from each conversation. While it makes sense, it's actually pretty time-consuming to obtain the conversations.

# What we will do is to create a document that contains the "sent mails box" for each person. It doesn't follow a conversation, so our results won't be the most coherent we could get. But the purpose here is to show the basics of topic modelling.

# In[88]:

import pandas as pd
import gensim
import ntlk


# In[9]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[10]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)


# In[81]:

sampleEmail = emails.loc[1].ExtractedBodyText


# In[87]:

# Testing the cleaning function
cleanedSample = clean_text(sampleEmail)
cleanedSample


# In[72]:

emailsBySend = emails.groupby(['SenderPersonId'])['ExtractedBodyText']
df = list(emailsBySend)
df = pd.DataFrame(df)


# In[50]:

senderIDs = []
for senderID in emails['SenderPersonId']:
    print(senderID)


# In[32]:

emailsBySend


# In[20]:

bodyContent = pd.DataFrame(emails.ExtractedBodyText.dropna())


# In[21]:

bodyContent


# In[86]:

def clean_text(text):
    cleanedText = text.replace('\n', ' ')
    cleanedText = cleanedText.replace('\r', '')
    return cleanedText

