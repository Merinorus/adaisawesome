
# coding: utf-8

# In this part of the exercise, we now need to put the data which we have procured about the funding levels of the different universities that are located in different cantons onto a canton map. We will do so using Folio and take the example TopoJSON mapping which they use.

# In[15]:

import folium
import pandas as pd


# In[49]:

# Test seeing Switzerland
ch_map = folium.Map(location=[47.3769, 8.5417], tiles='Stamen Toner',
                    zoom_start=13)
ch_map.save('stamen_toner.html')
ch_map


# Now do the TopoJSON overlay

# In[61]:

# Import the Switzerland map (from the folio pylib notebook)
topo_path = r'ch-cantons.topojson.json'
# Import our csv file with all of the values for the amounts of the grants 
data = 'P3_GrantExport.csv'

# Insert coordinates that are for Switzerland (i.e. 9.594226,47.525058)
ch_map = folium.Map(location=[46.8769, 8.6017], tiles='Mapbox Bright',
                    zoom_start=7)
ch_map.choropleth(geo_path=topo_path, topojson='objects.ch-cantons')
ch_map.save('ch_map.html')
ch_map


# In[ ]:

# Need to use colors wisely - becaue this is continuous and not descrete, we will be using different shades of green

