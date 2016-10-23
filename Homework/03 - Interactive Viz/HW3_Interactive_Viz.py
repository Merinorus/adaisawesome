
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.
# Good luck

# In[2]:

import pandas as pd
import numpy as np


# In[22]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[23]:

p3_grant_export_data = p3_grant_export_data[p3_grant_export_data['Approved Amount'].apply(lambda x : x.isnumeric())]


# In[24]:

p3_grant_export_data


# In[ ]:

df[df.id.apply(lambda x: x.isnumeric())]


# In[28]:

str.isnumeric('200.92')


# In[27]:

str.isnumeric('200')

