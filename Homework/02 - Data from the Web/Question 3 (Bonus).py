
# coding: utf-8

# BONUS: perform the gender-based study also on the Master students, as explained in 1. Use scatterplots to visually identify changes over time. Plot males and females with different colors -- can you spot different trends that match the results of your statistical tests?

# In[1]:

# Requests : make http requests to websites
import requests
# BeautifulSoup : parser to manipulate easily html content
from bs4 import BeautifulSoup
# Regular expressions
import re


# In[2]:

# Ask for the first page on IS Academia. To see it, just type it on your browser address bar : http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247
r = requests.get('http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_i_reportModel=133685247')
htmlContent = BeautifulSoup(r.content, 'html.parser')


# In[3]:

print(htmlContent.prettify())


# In[4]:

# We first get the "Computer science" value
computerScienceField = htmlContent.find('option', text='Informatique')
computerScienceField


# In[5]:

computerScienceValue = computerScienceField.get('value')
computerScienceValue


# In[6]:

# Then, we're going to need all the academic years values.
academicYearsField = htmlContent.find('select', attrs={'name':'ww_x_PERIODE_ACAD'})
#academicYearsField = academicYearsField.find('option', text='20')
#academicYearsField = academicYearsField.select("select > option")
academicYearsSet = academicYearsField.findAll('option')
academicYearsSet
#print(academicYearsField.prettify())


# In[7]:

for option in academicYearsSet:
    print(option)


# In[8]:

academicYearsValues = academicYearsField.get('value')
academicYearsValues


# In[9]:

academicYearsValues = academicYearsField.find('option')
academicYearsValues


# In[10]:

print(htmlContent.prettify())


# In[ ]:

#Statistical Tests
#Find Students who completed masters
#Assumption: to complete the masters, we consider students with an Entry on Semester 1 and on Masters Project
#use if statement to find students who posses both




# In[ ]:

#Calculate time at EPFL 
#Formula: time at EPFL (time of Semester 1 - Time of Masters Project)
#Add a column of time at EPFL 
[m,n] = DataSet.shape;
for i in (0,m):
    DataSet[i,ExtraColumn]=DataSet[i,M1]-DataSet[i,MP];
    
    


# In[ ]:

#Calculate Overall Average by Gender
Fem = 0; #initialize count for female/male entries
Male = 0;
TotFem = 0; #initialize sum of total time spent at EPFL
TotMale = 0;
for i in (0,m):
    if DataSet[i,GenderColumn] == 'Female':
        Fem = Fem + 1;
        TotFem = TotFem + DataSet[i,ExtraColumn];
        elif DataSet[i,GenderColumn] == 'Male'
        Male = Male + 1;
        TotMale = TotMale + DataSet[i,ExtraColumn];
    
MaleAvg = TotMale/Male;
FemAvg = TotFem/Fem;
Avgs = [MaleAvg FemAvg];
return Avgs


# In[ ]:

# determine statistical significance using t-test 
from scipy.stats import ttest_ind

Fem = DataSet[DataSet['Gender']=='Female']
Male = DataSet[DataSet['Gender']=='Male']

[p,e] = ttest_ind(Fem['TimeColumn'], Male['TimeColumn'])
if p<=0.05:
    print "The difference in averages is statistically significance to a siginificance level of 95%"
    else
        print "The difference in averages is not statistically significance to a significance level of 95%"



# In[ ]:

#Find the evolution of averages by gender
#Calculate the average stay at EPFL for people arriving at different years
FemArray = []; #initialize arrays to store average by starting year
MaleArray = [];
for i in (2007,2014):
    YearAvg = DataSet[DataSet['Semester1']==i];
    Fem2 = YearAvg[YearAvg['Gender']=='Female'];
    Male2 = YearAvg[YearAvg['Gender']=='Male'];
    MeanFem = mean(Fem2[:,TimeColumn]);
    MeanMale = mean(Male2[:,TimeColumn]);
    FemArray.extend(MeanFem);
    MaleArray.extend(MeanMale);
    



        
    


# In[ ]:

#create scatter plot of evolution with different colors by gender

import matplotlib.pyplot as plt

x = [2007:2014]; # set x axis array of starting dates
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(x, FemArray, c='r', label='Female')
ax1.scatter(x, MaleArray, c='b', label='Male')
plt.legend(loc='upper left');
plt.show()



