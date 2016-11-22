
# coding: utf-8

# # I. Setting up the Problem

# In[62]:

import pandas as pd
import numpy as np
from IPython.display import Image

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[48]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[49]:

Data.ix[:10,:13]


# In[61]:

Data.ix[:10,13:28]


# # II. Preparing data

# ### 1) Keep only players that have a Rater Image

# In[51]:

# Remove the players without rater 1 / 2 (ie: without photo) because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]


# ### 2) Getting rif of referees and grouping data by soccer player

# We need to aggregate the information about referees and group the result by soccer player. It means that each line will correspond to a soccer player, with the sum of all the cards he got, and we won't know anymore who gaves the cards.

# In[54]:

# Group by player and do the sum of every column, except for mean_rater (skin color) that we need to move away during the calculation (we don't want to sum skin color values !)
Data_aggregated = Data_hasImage.drop(['refNum', 'refCountry'], 1)
Data_aggregated = Data_aggregated.groupby(['playerShort', 'position'])['games','yellowCards', 'yellowReds', 'redCards'].sum()
Data_aggregated = Data_aggregated.reset_index()

# Take information of skin color for each player
Data_nbGames_skinColor = pd.DataFrame(Data_nbGames_skinColor[['playerShort','mean_rater']])
Data_aggregated = pd.merge(left=Data_aggregated,right=Data_nbGames_skinColor, how='left', left_on='playerShort', right_on='playerShort')
Data_aggregated


# In[ ]:




# # III. Unsupervized machine learning

# The first idea we got is to start an unsupervized learning kept as simple as possible.
# 
# We will have to take player position, the three types of cards and the skin color: that makes 5 dimensions to deal with !
# 
# Instead, let say we only look at the total number of cards the players got, and their skin color. Then we would be able to display something in 2 dimensions only:

# <img src="resources/axis_assumption.jpg" alt="Drawing" style="width: 600px;"/>

# Then, we would try to obtain two clusters that might lead to really simple conclusion such as "dark people slightly tend to get more cards":

# <img src="resources/axis_assumption_clustered.jpg" alt="Drawing" style="width: 600px;"/>

# Again, this is totally hypothetical. So let's give it a try.
