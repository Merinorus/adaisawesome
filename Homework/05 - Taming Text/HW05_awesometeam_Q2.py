
# coding: utf-8

# Question 2) Find all the mentions of world countries in the whole corpus, 
# using the pycountry utility (HINT: remember that there will be different surface forms 
# for the same country in the text, e.g., Switzerland, switzerland, CH, etc.) 
# Perform sentiment analysis on every email message using the demo methods 
# in the nltk.sentiment.util module. Aggregate the polarity information of all 
# the emails by country, and plot a histogram (ordered and colored by polarity level) 
# that summarizes the perception of the different countries. Repeat the aggregation and plotting steps using different demo methods from the sentiment analysis module.
# Can you find substantial differences?

# In[1]:

import pandas as pd
import pycountry
from nltk.sentiment import *
import numpy as np



# Pre Process the Data, Dropping Irrelevant Columns

# In[ ]:

emails = pd.read_csv("hillary-clinton-emails/Emails.csv")


# In[ ]:

# Drop columns that won't be used
emails = emails.drop(['DocNumber', 'MetadataPdfLink','DocNumber', 'ExtractedDocNumber', 'MetadataCaseNumber'], axis=1)


# In[ ]:



