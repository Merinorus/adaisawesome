
# coding: utf-8

# Obtain all the data for the Master students, starting from 2007. Compute how many months it took each master student to complete their master, for those that completed it. Partition the data between male and female students, and compute the average -- is the difference in average statistically significant?
# 
# Notice that master students' data is more tricky than the bachelors' one, as there are many missing records in the IS-Academia database. Therefore, try to guess how much time a master student spent at EPFL by at least checking the distance in months between Master semestre 1 and Master semestre 2. If the Mineur field is not empty, the student should also appear registered in Master semestre 3. Last but not the least, don't forget to check if the student has an entry also in the Projet Master tables. Once you can handle well this data, compute the "average stay at EPFL" for master students. Now extract all the students with a Spécialisation and compute the "average stay" per each category of that attribute -- compared to the general average, can you find any specialization for which the difference in average is statistically significant?

# In[118]:

# Requests : make http requests to websites
import requests
# BeautifulSoup : parser to manipulate easily html content
from bs4 import BeautifulSoup
# Regular expressions
import re
# Aren't pandas awesome ?
import pandas as pd


# Let's get the first page in which we will be able to extract some interesting content !

# In[119]:

# Ask for the first page on IS Academia. To see it, just type it on your browser address bar : http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247
r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlContent = BeautifulSoup(r.content, 'html.parser')


# In[120]:

print(htmlContent.prettify())


# Now we need to make other requests to IS Academia, which specify every parameter : computer science students, all the years, and all bachelor semester (which are a couple of two values : pedagogic period and semester type). Thus, we're going to get all the parameters we need to make the next request :

# In[121]:

# We first get the "Computer science" value
computerScienceField = htmlContent.find('option', text='Informatique')
computerScienceField


# In[122]:

computerScienceValue = computerScienceField.get('value')
computerScienceValue


# In[123]:

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


# In[181]:

# Now, we have all the academic years that might interest us. We wrangle them a little bit so be able to make request more easily later.
academicYearValues_series = pd.Series(academicYearValues)
academicYearContent_series = pd.Series(academicYearContent)
academicYear_df = pd.concat([academicYearContent_series, academicYearValues_series], axis = 1)
academicYear_df.columns= ['Academic_year', 'Value']
academicYear_df = academicYear_df.sort_values(['Academic_year', 'Value'], ascending=[1, 0])
academicYear_df


# In[125]:

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


# In[213]:

# Let's make the values and content meet each other
pedagogicPeriodContent_series = pd.Series(pedagogicPeriodContent)
pedagogicPeriodValues_series = pd.Series(pedagogicPeriodValues)
pedagogicPeriod_df = pd.concat([pedagogicPeriodContent_series, pedagogicPeriodValues_series], axis = 1);
pedagogicPeriod_df.columns = ['Pedagogic_period', 'Value']


# In[238]:

# We keep all semesters related to master students
pedagogicPeriod_df_master = pedagogicPeriod_df[[period.startswith('Master') for period in pedagogicPeriod_df.Pedagogic_period]]
pedagogicPeriod_df_minor = pedagogicPeriod_df[[period.startswith('Mineur') for period in pedagogicPeriod_df.Pedagogic_period]]
pedagogicPeriod_df_project = pedagogicPeriod_df[[period.startswith('Projet Master') for period in pedagogicPeriod_df.Pedagogic_period]]

pedagogicPeriod_df = pd.concat([pedagogicPeriod_df_master, pedagogicPeriod_df_minor, pedagogicPeriod_df_project])
pedagogicPeriod_df


# In[128]:

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


# In[190]:

# Here are the values for autumn and spring semester :

semesterTypeValues_series = pd.Series(semesterTypeValues)
semesterTypeContent_series = pd.Series(semesterTypeContent)
semesterType_df = pd.concat([semesterTypeContent_series, semesterTypeValues_series], axis = 1)
semesterType_df.columns = ['Semester_type', 'Value']
semesterType_df


# Now, we got all the information to get all the master students !
# Let's make all the requests we need to build our data.
# We will try to do requests such as :
# - Get students from master semester 1 of 2007-2008
# - ...
# - Get students from master semester 4 of 2007-2008
# - Get students from mineur semester 1 of 2007-2008
# - Get students from mineur semester 2 of 2007-2008
# - Get students from master project semester 1 of 2007-2008
# - Get students from master project semester 2 of 2007-2008
# 
# ... and so on for each academic year until 2015-2016, the last complete year.
# We can even take the first semester of 2016-2017 into account, to check if some students we though they finished last year are actually still studying. This can be for different reasons : doing a mineur, a project, repeating a semester...

# We can ask for a list of student in two formats : HTML or CSV.
# We choosed to get them in a HTML format because this is the first time that we wrangle data in HTML format, and that may be really useful to learn in order to work with most of the websites in the future !
# The request sent by the browser to IS Academia, to get a list of student in a HTML format, looks like this :
# http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?arg1=xxx&arg2=yyy
# With "xxx" the value associated with the argument named "arg1", "yyy" the value associated with the argument named "arg2" etc. It uses to have a lot more arguments.
# For instance, we tried to send a request as a "human" through our browser and intercepted it with Postman interceptor.
# We found that the folowing arguments have to be sent :
# ww_x_GPS = -1
# ww_i_reportModel = 133685247
# ww_i_reportModelXsl = 133685270
# ww_x_UNITE_ACAD = 249847 (which is the value of computer science !)
# ww_x_PERIODE_ACAD = X (eg : the value corresponding to 2007-2008 would be 978181)
# ww_x_PERIODE_PEDAGO = Y (eg : 2230106 for Master semestre 1)
# ww_x_HIVERETE = Z (eg : 2936286 for autumn semester)
# 
# The last three values X, Y and Z must be replaced with the ones we extracted previously. For instance, if we want to get students from Master, semester 1 (which is necessarily autumn semester) of 2007-2008, the "GET Request" would be the following :
# 
# http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.html?ww_x_GPS=-1&ww_i_reportModel=133685247&ww_i_reportModelXsl=133685270&ww_x_UNITE_ACAD=249847&ww_x_PERIODE_ACAD=978181&ww_x_PERIODE_PEDAGO=2230106&ww_x_HIVERETE=2936286
# 
# So let's cook all the requests we're going to send !

# In[249]:

# Let's put the semester types aside, because we're going to need them
autumn_semester_value = semesterType_df.loc[semesterType_df['Semester_type'] == 'Semestre d\'automne', 'Value']
autumn_semester_value = autumn_semester_value.iloc[0]

spring_semester_value = semesterType_df.loc[semesterType_df['Semester_type'] == 'Semestre de printemps', 'Value']
spring_semester_value = spring_semester_value.iloc[0]


# In[270]:

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
        
        # The period (eg: 'Master semestre 1')
        pedagogicPeriod = pegagogicPeriod_row.Pedagogic_period
        
        # The associated value (eg: '2230106')
        pegagogicPeriod_Value = pegagogicPeriod_row.Value
        
        # We need to associate the corresponding semester type (eg: Master semester 1 is autumn, but Master semester 2 will be spring)
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
        
        
        


# In[267]:

# Here is the list of all the requests we have to send !
requestsToISAcademia


# The requests are now ready to be sent to IS Academia. Let's try it out !

# In[279]:

# WARNING : NEXT LINE IS COMMENTED FOR DEBGUGGING THE FIRST REQUEST ONLY. UNCOMMENT IT AND INDENT THE CODE CORRECTLY TO MAKE ALL THE REQUESTS

#for request in requestsToISAcademia: # LINE TO UNCOMMENT TO SEND ALL REQUESTS
request = requestsToISAcademia[0] # LINE TO COMMENT TO SEND ALL REQUESTS
print(request)

# Send the request to IS Academia
r = requests.get(request)

# Here is the HTML content of IS Academia's response
htmlContent = BeautifulSoup(r.content, 'html.parser')

# Let's extract some data...
# TODO

