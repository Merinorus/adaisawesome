
# coding: utf-8

# # I. Setting up the Problem

# In[83]:

import pandas as pd
import numpy as np
from IPython.display import Image
import matplotlib.pyplot as plt

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# In[84]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[85]:

Data.ix[:10,:13]


# In[86]:

Data.ix[:10,13:28]


# # II. Preparing data

# ### 1) Keep only players that have a Rater Image

# In[87]:

# Remove the players without rater 1 / 2 (ie: without photo) because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]


# ### 2) Getting rif of referees and grouping data by soccer player

# We need to aggregate the information about referees and group the result by soccer player. It means that each line will correspond to a soccer player, with the sum of all the cards he got, and we won't know anymore who gaves the cards.

# In[88]:

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

# In[89]:

# Input
x = Data_aggregated
x = x.drop(['playerShort'], 1)

# We have to convert every columns to floats, to be able to train our model
mapping = {'Center Back': 1, 'Attacking Midfielder': 2, 'Right Midfielder': 3, 'Center Midfielder': 4, 'Defensive Midfielder': 5, 'Goalkeeper':6, 'Left Fullback':7, 'Left Midfielder':8, 'Right Fullback':9, 'Center Forward':10, 'Left Winger':11, 'Right Winger':12}
x = x.replace({'position': mapping})
x


# In[90]:

# Output with the same length as the input, that will contains the associated cluster
y = pd.DataFrame(index=x.index, columns=['targetCluster'])
y.head()


# In[91]:

# Create a colormap for target clusters (only 2)
colormap = np.array(['red', 'lime'])

# K Means Cluster
model = KMeans(n_clusters=2)
model = model.fit(x)
model


# In[92]:

# We got a model with two clusters
model.labels_


# In[93]:

# View the results
# Set the size of the plot
plt.figure(figsize=(14,7))
 
# Create a colormap for the two clusters
colormap = np.array(['red', 'lime'])
 
# Plot the Model Classification PARTIALLY
plt.scatter((0.5*x.yellowCards + x.yellowReds + x.redCards)/x.games, x.skinColor, c=colormap[model.labels_], s=40)
plt.xlabel('Red cards per game (yellow = half a red card)')
plt.ylabel('Skin color')
plt.title('K Mean Classification')
plt.show()


# (We show only skin color and number of "red cards" because it's a 2D plot, but we actually used 5 parameters: position, yellowCards, yellowReds, redCards and number of games. So this graph doesn't really represent how our data has been clustered.
# This is only to check if some clustering has ben done. Here we don't really see two distincts clusters. It looks like more random coloring ! :x

# Now, let's add the result to each player:

# In[94]:

cluster = pd.DataFrame(pd.Series(model.labels_, name='cluster'))
Data_Clustered = Data_aggregated
Data_Clustered['cluster'] = cluster
Data_Clustered


# So, do we have any new information ? What can we conclude of this ?
# We can use the "silhouette score", which is a metric showing if the two clusters are well separated. It it's equals to 1, the clusters are perfectly separated, and if it's 0, the clustering doesn't make any sense.

# In[96]:

#score = silhouette_score(x.as_matrix, model.labels_, metric="euclidean")
score = silhouette_score(x, model.labels_)
score


# We got a silhouette score of 58%, which is honestly not really meaningful. We cannot rely on this model.
