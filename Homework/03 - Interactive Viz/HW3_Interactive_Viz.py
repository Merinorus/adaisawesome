
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.

# In[54]:

import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import geonames
import time
import requests


# In[55]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[56]:

p3_grant_export_data.size


# In[57]:

# We keep only the rows which mention how much money has been granted (the amount column starts by a number)
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data['Approved Amount'].apply(lambda x : x[0].isdigit())]


# In[58]:

# Almost 200k rows have been removed
p3_grant_export_data.size


# In[59]:

# We don't need this data
p3_grant_export_data = p3_grant_export_data.drop(p3_grant_export_data.columns[[0]], axis = 1)
p3_grant_export_data = p3_grant_export_data.drop(['Project Title', 'Project Title English', 'Responsible Applicant', 'Discipline Number', 'Discipline Name', 'Discipline Name Hierarchy', 'Keywords'], axis=1)
p3_grant_export_data.size


# First, we will locate projcets according to the University name.
# We will ignore all project in which the University is not mentioned : we assume that if it's not, the project is probably outside Switzerland.
# If we have the time, a better solution would be taking the institution's location into account as well.

# In[60]:

# Removing rows in which University is not mentioned
p3_grant_export_data = p3_grant_export_data.dropna(subset=['University'])
p3_grant_export_data.size


# In[61]:

p3_grant_export_data


# Using only university names as a parametrer for geolocators isn't enough, because we get about half of the results.
# A better idea would be using university name, and if there is no result, using the institution name as a second chance.  
# We will then take both universities and institution names into account in order to do our research:
# 1) Create a key-value (name-canton) dictionary for universities and institutions :
#     ['University', 'Canton'] and ['Institution', 'Canton']
# 2) Go trough the dataframe:
#   - Check if the university name exists in our index. If not, geolocate the address 
#   - If several addresses are returned, check one that is in Switzerland (eg: University of Geneva uses to be found is US !)
#   - If the university address is not relevant, try to find it with institution name, the same way as above
#   - Extract the canton of the address (if it found an address and if it's in Switzerland). If no canton, let's say 'None' canton
#   - Add the canton name to a the dictionary (or add something like 'None' if no canton has been found), so next university or institution that has been already found won't have to be geolocated again
#   - Add the canton to a table
# 3) Add the canton table to the above dataframe in a way that they match with the universities or institutions

# In[ ]:




# In[66]:

# Let's start by creating our geolocator. We will use Google Maps API :
googlemapsapikeyjson = json.loads(open('google_maps_api_key.json').read())
googlemapsapikey = googlemapsapikeyjson['key']


# In[68]:

#geolocator = geopy.geocoders.GeoNames(None, geonames_login)
geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikey)
test_university_geneva = geolocator.geocode("University of Geneva")
test_university_geneva


# That's why we have to be careful and check if an address is relevant to Switzerland !
# So let's start by creating the indexes for 

# In[ ]:




# THE FOLLOWING CODE HAS TO BE CHECKED

# In[62]:

# We also delete every row that contains "Nicht zuteilbar - NA", which means that University is not mentioned.
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data.University.str.contains('Nicht zuteilbar - NA') == False]
p3_grant_export_data.head()


# In[63]:

# The 'Approved Amount' column contains string types instead of numbers
type(p3_grant_export_data['Approved Amount'][1])


# In[64]:

# Let's convert this column to float numbers, so we'll be able to do some maths
# p3_grant_export_data['Approved Amount'] = p3_grant_export_data['Approved Amount'].apply(float)
p3_grant_export_data['Approved Amount'] = p3_grant_export_data['Approved Amount'].astype(float)
#p3_grant_export_data['Approved Amount']


# In[65]:

# Now we definitely have numbers in the 'Approved Amount' column !
type(p3_grant_export_data['Approved Amount'][1])


# Now, time to locate universities...
# For this, we are giong to use Geopy, which is a python client that works with most popular websites.

# In[16]:

json_login=open('geonames_login.json').read()
login = json.loads(json_login)
geonames_login = login['login']
geonames_password = login['password']
geonames_login


# In[17]:

googlemapsapikeyjson = json.loads(open('google_maps_api_key.json').read())
googlemapsapikey = googlemapsapikeyjson['key']


# We want to locate every university, then add the corresponding canton in a new column, on the dataframe we were dealing with before.

# In[18]:

#geolocator = geopy.geocoders.GeoNames(None, geonames_login)
geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikey)
test = geolocator.geocode("University of Geneva")
test


# The only problem is that Google maps locates the University of Geneva in United States... Since we are only interested by Swiss universities, we'll add "Switzerland" at the end of each university that we'll give in parameters to the geolocator. If it finds something, we assume the University is in Switzerland, otherwise it would be outside the country.

# In[19]:

test = geolocator.geocode("University of Geneva Switzerland")
test


# That's better !

# We'll create a table containing all the cantons corresponding to the Universities, then we'll add this new table at the end of our dataframe. So each row will be linked to a canton.

# In[20]:

# Let's count the number of distinct universities we have
p3_grant_export_data.groupby('University').Institution.nunique().size


# THE FOLLOWING CODE HAS TO BE CHECKED

# In[21]:

# So we will have to make about 77 request to Geonames, which isn't that much !
# We'll create a dataframe that will link each university to a canton.


# In[22]:

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

# In[23]:

university_canton_df['UniversityName'] = university_canton_df['UniversityName'].apply(lambda x: x.split(' -')[0])
university_canton_df.head()


# In[ ]:

req = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=EPF+Lausanne+-+EPFL&key=AIzaSyBHiguwVkCbbYPAy6c0ACQTrz73JvFz4PM")
json_response = req.json()
address_components = json_response["results"][0]["address_components"]
for i in address_components:
    if (i["types"][0] == "administrative_area_level_1"):
        print(i["long_name"] + " " + i["short_name"] + "")


# In[ ]:

university_canton_df.UniversityName


# In[ ]:

cantons_longname_table = []
cantons_shortname_table = []
for i in university_canton_df.UniversityName:
    # Create a request to Google maps API
    request = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    print(i)
    i = i + " Switzerland"
    i = i.replace (" ", "+")
    request = request + i
    request = request + "&key=" + googlemapsapikey
    req = requests.get(request)
    json_response = req.json()
    address_components = None
    try:
        address_components = json_response["results"][0]["address_components"]
        for i in address_components:
            canton_longname = None
            canton_shortname = None
            if (i["types"][0] == "administrative_area_level_1"):
                if i["long_name"] is not None:
                    canton_longname = i["long_name"]
                if i["short_name"] is not None:
                    cantons_shortname = i["short_name"]
            
            cantons_longname_table.append(canton_longname)
            cantons_shortname_table.append(canton_shortname)
            if canton_longname is not None:
                print("  canton: " + canton_longname)
            else:
                print("  canton not found")
             
                
    except IndexError:
        cantons_longname_table.append(None)
        cantons_shortname_table.append(None)
        print("  no result")
    


# In[ ]:

len(cantons_longname_table)


# In[ ]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i)
    print(canton)
    cantons_table.append(canton)


# In[ ]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i)
    print(canton)
    cantons_table.append(canton)


# In[ ]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i + " Switzerland")
    print(canton)
    cantons_table.append(canton)


# In[ ]:

cantons_table


# In[ ]:

cantons_table[0]


# In[ ]:

print(cantons_table[0])


# In[ ]:

cantons_table[0].latitude


# In[ ]:

cantons_table[0].longitude


# In[ ]:

geolocator.reverse(cantons_table[0].longitude, cantons_table[0].latitude)


# In[ ]:



