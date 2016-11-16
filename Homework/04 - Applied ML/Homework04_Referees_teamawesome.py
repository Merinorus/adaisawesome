
# coding: utf-8

# # I. Setting up the Problem

# In[1]:

import pandas as pd
import numpy as np

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[15]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[16]:

Data.ix[:10,:13]


# In[58]:

Data.ix[:10,13:28]


# # II. Preparing the training & test data

# ### 1) Only use players that have a Rater Image

# In[38]:

# 1) Remove the players without rater 1 / 2 rating because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]
#Data_hasImage.ix[:10,13:28]


# ### 2) Disaggregate the data so each row is 1 game

# In[57]:

#for i in Data.iterrows():
#    if Data.at[i, 'games'] > 1:
#        df = Data[i]


# In[65]:

# Testing - divide # cards (all types) by # games column
Data_hasImage['fractionYellow'] = Data_hasImage['yellowCards']/Data_hasImage['games']
Data_hasImage['fractionYellowRed'] = Data_hasImage['yellowReds']/Data_hasImage['games']
Data_hasImage['fractionRed'] = Data_hasImage['redCards']/Data_hasImage['games']

# Get the average of the raters
Data_hasImage['raterAvg'] = (Data_hasImage['rater1']+Data_hasImage['rater2'])/2

#Data_hasImage.head()


# ### 3) Create the Training and Testing Datframes with only select data

# In[96]:

# Removing columns that we do not need
Data_Simple1 = Data_hasImage[['games', 'fractionYellow', 'fractionYellowRed', 'fractionRed',
                              'refNum', 'refCountry', 'raterAvg']]

#cols = ['playerShort', 'games', 'fractionYellow', 'fractionYellowRed', 'fractionRed',
cols = ['games', 'fractionYellow', 'fractionYellowRed', 'fractionRed', 'refNum', 'refCountry']
colsRes = ['raterAvg']

# Take a random 80% sample of the Data for the Training Sample
Data_Training = Data_Simple1.sample(frac=0.8)

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
Input_Data_Training = Data_Training.drop(colsRes, axis=1)
#Results_Data_Training = list(Data_Training.raterAvg.values)
Results_Data_Training = Data_Training[colsRes]


# In[90]:

# Take a random 20% sample of the Data for the Testing Sample
#Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
#Input_Data_Testing = Data_Testing.drop(colsRes, axis=1)
#Results_Data_Testing = list(Data_Testing.raterAvg.values)


# In[97]:

# Need to make arrays
# http://www.analyticbridge.com/profiles/blogs/random-forest-in-python

trainArr = Input_Data_Training.as_matrix(cols) #training array
trainRes = Results_Data_Training.as_matrix(colsRes) #training results


# # III. Random Forest

# In[99]:

#Initialize
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest.fit(trainArr,trainRes)

# Take the same decision trees and run it on the test data
#testArr = test.as_matrix(cols)
#results = rf.predict(testArr)

#test['predictions'] = results
#test.head()


# In[ ]:



