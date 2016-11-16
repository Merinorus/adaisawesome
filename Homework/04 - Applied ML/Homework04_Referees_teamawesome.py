
# coding: utf-8

# # I. Setting up the Problem

# In[2]:

import pandas as pd
import numpy as np

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[3]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[4]:

Data.ix[:10,:13]


# In[5]:

#Data.ix[:10,13:28]


# # II. Preparing the training & test data

# ### 1) Only use players that have a Rater Image

# In[6]:

# 1) Remove the players without rater 1 / 2 rating because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]
#Data_hasImage.ix[:10,13:28]


# 

# In[ ]:




# ### 2) Disaggregate the data so each row is 1 game

# Got a lot of help from this script ! https://osf.io/w7tds/
# It will be much simpler for us to train our random forest if each row corresponds to one game. This way, we won't have to give a different "weight" to each row according to the number of played games.

# But let's start by doing the mean value of rater1 and rater 2, because if we keep them separated we might get some strange results.
# Indeed, what if for a player, rater1 = 0.0 and rater2 = 0.75 ?
# It would not make a lot of sense, or at least we would know our model is not viable !

# In[16]:

Data_hasImage['mean_rater']=(Data_hasImage['rater1']+Data_hasImage['rater2'])/2


# Let's now disaggregate the games:

# In[ ]:




# ### 3) Create the Training and Testing Datframes with only select data

# In[47]:

# Removing columns that we do not need
Data_Simple1 = Data_hasImage[['playerShort', 'games', 'yellowCards', 'yellowReds', 'redCards',
                              'refNum', 'refCountry', 'rater1', 'rater2']]

# Take a random 80% sample of the Data for the Training Sample
Data_Training = Data_Simple1.sample(frac=0.8)

# Take a random 20% sample of the Data for the Testing Sample
Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]


# In[ ]:

# TO DO Need to make arrays
# http://www.analyticbridge.com/profiles/blogs/random-forest-in-python


# # III. Random Forest

# In[42]:

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(Data_Simple2[0::,1::],Data_Simple2[0::,0])

# Take the same decision trees and run it on the test data
output = forest.predict(Data_Simple2)


# In[ ]:



