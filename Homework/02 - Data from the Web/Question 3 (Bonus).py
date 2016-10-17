
# coding: utf-8

# BONUS: perform the gender-based study also on the Master students, as explained in 1. Use scatterplots to visually identify changes over time. Plot males and females with different colors -- can you spot different trends that match the results of your statistical tests?

# In[ ]:

#use hypothetical data set generated in Question 2
# we were not able to generate the DataSet and therefore were not able to test this code
#this is our attemp at demonstrating the algorithim that we'd use to compute stats for part 3


# In[ ]:

#Statistical Tests for Question 3 (Bonus)
#Find Students who completed masters
#Assumption: to complete the masters, we consider students with an Entry on Semester 1 and on Masters Project
#use if statement to find students who posses both




# In[ ]:

#Calculate time at EPFL 
#Formula: time at EPFL (time of Semester 1 - Time of Masters Project)
#Add a column of time at EPFL 
[m,n] = DataSet.shape;
for i in (0,m):
    DataSet.TimeSpent[i]=DataSet.StartDate[i]-DataSet.EndDate[i]; #assume we were able to create a column with the end date and start date of each student
    
    


# In[ ]:

#Calculate Overall Average by Gender
Fem = 0; #initialize count for female/male entries
Male = 0;
TotFem = 0; #initialize sum of total time spent at EPFL
TotMale = 0;
for i in (0,m):
    if DataSet[i,1] == 'Madame':
        Fem = Fem + 1;
        TotFem = TotFem + DataSet.TimeSpent[i];
        elif DataSet[i,1] == 'Monsieur'
        Male = Male + 1;
        TotMale = TotMale + DataSet.TimeSpent[i];
    
MaleAvg = TotMale/Male;
FemAvg = TotFem/Fem;
Avgs = [MaleAvg FemAvg];
return Avgs


# In[ ]:

# determine statistical significance using t-test 
from scipy.stats import ttest_ind

Fem = DataSet[DataSet['Civilité']=='Madame']
Male = DataSet[DataSet['Civilité']=='Monsieur']

[p,e] = ttest_ind(Fem['TimeSpent'], Male['TimeSpent'])
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
    YearAvg = DataSet[DataSet['StartDate']==i];
    Fem2 = YearAvg[YearAvg['Civilité']=='Madame'];
    Male2 = YearAvg[YearAvg['Civilité']=='Monsieur'];
    MeanFem = mean(Fem2.TimeSpent);
    MeanMale = mean(Male2.TimeSpent);
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



