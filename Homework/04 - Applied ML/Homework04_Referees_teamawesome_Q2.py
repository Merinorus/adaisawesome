
# coding: utf-8

# # I. Setting up the Problem

# In[111]:

import pandas as pd
import numpy as np
from IPython.display import Image
import matplotlib.pyplot as plt

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# In[112]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[113]:

Data.ix[:10,:13]


# In[114]:

Data.ix[:10,13:28]


# # II. Preparing data

# ### 1) Keep only players that have a Rater Image

# In[115]:

# Remove the players without rater 1 / 2 (ie: without photo) because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]


# ### 2) Getting rif of referees and grouping data by soccer player

# We need to aggregate the information about referees and group the result by soccer player. It means that each line will correspond to a soccer player, with the sum of all the cards he got, and we won't know anymore who gaves the cards.

# In[116]:

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

# In[117]:

# Input
x = Data_aggregated
x = x.drop(['playerShort'], 1)

# We have to convert every columns to floats, to be able to train our model
mapping = {'Center Back': 1, 'Attacking Midfielder': 2, 'Right Midfielder': 3, 'Center Midfielder': 4, 'Defensive Midfielder': 5, 'Goalkeeper':6, 'Left Fullback':7, 'Left Midfielder':8, 'Right Fullback':9, 'Center Forward':10, 'Left Winger':11, 'Right Winger':12}
x = x.replace({'position': mapping})
x


# In[118]:

# Output with the same length as the input, that will contains the associated cluster
y = pd.DataFrame(index=x.index, columns=['targetCluster'])
y.head()


# In[119]:

# K Means Cluster
model = KMeans(n_clusters=2)
model = model.fit(x)
model


# In[120]:

# We got a model with two clusters
model.labels_


# In[121]:

# View the results
# Set the size of the plot
plt.figure(figsize=(14,7))
 
# Create a colormap for the two clusters
colormap = np.array(['blue', 'lime'])
 
# Plot the Model Classification PARTIALLY
plt.scatter((0.5*x.yellowCards + x.yellowReds + x.redCards)/x.games, x.skinColor, c=colormap[model.labels_], s=40)
plt.xlabel('Red cards per game (yellow = half a red card)')
plt.ylabel('Skin color')
plt.title('K Mean Classification')
plt.show()


# (We show only skin color and number of "red cards" because it's a 2D plot, but we actually used 5 parameters: position, yellowCards, yellowReds, redCards and number of games. So this graph doesn't really represent how our data has been clustered.
# This is only to check if some clustering has ben done. Here we don't really see two distincts clusters. It looks like more random coloring ! :x

# Now, let's add the result to each player:

# In[122]:

cluster = pd.DataFrame(pd.Series(model.labels_, name='cluster'))
Data_Clustered = Data_aggregated
Data_Clustered['cluster'] = cluster
Data_Clustered


# So, do we have any new information ? What can we conclude of this ?
# We can use the "silhouette score", which is a metric showing if the two clusters are well separated. It it's equals to 1, the clusters are perfectly separated, and if it's 0, the clustering doesn't make any sense.

# In[131]:

score = silhouette_score(x, model.labels_)
score


# We got a silhouette score of 58%, which is honestly not enough to predict precisely the skin color of new players. A value closer to +1 would have indicated with higher confidence a difference between the clusters. 60% is enough to distinguish the two clusters but, still, we cannot rely on this model.
# Let's try to remove features iterately, starting with skin color.

# In[130]:

x_noSkinColor = x.drop(['skinColor'], 1)
model = KMeans(n_clusters=2)
model = model.fit(x_noSkinColor)
score_noSkinColor = silhouette_score(x_noSkinColor, model.labels_)
score_noSkinColor


# In[134]:

score_noSkinColor / score


# Seems like removing skin color from the input didn't change anything for the clustering performance !
# Let's do this with removing another parameter: position.

# In[142]:

x_noPosition = x.drop(['position'], 1)
model = KMeans(n_clusters=2)
model = model.fit(x_noPosition)
score_noPosition= silhouette_score(x_noPosition, model.labels_)
score_noPosition


# In[143]:

score_noPosition / score


# Player position doesn't have much impact either. We can try to remove the number of games, but it won't make sense: some player will have an absolute higher number of cards, only because they played a lot more games. But we will lost this information.

# In[144]:

x_noGameNumber = x.drop(['games'], 1)
model = KMeans(n_clusters=2)
model = model.fit(x_noGameNumber)
score_noGameNumber = silhouette_score(x_noGameNumber, model.labels_)
score_noGameNumber


# In[145]:

score_noGameNumber / score


# Well, that makes a 2% improvement, but the information is biased ! This model doesn't show anything helpful.
# Whatever feature we remove, we don't get a good prediction with unsupervized learning. It doesn't mean that there is absolutely zero correlation between the skin color and the number of cards a players can get. But we're not able to predict correctly the skin color of a player, according to the different features we studied previously.
