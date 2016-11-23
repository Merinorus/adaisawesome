
# coding: utf-8

# # I. Setting up the Problem

# In[50]:

import pandas as pd
import numpy as np
from IPython.display import Image

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[51]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[52]:

Data.ix[:10,:13]


# In[53]:

Data.ix[:10,13:28]


# # II. Preparing data

# ### 1) Keep only players that have a Rater Image

# In[54]:

# Remove the players without rater 1 / 2 (ie: without photo) because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]


# ### 2) Getting rif of referees and grouping data by soccer player

# We need to aggregate the information about referees and group the result by soccer player. It means that each line will correspond to a soccer player, with the sum of all the cards he got, and we won't know anymore who gaves the cards.

# In[55]:

# Group by player and do the sum of every column, except for mean_rater (skin color) that we need to move away during the calculation (we don't want to sum skin color values !)
Data_aggregated = Data_hasImage.drop(['refNum', 'refCountry'], 1)
Data_aggregated = Data_aggregated.groupby(['playerShort', 'position'])['games','yellowCards', 'yellowReds', 'redCards'].sum()
Data_aggregated = Data_aggregated.reset_index()

# Take information of skin color for each player
Data_nbGames_skinColor = Data_hasImage
Data_nbGames_skinColor.drop_duplicates('playerShort')
Data_nbGames_skinColor['skinColor']=(Data_nbGames_skinColor['rater1']+Data_hasImage['rater2'])/2
Data_nbGames_skinColor = pd.DataFrame(Data_nbGames_skinColor[['playerShort','skinColor']])
Data_aggregated = pd.merge(left=Data_aggregated,right=Data_nbGames_skinColor, how='left', left_on='playerShort', right_on='playerShort')
Data_aggregated = Data_aggregated.drop_duplicates('playerShort')
Data_aggregated = Data_aggregated.reset_index(drop=True)
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
# We try to use a K means clustering methode to obtain 2 distinct clusters, with the help of this website:
# http://stamfordresearch.com/k-means-clustering-in-python/

# In[77]:

# Input
x = Data_aggregated
x = x.drop(['playerShort'], 1)

# We have to convert every columns to floats, to be able to train our model
mapping = {'Center Back': 1, 'Attacking Midfielder': 2, 'Right Midfielder': 3, 'Center Midfielder': 4, 'Defensive Midfielder': 5, 'Goalkeeper':6, 'Left Fullback':7, 'Left Midfielder':8, 'Right Fullback':9, 'Center Forward':10, 'Left Winger':11, 'Right Winger':12}
x = x.replace({'position': mapping})
x


# In[68]:

# Output with the same length as the input, that will contains the associated cluster
y = pd.DataFrame(index=x.index, columns=['targetCluster'])
y.head()


# In[78]:

# Create a colormap for target clusters (only 2)
colormap = np.array(['red', 'lime'])

# K Means Cluster
model = KMeans(n_clusters=2)
model.fit(x)


# In[79]:

# We got a model with two clusters
model.labels_

