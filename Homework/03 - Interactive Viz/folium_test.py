
# coding: utf-8

# In[21]:

import folium
map_osm = folium.Map(location=[45.5236, 44])
folium.Marker([45.5236, 44], popup='Cool place', icon = folium.Icon(icon = 'cloud')).add_to(map_osm)
map_osm.save("cool_place.html")


# In[ ]:




# In[8]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Stamen Terrain')
map_osm


# In[9]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Stamen Toner')
map_osm


# In[10]:

map_osm = folium.Map(location=[45.5236, 44], tiles='Mapbox Bright')
map_osm


# In[ ]:



