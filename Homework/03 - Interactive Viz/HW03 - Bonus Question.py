
# coding: utf-8

# In[53]:

import pandas as pd
import numpy as np
import json
import geopy
import time
import math 
import logging
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


# In[8]:

p3_cantons_data = pd.read_pickle('P3_Cantons.pickle')
p3_cantons_data


# In[9]:

#delete irrelevant columns in the dataset to clean data
p3_cantons_data = p3_cantons_data.drop(['Funding Instrument', 'Canton Longname', 'End Date', 'Start Date', 'Institution', 'University', 'Funding Instrument Hierarchy'], axis=1)
p3_cantons_data


# In[36]:

# define which cantons are german speaking and which are french speaking
# assumption: of the mixed language cantons, only Valais is categorized as French, others are German
german = ['AG','AR','AI', 'ZH', 'BE', 'LU', 'UR', 'SZ', 'OW', 'NW', 'GL', 'ZG', 'FR', 'SO', 'BS', 'SH', 'SG', 'GR', 'TG']
french = ['VD', 'NE', 'GE', 'JU', 'VS']
#delete N/As and Italian Cantons
p3_cantons_data = p3_cantons_data[p3_cantons_data['Canton Shortname'] != 'N/A']
p3_cantons_data = p3_cantons_data[p3_cantons_data['Canton Shortname'] != 'TI']


#add language code for german and french
p3_cantons_data["Language"] = ""
p3_cantons_data['Language'] = ['GE' if x in german else 'FR'for x in p3_cantons_data['Canton Shortname']]



p3_cantons_data      


# In[42]:

#convert values to ints
p3_cantons_data['Approved Amount'] = (p3_cantons_data['Approved Amount']).astype(float)


# In[65]:

#find what distribution of grants looks like
p3_cantons_data['Approved Amount'].hist(bins=100)
pylab.show()


# In[43]:

german_switz = p3_cantons_data[p3_cantons_data['Language']=='GE']
french_switz = p3_cantons_data[p3_cantons_data['Language']=='FR']

ttest_ind(german_switz['Approved Amount'], french_switz['Approved Amount'])


# In[ ]:

# Result: with a p-value of nearly zero, there is a statistically significant difference between 
#how grants are distributed among german and french cantons
#HOWEVER, a t test is not an ideal way to test this because some basic assumptions of the distributions are not met
#such as a normal distribution

