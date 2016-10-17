
# coding: utf-8

# Obtain all the data for the Master students, starting from 2007. Compute how many months it took each master student to complete their master, for those that completed it. Partition the data between male and female students, and compute the average -- is the difference in average statistically significant?
# 
# Notice that master students' data is more tricky than the bachelors' one, as there are many missing records in the IS-Academia database. Therefore, try to guess how much time a master student spent at EPFL by at least checking the distance in months between Master semestre 1 and Master semestre 2. If the Mineur field is not empty, the student should also appear registered in Master semestre 3. Last but not the least, don't forget to check if the student has an entry also in the Projet Master tables. Once you can handle well this data, compute the "average stay at EPFL" for master students. Now extract all the students with a Spécialisation and compute the "average stay" per each category of that attribute -- compared to the general average, can you find any specialization for which the difference in average is statistically significant?

# In[45]:

# Requests : make http requests to websites
import requests
# BeautifulSoup : parser to manipulate easily html content
from bs4 import BeautifulSoup
# Regular expressions
import re
# Aren't pandas awesome ?
import pandas as pd


# Let's get the first page in which we will be able to extract some interesting content !

# In[3]:

# Ask for the first page on IS Academia. To see it, just type it on your browser address bar : http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247
r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlContent = BeautifulSoup(r.content, 'html.parser')


# In[4]:

print(htmlContent.prettify())


# Now we need to make other requests to IS Academia, which specify every parameter : computer science students, all the years, and all bachelor semester (which are a couple of two values : pedagogic period and semester type). Thus, we're going to get all the parameters we need to make the next request :

# In[5]:

# We first get the "Computer science" value
computerScienceField = htmlContent.find('option', text='Informatique')
computerScienceField


# In[13]:

computerScienceValue = computerScienceField.get('value')
computerScienceValue


# In[101]:

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


# In[104]:

# Now, we have all the academic years that might interest us
academicYear_Series = pd.Series(academicYearContent, index=academicYearValues)
academicYear_Series


# In[90]:

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


# In[91]:

# Let's make the values and content meet each other
pedagogicPeriod_Series = pd.Series(pedagogicPeriodContent, index=pedagogicPeriodValues)
pedagogicPeriod_Series


# In[96]:

# We keep all semesters related to master students
masterPedagogicPeriod_Series = pedagogicPeriod_Series[[name.startswith('Master') or name.startswith('Projet Master') or name.startswith('Mineur') for name in pedagogicPeriod_Series]]
masterPedagogicPeriod_Series


# In[106]:

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


# In[108]:

# Here are the values for autumn and spring semester :
semesterType_Series = pd.Series(semesterTypeContent, index=semesterTypeValues)
semesterType_Series

