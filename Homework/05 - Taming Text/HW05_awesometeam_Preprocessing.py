
# coding: utf-8

# Each question is handled in a separate file, but they have some data wrangling in common. This file prepares emails in a way that they can be used for the questions. Thus we don't have to do it in each separate notebook.

# In[1]:

import pandas as pd


# In[2]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[3]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)


# In[4]:

# Senders and receivers names could be renamed correctly with corssing aliases and persons.
# But as we don't need them for the three questions, we won't do it for the moment.


# In[ ]:

# Export the data so it can be used for next questions


# In[ ]:



