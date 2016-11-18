
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


# # II. Preparing the training & test data : Unique Game Row version

# ### 1) Keep only players that have a Rater Image

# In[6]:

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

# In[16]:

Data_hasImage['mean_rater']=(Data_hasImage['rater1']+Data_hasImage['rater2'])/2


# Let's now disaggregate the games:

# In[37]:

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

# In[44]:

# Removing columns that we do not need
Data_Simple1 = Data_OneGamePerRow[['playerShort', 'yellowCards', 'yellowReds', 'redCards',
                              'refNum', 'refCountry', 'mean_rater']]

# Take a random 80% sample of the Data for the Training Sample
Data_Training = Data_Simple1.sample(frac=0.8)

# Take a random 20% sample of the Data for the Testing Sample
Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]


# In[45]:

Data_Simple1


# # II. Preparing the training & test data : Fraction version

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

# In[104]:

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


# In[112]:

# Need to make arrays
# http://www.analyticbridge.com/profiles/blogs/random-forest-in-python

trainArr = Input_Data_Training.as_matrix(cols) #training array
trainRes = Results_Data_Training.as_matrix(colsRes) #training results
#trainRes = np.asarray(Data_Training['raterAvg'], dtype="|S6")

trainRes


# # III. Random Forest

# In[3]:

#Initialize
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr,trainRes)

# Take the same decision trees and run it on the test data
#testArr = test.as_matrix(cols)
#results = rf.predict(testArr)

#test['predictions'] = results
#test.head()


# In[ ]:



