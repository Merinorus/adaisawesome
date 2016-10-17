
# coding: utf-8

# Obtain all the data for the Bachelor students, starting from 2007. Keep only the students for which you have an entry for both Bachelor semestre 1 and Bachelor semestre 6. Compute how many months it took each student to go from the first to the sixth semester. Partition the data between male and female students, and compute the average -- is the difference in average statistically significant?

# In[57]:

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import urllib
import csv


# In[58]:

r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlContent = BeautifulSoup(r.content, 'html.parser')
print(htmlContent.prettify())


# In[59]:

# We first get the "Computer science" value
computerScienceField = htmlContent.find('option', text='Informatique')
computerScienceField


# In[60]:

computerScienceValue = computerScienceField.get('value')
computerScienceValue


# In[61]:

# Then, we're going to need all the academic years values.
academicYearsField = htmlContent.find('select', attrs={'name':'ww_x_PERIODE_ACAD'})
academicYearsSet = academicYearsField.findAll('option')

# Since there are several years to remember, we're storing all of them in a table to use them later
academicYearValues = []
# We'll put the textual content in a table aswell ("Master semestre 1", "Master semestre 2"...)
academicYearContent = []

for option in academicYearsSet:
    value = option.get('value')
    # However, we don't want any "null" value
    if value != 'null':
        academicYearValues.append(value)
        academicYearContent.append(option.text)


# In[62]:

# Now, we have all the academic years that might interest us
academicYear_Series = pd.Series(academicYearContent, index=academicYearValues)
academicYear_Series


# In[63]:

# Then, let's get all the pedagogic periods we need. It's a little bit more complicated here because we need to link the pedagogic period with a season (eg : Bachelor 1 is autumn, Bachelor 2 is spring etc.)
# Thus, we need more than the pedagogic values. For doing some tests to associate them with the right season, we need the actual textual value ("Bachelor semestre 1", "Bachelor semestre 2" etc.)
pedagogicPeriodsField = htmlContent.find('select', attrs={'name':'ww_x_PERIODE_PEDAGO'})
pedagogicPeriodsSet = pedagogicPeriodsField.findAll('option')

# Same as above, we'll store the values in a table
pedagogicPeriodValues = []
# We'll put the textual content in a table aswell ("Master semestre 1", "Master semestre 2"...)
pedagogicPeriodContent = []

for option in pedagogicPeriodsSet:
    value = option.get('value')
    if value != 'null':
        pedagogicPeriodValues.append(value)
        pedagogicPeriodContent.append(option.text)


# In[64]:

# Let's make the values and content meet each other
pedagogicPeriod_Series = pd.Series(pedagogicPeriodContent, index=pedagogicPeriodValues)
pedagogicPeriod_Series


# In[65]:

# We keep all semesters related to Bachelor students
bachelorPedagogicPeriod_Series = pedagogicPeriod_Series[[name.startswith('Bachelor') for name in pedagogicPeriod_Series]]
bachelorPedagogicPeriod_Series


# In[66]:

# Lastly, we need to extract the values associated with autumn and spring semesters.
semesterTypeField = htmlContent.find('select', attrs={'name':'ww_x_HIVERETE'})
semesterTypeSet = semesterTypeField.findAll('option')

# Again, we need to store the values in a table
semesterTypeValues = []
# We'll put the textual content in a table aswell
semesterTypeContent = []

for option in semesterTypeSet:
    value = option.get('value')
    if value != 'null':
        semesterTypeValues.append(value)
        semesterTypeContent.append(option.text)


# In[67]:

# Here are the values for autumn and spring semester :
semesterType_Series = pd.Series(semesterTypeContent, index=semesterTypeValues)
semesterType_Series


# In[68]:

cases = {}
for element in semesterTypeValues:
    cases[element.a.get_text()] = {}
cases[0].a['href']


# In[69]:


<a href="http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247" name='ww_x_PERIODE_ACAD' id=periodAcad</a>


# In[78]:




# In[ ]:




# In[ ]:



