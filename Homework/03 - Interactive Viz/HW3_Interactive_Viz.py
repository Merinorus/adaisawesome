
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.

# In[239]:

import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import geonames
import time
import requests
import math
import logging


# In[275]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[276]:

p3_grant_export_data.size


# In[277]:

# We keep only the rows which mention how much money has been granted (the amount column starts by a number)
p3_grant_export_data = p3_grant_export_data[p3_grant_export_data['Approved Amount'].apply(lambda x : x[0].isdigit())]


# In[278]:

# Almost 200k rows have been removed
p3_grant_export_data.size


# In[279]:

# We don't need this data
p3_grant_export_data = p3_grant_export_data.drop(p3_grant_export_data.columns[[0]], axis = 1)
p3_grant_export_data = p3_grant_export_data.drop(['Project Title', 'Project Title English', 'Responsible Applicant', 'Discipline Number', 'Discipline Name', 'Discipline Name Hierarchy', 'Keywords'], axis=1)
p3_grant_export_data.size


# First, we will locate projcets according to the University name.
# We will ignore all project in which the University is not mentioned : we assume that if it's not, the project is probably outside Switzerland.
# If we have the time, a better solution would be taking the institution's location into account as well.

# In[60]:

# Removing rows in which University is not mentioned
# p3_grant_export_data = p3_grant_export_data.dropna(subset=['University'])
# p3_grant_export_data.size


# In[280]:

p3_grant_export_data


# Using only university names as a parametrer for geolocators isn't enough, because we get about half of the results.
# A better idea would be using university name, and if there is no result, using the institution name as a second chance.  
# We will then take both universities and institution names into account in order to do our research:
# 1) Create initial data containers :
#     - a key-value (name-canton) dictionary for universities and institutions :
#         -['University', 'Canton'] and ['Institution', 'Canton']
#     - a table that contains all cantons that have been found
# 2) Go trough the dataframe:
#   - Check if the university name exists in our index. If not, geolocate the address 
#   - Check if the address is in Switzerland, otherwise canton will be considered as 'None'
#   - If the university address is not found, try to find it with institution name, the same way as above
#   - Extract the canton of the address (if it found an address and if it's in Switzerland). If no canton, let's say 'None' canton
#   - Add the canton name to a the dictionary (or add something like 'None' if no canton has been found), so next university or institution that has been already found won't have to be geolocated again
#   - Add the canton to the canton table
# 3) Add the canton table to the above dataframe in a way that they match with the universities or institutions

# In[281]:

# Let's start by creating our geolocator. We will use Google Maps API :
googlemapsapikeyjson = json.loads(open('google_maps_api_keys.json').read())
googlemapsapikeys = googlemapsapikeyjson['keys']


# In[282]:

geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikeys[0])
# Do a test with University of Geneva
test_university_geneva = geolocator.geocode("University of Geneva")
test_university_geneva


# University of Geneva may appear to be in USA ! But the one of our Dataframe is without a doubt the Swiss one.

# In[283]:

# Specifying the region for the geolocator
test_university_geneva = geolocator.geocode("University of Geneva", region='ch')
test_university_geneva


# That's much better !
# Now let's start by creating the indexes for universities and institutions :

# In[154]:

university_canton_dict = {}
institution_canton_dict = {}


# In[299]:




# In[302]:




# In[304]:

# We can already add the values in our dataframe that won't lead to an address
university_canton_dict['Nicht zuteilbar - NA'] # it means "Not Available" in German !
institution_canton_dict['NaN'] = {'long_name': None, 'short_name': None}
institution_canton_dict['nan'] = {'long_name': None, 'short_name': None}


# We will need to log the next steps in order de debug easily the part of code related to geolocation...

# In[308]:

# set root logger level
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# setup custom logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('geolocation8.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# log
logger.info('This file is used to debug the next code part related to geolocation of universities/institutions')


# It's kinda dirty, but we will need more than one API key to make all the requests we need for our data.
# So we created several Google API keys and switch the key each time the current one cannot be used anymore !

# In[309]:

# We create tables that will contains every canton we find, so we'll be able to match it with the dataframe at the end.
logger.debug('Beginning of geolocation : creating canton tables')
canton_shortname_table = [] # eg: VD
canton_longname_table = []# eg: Vaud

# number of rows analysed. Can be limited for debuging (eg : 10) because the number of requests to Google Maps API is limited !
MAX_ROWS = 10 # max : math.inf 
row_counter = 0

# maximum duration of a query to the geocoder, in seconds
geocoder_timeout = 5

# We're going to use more than one API key if we want to make all the requests !! :@
APIkeynumber = 0

# The following lines make the geolocator stubborn : it uses all the keys that are available and if it gets a timeout error, it tries again... indefinitely !
        
def stubborn_geocode(geolocator, address):
    global APIkeynumber
    try:
        #print("Using API key n°" + str(APIkeynumber))
        geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikeys[APIkeynumber])
        return geolocator.geocode(address, region='ch', timeout=geocoder_timeout)
    except geopy.exc.GeocoderTimedOut:
        print("Error : the geocoder timed out. Let's try again...")
        return stubborn_geocode(geolocator, address)
    
    except geopy.exc.GeocoderQuotaExceeded:
        print("Error : The given key has gone over the requests limit in the 24 hour period or has submitted too many requests in too short a period of time. Let's try again with a different key...")
        APIkeynumber = APIkeynumber + 1
        try:
            print("Trying API key n°" + str(APIkeynumber) + "...")           
            return stubborn_geocode(geolocator, address)
        except IndexError:
            print("Error : Out of API keys ! We need to request another API key from Google :(")
            print("When you get a new API key, add it to the json file containing the others keys.")
            # We have to stop there...
            raise
    
    
        

    
# Go through the dataframe
for index, row in p3_grant_export_data.iterrows():
    logger.debug("Iterating over row n°" + str(row_counter) + ":")
    # initialize variables that will contain canton name for the current row
    canton_longname = None
    canton_shortname = None
    # Check if the university name exists in our index
    university_name = row['University']
    institution_name = row['Institution']
    if university_name in university_canton_dict:
        # The university has already been located. Let's add the canton to the canton table
        if university_canton_dict[university_name]['long_name'] is not None:
            logger.debug('University already exists in dictionary (' + university_canton_dict[university_name]['long_name'] + ')')
        else:
            logger.debug('University already exists in dictionary, but no canton is associated to it (it might be outside Switzerland).')
        
        #canton_shortname_table.append(university_canton_dict[university_name]['short_name'])
        #canton_longname_table.append(university_canton_dict[university_name]['long_name'])
        canton_longname = university_canton_dict[university_name]['long_name']
        canton_shortname = university_canton_dict[university_name]['short_name']
    
    elif institution_name in institution_canton_dict:
        # The institution has already ben located, so we add its canton to the canton table
        logger.debug('University wasn''t found, but institution already exists in dictionary (' + institution_canton_dict[institution_name]['long_name'] + ')')
        
        #canton_shortname_table.append(institution_canton_dict[institution_name]['short_name'])
        #canton_longname_table.append(institution_canton_dict[institution_name]['long_name'])
        canton_longname = institution_canton_dict[institution_name]['long_name']
        canton_shortname = institution_canton_dict[institution_name]['short_name']
    
    else:
        # Nor the university neither the institution has been found yet, so we have to geolocate it
        logger.debug('No university/institution found in dictionaries, geolocating...')
        adr = stubborn_geocode(geolocator, university_name)
        if adr is None:
            # TODO No address has been found for this University. So we have to do the same with Institution           
            adr = stubborn_geocode(geolocator, institution_name)
            
        # Now, the address should have been found, either by locating the university or the institution
        if adr is not None:                 
            # Check if it's a Swiss address, if yes add the canton to the table
            try:
                swiss_address = False
                for i in adr.raw['address_components']:
                    if i["types"][0] == "country" and i["long_name"] == "Switzerland":
                        # The address is located in Switerland
                        swiss_address = True
                # So, we go on only if we found a Swiss address. Otherwise, there is no point to continue.
                if swiss_address:
                    for i in adr.raw['address_components']:
                        if i["types"][0] == "administrative_area_level_1":
                            # We found a canton !
                            canton_longname = (i['long_name'])
                            canton_shortname = (i['short_name'])
                            # We also add it to the university/institution dictionary, in order to limit the number of requests
                            university_canton_dict[university_name] = {}
                            university_canton_dict[university_name]['short_name'] = canton_shortname
                            university_canton_dict[university_name]['long_name'] = canton_longname
                            institution_canton_dict[institution_name] = {}
                            institution_canton_dict[institution_name]['short_name'] = canton_shortname
                            institution_canton_dict[institution_name]['long_name'] = canton_longname
                            break
            
            except IndexError:
                # I don't know where this error comes from exactly, just debugging... it just comes from this line :
                # if i["types"][0] == "country" and i["long_name"] == "Switzerland":
                # For the moment I assume that the the address doesn't match the requirements, so it should not be located in Switzerland
                # Thus, we just forget it and look for the next address.
                print("IndexError : no canton found for the current row")
                
            except KeyError:
                print("KeyError : no canton found for the current row")
                print("Current item: n°" + str(len(canton_shortname_table)))
                # The address doesn't act as excpected. There are two possibilities :
                # - The address doesn't contain the field related to the canton
                # - The address doesn't contain the field related to the country
                # So we don't consider this address as a Swiss one and we give up with this one.
    
    # Let's add what we found about the canton !
    # If we didn't find any canton for the current university/institution, it will just append 'None' to the tables.
    if canton_longname is not None:
        logger.debug("Appending canton to the table: " + canton_longname)
    else:
        logger.debug("Appending canton to the table: None")
    canton_shortname_table.append(canton_shortname)
    canton_longname_table.append(canton_longname)
            

    row_counter = row_counter + 1
    if row_counter >= MAX_ROWS:
        print("Maximum number of rows reached ! (" + str(MAX_ROWS) + ")")
        print("Increase the MAX_ROWS variable to analyse more locations")
        print("No limit : MAX_ROWS = maths.inf")
        break


# In[292]:

# We have the table containing all cantons !
len(canton_shortname_table)


# In[310]:

canton_longname_table


# In[311]:

university_canton_dict


# In[301]:

# Same with the dictionary (we save it)
with open('university_canton_dict.json', 'w') as fp:
    json.dump(university_canton_dict, fp, sort_keys=True, indent=4)
university_canton_dict


# In[237]:

with open('institution_canton_dict.json', 'w') as fp:
    json.dump(institution_canton_dict, fp, indent=4)
institution_canton_dict


# In[227]:

canton_shortname_series = pd.Series(canton_shortname_table, name='Canton Shortname')
canton_shortname_series.size


# In[228]:

canton_longname_series = pd.Series(canton_longname_table, name='Canton Longname')
canton_longname_series.size


# In[229]:

p3_grant_cantons.size


# In[222]:

# Let's add the cantons to our dataframe !
canton_shortname_series = pd.Series(canton_shortname_table, name='Canton Shortname')
canton_longname_series = pd.Series(canton_longname_table, name='Canton Longname')
p3_grant_cantons = pd.concat([p3_grant_export_data, canton_longname_series, canton_shortname_series], axis=1)
p3_grant_cantons.columns.get_value
p3_grant_cantons


# Now we have the cantons associated with the universities/institutions :)

# In[223]:

p3_grant_cantons.to_csv('P3_Cantons.csv')


# In[ ]:




# In[ ]:




# THE FOLLOWING CODE HAS TO BE CHECKED, WE CAN DROP SOME OF IT (don't worry, it can be taken back from ancient commits on GitHub)

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

googlemapsapikeyjson = json.loads(open('google_maps_api_keys.json').read())
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



