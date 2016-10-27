
# coding: utf-8

# In[3]:

#Load DataSet
import folium
import pandas as pd


# In[4]:

grants_data = pd.read_pickle('P3_Cantons_Sum.pickle')
grants_data['Canton Shortname'] = grants_data.index
grants_data = grants_data.reset_index(drop=True)
grants_data.columns = ['Total Amount','Canton']
grants_data


# In[8]:

topo_path = r'world-countries.json'
topo_path


# In[18]:

topo_path2=r'ch-cantons.topojson.json'
topo_path2


# In[12]:

ch_map = folium.Map(location=[46.8769, 8.6017], tiles='Mapbox Bright',
                    zoom_start=7)
ch_map

Now Map Switzerland with Canton Divisions
# In[22]:




# In[23]:

ch_map.choropleth(geo_path=topo_path2, data=grants_data,
             columns=['Canton', 'Total Amount'],
             key_on='objects.cantons.id',
             fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
             legend_name='Total Grants (CHF)')
ch_map


# In[ ]:




# In[ ]:




# In[ ]:



