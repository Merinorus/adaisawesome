
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import json
import geopy
import time
import math 
import logging


# In[93]:

p3_cantons_data = pd.read_pickle('P3_Cantons.pickle')
p3_cantons_data


# In[51]:

#find all possible short names
cantons = p3_cantons_data['Canton Shortname'].unique()
#create new dataframe with canton indexes
final_df= pd.Series(0, index=cantons)
final_df = final_df.to_frame(name='Total Sum')
final_df['Canton Name'] = final_df.index
final_df = final_df.reset_index(drop=True)
final_df


# In[94]:

#delete irrelevant columns in the dataset to clean data
p3_cantons_data = p3_cantons_data.drop(['Funding Instrument', 'Canton Longname', 'End Date', 'Start Date', 'Institution', 'University', 'Funding Instrument Hierarchy'], axis=1)
p3_cantons_data


# In[122]:

# convert approved amount to numeric value
#for index, row in p3_cantons_data.iterrows():
  #      float(row['Approved Amount'])
pd.to_numeric(p3_cantons_data['Canton Shortname'], errors='coerce')
p3_cantons_data


# In[120]:

#sum elements by group
p3_cantons_data.groupby(['Canton Shortname']).sum()



    
    


# In[ ]:



