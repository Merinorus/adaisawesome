
# coding: utf-8

# In[21]:

import pandas as pd
import numpy as np
import json
import geopy
import time
import math 
import logging


# In[22]:

p3_cantons_data = pd.read_pickle('P3_Cantons.pickle')
p3_cantons_data


# In[23]:

#find all possible short names
cantons = p3_cantons_data['Canton Shortname'].unique()
#create new dataframe with canton indexes
final_df= pd.Series(0, index=cantons)
final_df = final_df.to_frame(name='Total Sum')
final_df['Canton Name'] = final_df.index
final_df = final_df.reset_index(drop=True)
final_df


# In[24]:

#delete irrelevant columns in the dataset to clean data
p3_cantons_data = p3_cantons_data.drop(['Funding Instrument', 'Canton Longname', 'End Date', 'Start Date', 'Institution', 'University', 'Funding Instrument Hierarchy'], axis=1)
# Drop all grants that are not associated with a canton
p3_cantons_data = p3_cantons_data[p3_cantons_data['Canton Shortname'] != 'N/A']
p3_cantons_data


# In[25]:

type(p3_cantons_data['Approved Amount'][1])


# In[26]:

p3_cantons_data['Approved Amount'] = (p3_cantons_data['Approved Amount']).astype(float)
type(p3_cantons_data['Approved Amount'][1])


# In[27]:

p3_cantons_sum = p3_cantons_data.groupby(['Canton Shortname']).sum()


# In[29]:

# Save the sums in a csv file to use it later
try:
    p3_cantons_sum.to_csv('P3_Cantons_Sum.csv', encoding='utf-8')
except PermissionError:
    print("Couldn't access to the file. Maybe close Excel and try again :)")


# In[30]:

# Maybe a pickle file is better !


# In[31]:

p3_cantons_sum.to_pickle('P3_Cantons_Sum.pickle')

