
# coding: utf-8

# Obtain all the data for the Bachelor students, starting from 2007. Keep only the students for which you have an entry for both Bachelor semestre 1 and Bachelor semestre 6. Compute how many months it took each student to go from the first to the sixth semester. Partition the data between male and female students, and compute the average -- is the difference in average statistically significant?

# In[96]:

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlcontent = BeautifulSoup(r.content, 'html.parser')
print(htmlcontent.prettify())


# In[98]:

computersciencefield = htmlcontent.find('option', text='Informatique')
computersciencefield.get('value')


# In[99]:

year = htmlcontent.find('option', text='2007-2008')
year.get('value')


# In[112]:

yearshtml = htmlcontent.findAll('input', attrs={'name' : 'zz_x_PERIODE_ACAD'})
#if yearshtml:
for option in yearshtml[0].findAll('option'):
    years = pd.DataFrame({'year':[option.text],'code':[option.get('value')]})
years


# In[90]:

yearshtml


# In[ ]:



