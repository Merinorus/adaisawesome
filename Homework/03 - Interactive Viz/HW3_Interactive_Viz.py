
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.

# In[135]:

import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import geonames
import time
import requests


# In[136]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[137]:

p3_grant_export_data.size


# In[138]:

# We keep only the rows which mention how much money has been granted (the amount column starts by a number)
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data['Approved Amount'].apply(lambda x : x[0].isdigit())]


# In[139]:

# Almost 200k rows have been removed
p3_grant_export_data.size


# In[140]:

# We don't need this data
p3_grant_export_data = p3_grant_export_data.drop(p3_grant_export_data.columns[[0]], axis = 1)
p3_grant_export_data = p3_grant_export_data.drop(['Project Title', 'Project Title English', 'Responsible Applicant', 'Discipline Number', 'Discipline Name', 'Discipline Name Hierarchy', 'Keywords'], axis=1)
p3_grant_export_data.size


# First, we will locate projcets according to the University name.
# We will ignore all project in which the University is not mentioned : we assume that if it's not, the project is probably outside Switzerland.
# If we have the time, a better solution would be taking the institution's location into account as well.

# In[141]:

# Removing rows in which University is not mentioned
p3_grant_export_data = p3_grant_export_data.dropna(subset=['University'])
p3_grant_export_data.size


# In[142]:

p3_grant_export_data


# In[143]:

# We also delete every row that contains "Nicht zuteilbar - NA", which means that University is not mentioned.
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data.University.str.contains('Nicht zuteilbar - NA') == False]
p3_grant_export_data.head()


# In[144]:

# The 'Approved Amount' column contains string types instead of numbers
type(p3_grant_export_data['Approved Amount'][1])


# In[145]:

# Let's convert this column to float numbers, so we'll be able to do some maths
p3_grant_export_data['Approved Amount'] = p3_grant_export_data['Approved Amount'].apply(float)


# In[146]:

# Now we definitely have numbers in the 'Approved Amount' column !
type(p3_grant_export_data['Approved Amount'][1])


# Now, time to locate universities...
# For this, we are giong to use Geopy, which is a python client that works with most popular websites.

# In[147]:

json_login=open('geonames_login.json').read()
login = json.loads(json_login)
geonames_login = login['login']
geonames_password = login['password']
geonames_login


# In[148]:

googlemapsapikeyjson = json.loads(open('google_maps_api_key.json').read())
googlemapsapikey = googlemapsapikeyjson['key']


# We want to locate every university, then add the corresponding canton in a new column, on the dataframe we were dealing with before.

# In[149]:

#geolocator = geopy.geocoders.GeoNames(None, geonames_login)
geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikey)
test = geolocator.geocode("University of Geneva")
test


# The only problem is that Google maps locates the University of Geneva in United States... Since we are only interested by Swiss universities, we'll add "Switzerland" at the end of each university that we'll give in parameters to the geolocator. If it finds something, we assume the University is in Switzerland, otherwise it would be outside the country.

# In[150]:

test = geolocator.geocode("University of Geneva Switzerland")
test


# That's better !

# We'll create a table containing all the cantons corresponding to the Universities, then we'll add this new table at the end of our dataframe. So each row will be linked to a canton.

# In[151]:

# Let's count the number of distinct universities we have
p3_grant_export_data.groupby('University').Institution.nunique().size


# In[152]:

# So we will have to make about 77 request to Geonames, which isn't that much !
# We'll create a dataframe that will link each university to a canton.


# In[153]:

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

# In[154]:

university_canton_df['UniversityName'] = university_canton_df['UniversityName'].apply(lambda x: x.split(' -')[0])
university_canton_df


# In[155]:

req = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=EPF+Lausanne+-+EPFL&key=AIzaSyBHiguwVkCbbYPAy6c0ACQTrz73JvFz4PM")
json_response = req.json()
address_components = json_response["results"][0]["address_components"]
for i in address_components:
    if (i["types"][0] == "administrative_area_level_1"):
        print(i["long_name"] + " " + i["short_name"] + "")


# In[158]:

university_canton_df.UniversityName


# In[170]:

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
    


# In[161]:

len(cantons_longname_table)


# In[83]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i)
    print(canton)
    cantons_table.append(canton)


# In[94]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i)
    print(canton)
    cantons_table.append(canton)


# In[95]:

cantons_table = []
for i in university_canton_df.UniversityName:
    canton = geolocator.geocode(i + " Switzerland")
    print(canton)
    cantons_table.append(canton)


# In[84]:

cantons_table


# In[86]:

cantons_table[0]


# In[87]:

print(cantons_table[0])


# In[92]:

cantons_table[0].latitude


# In[89]:

cantons_table[0].longitude


# In[90]:

geolocator.reverse(cantons_table[0].longitude, cantons_table[0].latitude)


# In[ ]:



