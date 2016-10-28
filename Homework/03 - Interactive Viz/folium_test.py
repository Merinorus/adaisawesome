
# coding: utf-8

# In[1]:

import folium
map_osm = folium.Map(location=[45.5236, 44])
folium.Marker([45.5236, 44], popup='Cool place', icon = folium.Icon(icon = 'cloud')).add_to(map_osm)
map_osm.save("cool_place.html")


# In[ ]:




# In[2]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Stamen Terrain')
map_osm


# In[3]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Stamen Toner')
map_osm


# In[4]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Mapbox Bright')
map_osm


# In[5]:

import json
import geopy
googlemapsapikeyjson = json.loads(open('google_maps_api_key.json').read())
googlemapsapikey = googlemapsapikeyjson['key']
geolocator = geopy.geocoders.GoogleV3(api_key=googlemapsapikey)
adr = geolocator.geocode("University of Geneva", region='ch')


# In[ ]:

adr.raw


# In[ ]:

# displays the dictionary in a visually better way
print(json.dumps(adr.raw, indent = 4))


# In[ ]:

adr.raw['address_components']


# In[ ]:

canton_longname = None
try:
    for i in adr.raw['address_components']:
        if i["types"][0] == "country" and i["long_name"] == "Switzerland":
            print("Switzerland !")
            #if i["types"][0] == "administrative_area_level_1":
                #canton_longname = (i['long_name'])
except KeyError:
    print('No canton found')
canton_longname


# In[ ]:

adr.raw['address_componentds']


# In[ ]:

"administrative_area_level_1" in adr.raw['address_components'][*][0]


# In[ ]:

null_adr =  geolocator.geocode("azdadefqefesrhtrtdgefregesrg", region='ch')
type(null_adr)


# In[ ]:

if null_adr is None:
    print("Nonetype !")


# In[ ]:

test_table = []
test_table.append(None)
test_table.append(1)
test_table.append(None)
test_table.append(None)
test_table.append(2)
test_table


# In[ ]:

test_dic = {}
test_dic['key1'] = {}
test_dic['key1']['longname'] = ['It''s so funny']
test_dic['key1']['shortname'] = ['lol']
test_dic


# In[ ]:

test_dic['key1']


# In[ ]:

table = ['aze', 'ae']
table[2]


# In[ ]:

from time import gmtime, strftime
strftime("%Y-%m-%d %H:%M:%S", gmtime())


# In[ ]:

str('coucou')


# In[8]:

test_dic = {}
test_dic['key1'] = 'ok'
test_dic['Physikal.-Meteorolog. Observatorium Davos - PMOD'] = 'ça marche ?'


# In[9]:

# Import the Switzerland map (from the folio pylib notebook)
topo_geo = r'ch-cantons.topojson.json'

# Need to be able to extract the id of the canton from the topo file
from pprint import pprint

with open(topo_geo) as data_file:    
    data = json.load(data_file)
#pprint(data)

#data['objects']['cantons']['geometries']
data['objects']['cantons']['geometries'][0]['id']


# In[10]:

# Need to overlap the Swiss topo file on the generic Folio map
ch_map = folium.Map(location=[46.9, 8.6], tiles='Mapbox Bright', zoom_start=7)
folium.TopoJson(open(topo_geo), 'objects.cantons', name = 'topojson').add_to(ch_map)
folium.LayerControl().add_to(ch_map)
ch_map


# In[14]:

data['objects']['cantons']['geometries'][0]['id']


# In[17]:

data['objects']['cantons']['type']

