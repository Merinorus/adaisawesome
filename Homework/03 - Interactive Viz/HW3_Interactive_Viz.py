
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.

# In[147]:

import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import geonames


# In[106]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[107]:

p3_grant_export_data.size


# In[108]:

# We keep only the rows which mention how much money has been granted (the amount column starts by a number)
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data['Approved Amount'].apply(lambda x : x[0].isdigit())]


# In[109]:

# Almost 200k rows have been removed
p3_grant_export_data.size


# In[110]:

# We don't need this data
p3_grant_export_data = p3_grant_export_data.drop(p3_grant_export_data.columns[[0]], axis = 1)
p3_grant_export_data = p3_grant_export_data.drop(['Project Title', 'Project Title English', 'Responsible Applicant', 'Discipline Number', 'Discipline Name', 'Discipline Name Hierarchy', 'Keywords'], axis=1)
p3_grant_export_data.size


# First, we will locate projcets according to the University name.
# We will ignore all project in which the University is not mentioned : we assume that if it's not, the project is probably outside Switzerland.
# If we have the time, a better solution would be taking the institution's location into account as well.

# In[111]:

# Removing rows in which University is not mentioned
p3_grant_export_data = p3_grant_export_data.dropna(subset=['University'])
p3_grant_export_data.size


# In[112]:

p3_grant_export_data


# In[104]:

# We also delete every row that contains "Nicht zuteilbar - NA", which means that University is not mentioned.
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data.University.str.contains('Nicht zuteilbar - NA') == False]
p3_grant_export_data.head()


# In[119]:

# The 'Approved Amount' column contains string types instead of numbers
type(p3_grant_export_data['Approved Amount'][0])


# In[127]:

# Let's convert this column to float numbers, so we'll be able to do some maths
p3_grant_export_data['Approved Amount'] = p3_grant_export_data['Approved Amount'].apply(float)


# In[128]:

# Now we definitely have numbers in the 'Approved Amount' column !
type(p3_grant_export_data['Approved Amount'][0])


# Now, time to locate universities...
# For this, we are giong to use Geopy, which is a python client that works with most popular websites.

# In[137]:

json_login=open('geonames_login.json').read()
login = json.loads(json_login)
geonames_login = login['login']
geonames_password = login['password']


# We want to locate every university, then add the corresponding canton in a new column, on the dataframe we were dealing with before.

# In[171]:

geolocator = geopy.geocoders.GeoNames(None, geonames_login)
test = geolocator.geocode("University of Geneva")
test


# We'll create a table containing all the cantons corresponding to the Universities, then we'll add this new table at the end of our dataframe. So each row will be linked to a canton.

# In[182]:

# Let's count the number of distinct universities we have
p3_grant_export_data.groupby('University').Institution.nunique().size


# In[ ]:

# So we will have to make about 77 request to Geonames, which isn't that much !
# We'll create a dataframe that will link each university to a canton.


# In[236]:

university_canton_df = p3_grant_export_data.groupby('University').Institution.nunique()
university_canton_df = pd.DataFrame(university_canton_df)
#university_canton_df = university_canton_df.rename(columns = {'Institution':'Canton'})
university_canton_df = p3_grant_export_data.groupby('University').Institution.nunique()
university_canton_df = pd.DataFrame(university_canton_df)
university_canton_df['UniversityName'] = university_canton_df.index
university_canton_df = university_canton_df.drop('Institution', axis = 1)
university_canton_df = university_canton_df.reset_index(drop=True)
university_canton_df.head()


# TODO  : we need to remove the acronym at the end of each row, maybe it might help getting more results with geocodes.

# In[240]:

university_canton_df['UniversityName'] = university_canton_df['UniversityName'].apply(lambda x: x.split(' -')[0])
university_canton_df.head()


# In[231]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i)
    cantons_table.append(canton)


# In[238]:

cantons_table

