
# coding: utf-8

# # I. Setting up the Problem

# In[1]:

import pandas as pd
import numpy as np

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[2]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[3]:

Data.ix[:10,:13]


# In[4]:

#Data.ix[:10,13:28]


# # II. Preparing the training & test data : Unique Game Row version

# ### 1) Keep only players that have a Rater Image

# In[4]:

# 1) Remove the players without rater 1 / 2 rating because we won't be 
# able to train or test the values (this can be done as bonus later)

Data_hasImage = Data[pd.notnull(Data['photoID'])]
#Data_hasImage.ix[:10,13:28]


# ### 2) Disaggregate the data so each row is 1 game

# Got a lot of help from this script ! https://osf.io/w7tds/
# It will be much simpler for us to train our random forest if each row corresponds to one game. This way, we won't have to give a different "weight" to each row according to the number of played games.

# But let's start by doing the mean value of rater1 and rater 2, because if we keep them separated we might get some strange results.
# Indeed, what if for a player, rater1 = 0.0 and rater2 = 0.75 ?
# It would not make a lot of sense, or at least we would know our model is not viable !

# In[5]:

Data_hasImage['mean_rater']=(Data_hasImage['rater1']+Data_hasImage['rater2'])/2


# Let's now disaggregate the games:

# In[6]:

game_counter = 0
game_total_number = sum(Data_hasImage['games'])
# Raw table that we'll have to convert to a dataframe later
output = [0 for i in range(game_total_number)]

# We now iterate each row of our dataframe, which may contains more that one game
for i, row in Data_hasImage.iterrows():
    # Number of games in the current row
    row_game_number = row['games']
    # Number of cumulated cards for the games in the current row
    yellowCards = row['yellowCards']
    yellowReds = row['yellowReds']
    redCards = row['redCards']
    # We want to seperate each of these games    
    for j in range (row_game_number):
        game = row
        game['yellowCards'] = 0
        game['yellowReds'] = 0
        game['redCards'] = 0
        # Basically, we distribute the cards we have on separate games.
        # ie: if we have 2 yellowCard and 1 redCard for a total of 4 games,
        # the first two games will be assigned a yellowCard,
        # the third game will be assigned a redCard,
        # and the last game won't have any card assigned, because there is no card left.        
        if yellowCards > 0:
            game['yellowCards'] = 1
            yellowCards = yellowCards - 1
        elif yellowReds > 0:
            game['yellowReds'] = 1
            yellowReds = yellowReds - 1
        elif redCards > 0:
            game['redCards'] = 1
            redCards = redCards - 1
            
        # Convert from pandas Series to prevent overwriting previous values of the output
        gamelist=list(game)
        # Add the new game to the output
        output[game_counter] = gamelist
        game_counter = game_counter + 1

# Here is the output dataframe

Data_OneGamePerRow = pd.DataFrame(output, columns=list(Data_hasImage.columns))
Data_OneGamePerRow


# ### 3) Create the Training and Testing Datframes with only select data

# In[70]:

# Removing columns that we do not need
Data_Simple1 = Data_OneGamePerRow[['playerShort', 'yellowCards', 'yellowReds', 'redCards',
                              'refNum', 'refCountry', 'mean_rater', 'games']]

# Take a random 80% sample of the Data for the Training Sample
#Data_Training = Data_Simple1.sample(frac=0.8)

# Take a random 20% sample of the Data for the Testing Sample
#Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]


# In[71]:

Data_Simple1


# In[73]:

#find proportion of yellow & red cards to games
Data_Simple1['fractionYellow'] = Data_Simple1['yellowCards']/Data_Simple1['games']
Data_Simple1['fractionYellowRed'] = Data_Simple1['yellowReds']/Data_Simple1['games']
Data_Simple1['fractionRed'] = Data_Simple1['redCards']/Data_Simple1['games']
Data_Simple1


# In[74]:

colRate = ['mean_rater']
Col_Rating = Data_Simple1[colRate].values
Ratings_Scale = []; 
Col_Rating


# In[75]:

# Must now convert this continuous scale into a categorical one, with 20 categories
A = len(Col_Rating)
for i in range (0,A):
    if Col_Rating[i] >= 0 and Col_Rating[i] <0.05:
        Ratings_Scale.append(1);
    elif Col_Rating[i] >= 0.05 and Col_Rating[i] <0.1:
        Ratings_Scale.append(2);
    elif Col_Rating[i] >= 0.1 and Col_Rating[i] <0.15:
        Ratings_Scale.append(3);
    elif Col_Rating[i] >= 0.15 and Col_Rating[i] <0.2:
        Ratings_Scale.append(4);
    elif Col_Rating[i] >= 0.2 and Col_Rating[i] <0.25:
        Ratings_Scale.append(5);
    elif Col_Rating[i] >= 0.25 and Col_Rating[i] <0.3:
        Ratings_Scale.append(6);
    elif Col_Rating[i] >= 0.3 and Col_Rating[i] <0.35:
        Ratings_Scale.append(7);
    elif Col_Rating[i] >= 0.35 and Col_Rating[i] <0.4:
        Ratings_Scale.append(8);
    elif Col_Rating[i] >= 0.4 and Col_Rating[i] <0.45:
        Ratings_Scale.append(9);
    elif Col_Rating[i] >= 0.45 and Col_Rating[i] <0.5:
        Ratings_Scale.append(10);
    elif Col_Rating[i] >= 0.5 and Col_Rating[i] <0.55:
        Ratings_Scale.append(11);
    elif Col_Rating[i] >= 0.55 and Col_Rating[i] <0.6:
        Ratings_Scale.append(12);
    elif Col_Rating[i] >= 0.6 and Col_Rating[i] <0.65:
        Ratings_Scale.append(13);
    elif Col_Rating[i] >= 0.65 and Col_Rating[i] <0.7:
        Ratings_Scale.append(14);
    elif Col_Rating[i] >= 0.7 and Col_Rating[i] <0.75:
        Ratings_Scale.append(15);
    elif Col_Rating[i] >= 0.75 and Col_Rating[i] <0.8:
        Ratings_Scale.append(16);
    elif Col_Rating[i] >= 0.8 and Col_Rating[i] <0.85:
        Ratings_Scale.append(17);
    elif Col_Rating[i] >= 0.85 and Col_Rating[i] <0.9:
        Ratings_Scale.append(18);
    elif Col_Rating[i] >= 0.9 and Col_Rating[i] <0.95:
        Ratings_Scale.append(19);
    elif Col_Rating[i] >= 0.95 and Col_Rating[i] <=1:
        Ratings_Scale.append(20);
    else:
        Ratings_Scale.append(99);
        
Data_Simple1['raterScale'] = Ratings_Scale
Data_Simple1.head()

## Some of the values in trainRes_1 are larger than one! We must delete them from the simple data set to avoid errors in the training process.


# In[76]:

# drop values on scale which are equal to 99
Data_Simple2 = Data_Simple1[Data_Simple1.raterScale != 99]
Data_Simple2.dropna(axis=0)
Data_Simple2


# # II. Preparing the training & test data : Fraction version

# ### 1) Create the Training and Testing Datframes with only select data

# In[77]:

#create test and training matrix

cols = ['games', 'fractionYellow', 'fractionYellowRed', 'fractionRed', 'refNum', 'refCountry']
exclude = ['raterScale','mean_rater', 'playerShort', 'yellowCards','yellowReds','redCards', 'games']
colsRes1 = ['raterScale']


# Take a random 80% sample of the Data for the Training Sample
Data_Training = Data_Simple2.sample(frac=0.8)

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
Input_Data_Training = Data_Training.drop(exclude, axis=1)

#Results_Data_Training = list(Data_Training.raterAvg.values)
Results_Data_Training = Data_Training[colsRes1]
Input_Data_Training.head()


# In[14]:

# Take a random 20% sample of the Data for the Testing Sample
#Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
#Input_Data_Testing = Data_Testing.drop(colsRes, axis=1)
#Results_Data_Testing = list(Data_Testing.raterAvg.values)


# In[78]:

# Need to make arrays
# http://www.analyticbridge.com/profiles/blogs/random-forest-in-python
trainArr = Input_Data_Training.as_matrix() #training array
#trainRes = Results_Data_Training.as_matrix(colsRes) #training results
trainRes_1 = Data_Training['raterScale'].values
trainArr


# # III. Random Forest

# In[80]:

#Initialize
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr,trainRes_1)

# Take the same decision trees and run it on the test data
Data_Testing = Data_Simple2.sample(frac=0.2)
Input_Data_Testing = Data_Testing.drop(exclude, axis=1)
testArr = Input_Data_Testing.as_matrix()
results = forest.predict(testArr)

Data_Testing['predictions'] = results
Data_Testing.head()


# In[84]:

#see percentage of right predictions
correct = list(Data_Testing[Data_Testing['raterScale'] == Data_Testing['predictions']].index)
A = len(correct)
percCorrect = A/Data_Testing['raterScale'].size
percCorrect


# The first attempt resulted in a 37% success of predicions with n_estimatos = 100. 

# In[ ]:

#See features importance
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()


# In[ ]:

#Initialize
forest = RandomForestClassifier(n_estimators = 500)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr,trainRes_1)

# Take the same decision trees and run it on the test data
Data_Testing = Data_Simple2.sample(frac=0.2)
Input_Data_Testing = Data_Testing.drop(exclude, axis=1)
testArr = Input_Data_Testing.as_matrix()
results2 = forest.predict(testArr)

Data_Testing['predictions2'] = results2
Data_Testing.head()


# In[ ]:



