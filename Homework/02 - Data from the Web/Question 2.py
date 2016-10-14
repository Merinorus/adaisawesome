
# coding: utf-8

# Perform a similar operation to what described above, this time for Master students. Notice that this data is more tricky, as there are many missing records in the IS-Academia database. Therefore, try to guess how much time a master student spent at EPFL by at least checking the distance in months between Master semestre 1 and Master semestre 2. If the Mineur field is not empty, the student should also appear registered in Master semestre 3. Last but not the least, don't forget to check if the student has an entry also in the Projet Master tables. Once you can handle well this data, compute the "average stay at EPFL" for master students. Now extract all the students with a Spécialisation and compute the "average stay" per each category of that attribute -- compared to the general average, can you find any specialization for which the difference in average is statistically significant?

# In[77]:

# Requests : make http requests to websites
import requests
# BeautifulSoup : parser to manipulate easily html content
from bs4 import BeautifulSoup
# Regular expressions
import re


# Let's get the first page in which we will be able to extract some interesting content !

# In[22]:

# Ask for the first page on IS Academia. To see it, just type it on your browser address bar : http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247
r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlContent = BeautifulSoup(r.content, 'html.parser')


# In[23]:

print(htmlContent.prettify())


# Now we need to make other requests to IS Academia, which specify every parameter : computer science students, all the years and bachelor semester etc. Thus, we're going to get all the parameters we need to make the next request :

# In[134]:

# We first get the "Computer science" value
computerScienceField = htmlContent.find('option', text='Informatique')
computerScienceField


# In[136]:

computerScienceValue = computerScienceField.get('value')
computerScienceValue


# In[154]:

# Then, we're going to need all the academic years values.
academicYearsField = htmlContent.find('select', attrs={'name':'ww_x_PERIODE_ACAD'})
#academicYearsField = academicYearsField.find('option', text='20')
#academicYearsField = academicYearsField.select("select > option")
academicYearsSet = academicYearsField.findAll('option')
academicYearsSet
#print(academicYearsField.prettify())


# In[155]:

for option in academicYearsSet:
    print(option)


# In[141]:

academicYearsValues = academicYearsField.get('value')
academicYearsValues


# In[138]:

academicYearsValues = academicYearsField.find('option')
academicYearsValues


# In[82]:

print(htmlContent.prettify())

