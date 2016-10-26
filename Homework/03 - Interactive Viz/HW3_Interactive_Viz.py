
# coding: utf-8

# Build a Choropleth map which shows intuitively (i.e., use colors wisely) how much grant money goes to each Swiss canton.

# In[239]:

import pandas as pd
import numpy as np
# We will read json files, for instance API keys stored in our computers for using Google Maps API, so they're not publicly visible
import json
# Geolocation
import geopy
from geopy.geocoders import geonames
import math
import logging


# In[275]:

p3_grant_export_data = pd.read_csv("P3_GrantExport.csv", sep=";")
p3_grant_export_data


# In[363]:

# Here is the total number of rows we will have to deal with
len(p3_grant_export_data.index)


# In[277]:

# We keep only the rows which mention how much money has been granted (the amount column starts by a number)
# ie : we keep rows where the 'Approved Amount' column starts with a number
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
# We might need several API keys, to make a potentially huge number of requests
googlemapsapikeys = googlemapsapikeyjson['keys']


# In[366]:

# Specifying the region for the geolocator, because University of Geneva
test_university_geneva = geolocator.geocode("University of Geneva", region='ch')
test_university_geneva


# Now let's start by creating the indexes for universities and institutions :

# In[154]:

try:
    university_canton_dict = json.loads(open('university_canton_dict.json').read())
except FileNotFoundError:
    print('The dictionary for universities has not been saved yet. Let''s create a new dictionary.')
    university_canton_dict = {}
    
try:
    institution_canton_dict = json.loads(open('institution_canton_dict.json').read())
except FileNotFoundError:
    print('The dictionary for institutions has not been saved yet. Let''s create a new dictionary.')
    institution_canton_dict = {}


# We excpect some dirty values if the dataframe, so we are anticipate the problems:

# In[318]:

# We can already add the values in our dataframe that won't lead to an address
university_canton_dict['Nicht zuteilbar - NA'] = {'long_name': 'N/A', 'short_name': 'N/A'} # it means "Not Available" in German !
institution_canton_dict['NaN'] = {'long_name': 'N/A', 'short_name': 'N/A'}
institution_canton_dict['nan'] = {'long_name': 'N/A', 'short_name': 'N/A'}


# We will need to log the next steps in order de debug easily the part of code related to geolocation...
# It seems like it's hard to create a log file in iPython, so we adapted the following of code. Basically, it writes to a file named geolocation.log

# In[336]:

# set root logger level
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# setup custom logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('geolocation.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# log
logger.info('This file is used to debug the next code part related to geolocation of universities/institutions')


# It's rather dirty, but we will need more than one API key to make all the requests we need for our data.
# So we created several Google API keys and switch the key each time the current one cannot be used anymore !
# Here is the main code to get all the cantons that we will associate with our dataframe:

# In[337]:

# We create tables that will contains every canton we find, so we'll be able to match it with the dataframe at the end.
logger.debug('Beginning of geolocation : creating canton tables')
canton_shortname_table = [] # eg: VD
canton_longname_table = []# eg: Vaud

# number of rows analysed. Can be limited for debuging (eg : 10) because the number of requests to Google Maps API is limited !
MAX_ROWS = math.inf # values between 0 and math.inf 
row_counter = 0 # will be incremented each time we iterate over a row

# maximum duration of a query to the geocoder, in seconds
geocoder_timeout = 5

# We're going to use more than one API key if we want to make all the requests !! :@
# Keys are referenced in a table, se we start with the first key:
APIkeynumber = 0

# This function definition makes the geolocator "stubborn" : it uses all the keys that are available and if it gets a timeout error, it just tries again !        
def stubborn_geocode(geolocator, address):
    global APIkeynumber
    
    try:
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
            # We have to stop there... the error will be raised and the execution stopped.
            raise

    
# Go through the dataframe that contains all universities and institutions
for index, row in p3_grant_export_data.iterrows():
    logger.debug("Iterating over row n°" + str(row_counter) + ":")
    # initialize variables that will contain canton name for the current row
    canton_longname = 'N/A'
    canton_shortname = 'N/A'
    # Check if the university name exists in our index
    university_name = row['University']
    institution_name = row['Institution']
    if university_name in university_canton_dict:
        # The university has already been located. Let's add the canton to the canton table
        if university_canton_dict[university_name]['long_name'] is not None:
            logger.debug('University already exists in dictionary (' + university_canton_dict[university_name]['long_name'] + ')')
        else:
            logger.debug('University already exists in dictionary, but no canton is associated to it (it might be outside Switzerland).')
        
        canton_longname = university_canton_dict[university_name]['long_name']
        canton_shortname = university_canton_dict[university_name]['short_name']
    
    elif institution_name in institution_canton_dict:
        # The institution has already ben located, so we add its canton to the canton table
        logger.debug('University wasn''t found, but institution already exists in dictionary (' + institution_canton_dict[institution_name]['long_name'] + ')')
        
        canton_longname = institution_canton_dict[institution_name]['long_name']
        canton_shortname = institution_canton_dict[institution_name]['short_name']
    
    else:
        # Nor the university neither the institution has been found yet, so we have to geolocate it
        logger.debug(str(university_name) + ' / ' + str(institution_name) + ' not found in dictionaries, geolocating...')
        adr = stubborn_geocode(geolocator, university_name)
        if adr is None:
            # No address has been found for this University. So we have to do the same with Institution           
            adr = stubborn_geocode(geolocator, institution_name)
            
        # Now, the address should have been found, either by locating the university or the institution
        if adr is not None:                 
            # Check if it's a Swiss address and finds the right canton
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
    # If we didn't find any canton for the current university/institution, it will just append 'N/A' to the tables.
    logger.debug("Appending canton to the table: " + canton_longname)
    canton_shortname_table.append(canton_shortname)
    canton_longname_table.append(canton_longname)
    
    # We also add it to the university/institution dictionary, in order to limit the number of requests
    university_canton_dict[university_name] = {}
    university_canton_dict[university_name]['short_name'] = canton_shortname
    university_canton_dict[university_name]['long_name'] = canton_longname
    institution_canton_dict[institution_name] = {}
    institution_canton_dict[institution_name]['short_name'] = canton_shortname
    institution_canton_dict[institution_name]['long_name'] = canton_longname
            

    row_counter = row_counter + 1
    if row_counter >= MAX_ROWS:
        print("Maximum number of rows reached ! (" + str(MAX_ROWS) + ")")
        print("Increase the MAX_ROWS variable to analyse more locations")
        print("No limit : MAX_ROWS = maths.inf")
        break


# In[367]:

# We have the table containing all cantons !
len(canton_shortname_table)


# In[338]:

canton_longname_table


# In[343]:

# We save the dictionary of cantons associated with universities
# Thus we won't need to make requests that have already been made to Google Maps next time we run this notebook !
with open('university_canton_dict.json', 'w') as fp:
    json.dump(university_canton_dict, fp, indent=4)
university_canton_dict


# In[344]:

# We save the dictionary of cantons/institutions as well
with open('institution_canton_dict.json', 'w') as fp:
    json.dump(institution_canton_dict, fp, indent=4)
institution_canton_dict


# In[345]:

canton_shortname_series = pd.Series(canton_shortname_table, name='Canton Shortname')
canton_shortname_series.size


# In[346]:

canton_longname_series = pd.Series(canton_longname_table, name='Canton Longname')
canton_longname_series.size


# In[350]:

len(p3_grant_export_data.index)


# In[353]:

# Reindex the dataframe to make the match with cantons
p3_grant_export_data_reindex = p3_grant_export_data.reset_index(drop=True)
p3_grant_export_data_reindex


# In[354]:

# Let's add the cantons to our dataframe !
p3_grant_cantons = pd.concat([p3_grant_export_data_reindex, canton_longname_series, canton_shortname_series], axis=1)
p3_grant_cantons.columns.get_value
p3_grant_cantons


# Now we have the cantons associated with the universities/institutions :)
# We save the dataframe into several formats, just in case, in order to use them in another notebook.

# In[357]:

p3_grant_cantons.to_csv('P3_Cantons.csv', encoding='utf-8')


# In[360]:

p3_grant_cantons_json = p3_grant_cantons.to_json()
with open('P3_cantons.json', 'w') as fp:
    json.dump(p3_grant_cantons_json, fp, indent=4)


# In[361]:

# The pickle format seems convenients to works with in Python, we're going to use it for transfering data to another notebook
p3_grant_cantons.to_pickle('P3_Cantons.pickle')


# This is the end of the first part. Now that we have linked universities and institutions to cantons, we can start working with the map !
