
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


# In[80]:

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
# We'll put the textual content in a table aswell ("Bachelor semestre 1", "Bachelor semestre 2"...)
academicYearContent = []

for option in academicYearsSet:
    value = option.get('value')
    # However, we don't want any "null" value
    if value != 'null':
        academicYearValues.append(value)
        academicYearContent.append(option.text)


# In[81]:

# Now, we have all the academic years that might interest us. We wrangle them a little bit so be able to make request more easily later.
academicYearValues_series = pd.Series(academicYearValues)
academicYearContent_series = pd.Series(academicYearContent)
academicYear_df = pd.concat([academicYearContent_series, academicYearValues_series], axis = 1)
academicYear_df.columns= ['Academic_year', 'Value']
academicYear_df = academicYear_df.sort_values(['Academic_year', 'Value'], ascending=[1, 0])
academicYear_df


# In[82]:

# Then, let's get all the pedagogic periods we need. It's a little bit more complicated here because we need to link the pedagogic period with a season (eg : Bachelor 1 is autumn, Bachelor 2 is spring etc.)
# Thus, we need more than the pedagogic values. For doing some tests to associate them with the right season, we need the actual textual value ("Bachelor semestre 1", "Bachelor semestre 2" etc.)
pedagogicPeriodsField = htmlContent.find('select', attrs={'name':'ww_x_PERIODE_PEDAGO'})
pedagogicPeriodsSet = pedagogicPeriodsField.findAll('option')

# Same as above, we'll store the values in a table
pedagogicPeriodValues = []
# We'll put the textual content in a table aswell ("Bachelor semestre 1", "Bachelor semestre 2"...)
pedagogicPeriodContent = []

for option in pedagogicPeriodsSet:
    value = option.get('value')
    if value != 'null':
        pedagogicPeriodValues.append(value)
        pedagogicPeriodContent.append(option.text)


# In[83]:

# Let's make the values and content meet each other
pedagogicPeriodContent_series = pd.Series(pedagogicPeriodContent)
pedagogicPeriodValues_series = pd.Series(pedagogicPeriodValues)
pedagogicPeriod_df = pd.concat([pedagogicPeriodContent_series, pedagogicPeriodValues_series], axis = 1);
pedagogicPeriod_df.columns = ['Pedagogic_period', 'Value']


# In[84]:

# We keep all semesters related to Bachelor students
pedagogicPeriod_df_bachelor = pedagogicPeriod_df[[period.startswith('Bachelor') for period in pedagogicPeriod_df.Pedagogic_period]]

pedagogicPeriod_df = pd.concat([pedagogicPeriod_df_bachelor])
pedagogicPeriod_df


# In[85]:

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


# In[86]:

# Here are the values for autumn and spring semester :

semesterTypeValues_series = pd.Series(semesterTypeValues)
semesterTypeContent_series = pd.Series(semesterTypeContent)
semesterType_df = pd.concat([semesterTypeContent_series, semesterTypeValues_series], axis = 1)
semesterType_df.columns = ['Semester_type', 'Value']
semesterType_df

Now, we got all the information to get all the bachelor students ! Let's make all the requests we need to build our data. We will try to do requests such as :
Get students from bachelor semester 1 of 2007-2008
...
Get students from bachelor semester 6b of 2007-2008
... and so on for each academic year until 2015-2016, the last complete year. We can even take the first semester of 2016-2017 into account, to check if some students we though they finished last year are actually still studying. 
# We can ask for a list of student in two formats : HTML or CSV. We choosed to get them in a HTML format because this is the first time that we wrangle data in HTML format, and that may be really useful to learn in order to work with most of the websites in the future ! The request sent by the browser to IS Academia, to get a list of student in a HTML format, looks like this : http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?arg1=xxx&arg2=yyy With "xxx" the value associated with the argument named "arg1", "yyy" the value associated with the argument named "arg2" etc. It uses to have a lot more arguments. For instance, we tried to send a request as a "human" through our browser and intercepted it with Postman interceptor. We found that the folowing arguments have to be sent : ww_x_GPS = -1 ww_i_reportModel = 133685247 ww_i_reportModelXsl = 133685270 ww_x_UNITE_ACAD = 249847 (which is the value of computer science !) ww_x_PERIODE_ACAD = X (eg : the value corresponding to 2007-2008 would be 978181) ww_x_PERIODE_PEDAGO = Y (eg : 2230106 for Bachelor semestre 1) ww_x_HIVERETE = Z (eg : 2936286 for autumn semester)
# The last three values X, Y and Z must be replaced with the ones we extracted previously. For instance, if we want to get students from Bachelor, semester 1 (which is necessarily autumn semester) of 2007-2008, the "GET Request" would be the following :
# http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?ww_x_GPS=-1&ww_i_reportModel=133685247&ww_i_reportModelXsl=133685270&ww_x_UNITE_ACAD=249847&ww_x_PERIODE_ACAD=978181&ww_x_PERIODE_PEDAGO=2230106&ww_x_HIVERETE=2936286
# So let's cook all the requests we're going to send !

# In[87]:

# Let's put the semester types aside, because we're going to need them
autumn_semester_value = semesterType_df.loc[semesterType_df['Semester_type'] == 'Semestre d\'automne', 'Value']
autumn_semester_value = autumn_semester_value.iloc[0]

spring_semester_value = semesterType_df.loc[semesterType_df['Semester_type'] == 'Semestre de printemps', 'Value']
spring_semester_value = spring_semester_value.iloc[0]


# In[90]:

# Here is the list of the GET requests we will send to IS Academia
requestsToISAcademia = []

# Go all over the years ('2007-2008', '2008-2009' and so on)
for academicYear_row in academicYear_df.itertuples(index=True, name='Academic_year'):
    
    # The year (eg: '2007-2008')
    academicYear = academicYear_row.Academic_year
    
    # The associated value (eg: '978181')
    academicYear_value = academicYear_row.Value
    
    # We get all the pedagogic periods associated with this academic year
    for pegagogicPeriod_row in pedagogicPeriod_df.itertuples(index=True, name='Pedagogic_period'):
        
        # The period (eg: 'Bachelor semestre 1')
        pedagogicPeriod = pegagogicPeriod_row.Pedagogic_period
        
        # The associated value (eg: '2230106')
        pegagogicPeriod_Value = pegagogicPeriod_row.Value
        
        # We need to associate the corresponding semester type (eg: Bachelor semester 1 is autumn, but Bachelor semester 2 will be spring)
        if (pedagogicPeriod.endswith('1') or pedagogicPeriod.endswith('3') or pedagogicPeriod.endswith('automne')):
            semester_Value = autumn_semester_value
        else:
            semester_Value = spring_semester_value
        
        # This print line is only for debugging if you want to check something
        # print("academic year = " + academicYear_value + ", pedagogic value = " + pegagogicPeriod_Value + ", pedagogic period is " + pedagogicPeriod + " (semester type value = " + semester_Value + ")")
        
        # We're ready to cook the request !
        request = 'http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?ww_x_GPS=-1&ww_i_reportModel=133685247&ww_i_reportModelXsl=133685270&ww_x_UNITE_ACAD=' + computerScienceValue
        request = request + '&ww_x_PERIODE_ACAD=' + academicYear_value
        request = request + '&ww_x_PERIODE_PEDAGO=' + pegagogicPeriod_Value
        request = request + '&ww_x_HIVERETE=' + semester_Value
        
        # Add the newly created request to our wish list...
        requestsToISAcademia.append(request)


# In[91]:

# Here is the list of all the requests we have to send !
requestsToISAcademia


# In[94]:

# Create a new Dataframe into which to concatenate all of the students and Scipers
data1 = requests.get(requestsToISAcademia[0])
htmlContentData1 = BeautifulSoup(data1.content, 'html.parser')
print(htmlContentData1.prettify())


# In[104]:

# Create an empty dataframe with the relevant columns
df1 = pd.DataFrame({'Civilité': [], 'Nom Prénom':[], 'Status':[], 'No Sciper':[]})
df1['Civilité';1] = htmlContentData1.find('select', attrs={'name':'Civilité'})
df1


# In[ ]:



