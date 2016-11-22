
# coding: utf-8

# # I. Setting up the Problem

# In[55]:

import pandas as pd
import numpy as np

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[56]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[57]:

Data.ix[:10,:13]


# In[58]:

#Data.ix[:10,13:28]


# # II. Preparing data

# ### 1) Keep only players that have a Rater Image

# In[59]:

# 1) Remove the players without rater 1 / 2 rating because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]
#Data_hasImage.ix[:10,13:28]


# ### 2) Getting rif of referees and grouping data by soccer player

# We need to aggregate the information about referees and group the result by soccer player. It means that each line will correspond to a soccer player, with the sum of all the cards he got, and we won't know anymore who gaves the cards.

# In[60]:

# Group by player and do the sum of every column, except for mean_rater (skin color) that we need to move away during the calculation (we don't want to sum skin color values !)
Data_aggregated = Data_hasImage.drop(['refNum', 'refCountry'], 1)
Data_aggregated = Data_aggregated.groupby(['playerShort', 'position'])['games','yellowCards', 'yellowReds', 'redCards'].sum()
Data_aggregated = Data_aggregated.reset_index()

# Take information of skin color for each player
Data_nbGames_skinColor = pd.DataFrame(Data_nbGames_skinColor[['playerShort','mean_rater']])
Data_aggregated = pd.merge(left=Data_aggregated,right=Data_nbGames_skinColor, how='left', left_on='playerShort', right_on='playerShort')
Data_aggregated


# In[ ]:




# # III. Random Forest

# In[110]:

#Initialize
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest.fit(trainArr,trainRes)

# Take the same decision trees and run it on the test data
#testArr = test.as_matrix(cols)
#results = rf.predict(testArr)

#test['predictions'] = results
#test.head()

