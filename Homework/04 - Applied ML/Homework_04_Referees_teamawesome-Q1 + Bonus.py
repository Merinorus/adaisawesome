
# coding: utf-8

# # I. Setting up the Problem

# In[2]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 


# In[3]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# ### 1) Peeking into the Data

# In[4]:

Data.ix[:10,:13]


# In[5]:

Data.ix[:10,13:28]


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

# In[7]:

Data_hasImage['mean_rater']=(Data_hasImage['rater1']+Data_hasImage['rater2'])/2


# Let's now disaggregate the games:

# In[8]:

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

# In[9]:

# Removing columns that we do not need
Data_Simple1 = Data_OneGamePerRow[['playerShort', 'yellowCards', 'yellowReds', 'redCards',
                              'refNum', 'refCountry', 'games', 'position', 'mean_rater']]

# Take a random 80% sample of the Data for the Training Sample
#Data_Training = Data_Simple1.sample(frac=0.8)

# Take a random 20% sample of the Data for the Testing Sample
#Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]


# In[10]:

Data_Simple1


# In[11]:

#find proportion of yellow & red cards to games
Data_Simple1['fractionYellow'] = Data_Simple1['yellowCards']/Data_Simple1['games']
Data_Simple1['fractionYellowRed'] = Data_Simple1['yellowReds']/Data_Simple1['games']
Data_Simple1['fractionRed'] = Data_Simple1['redCards']/Data_Simple1['games']
Data_Simple2 = Data_Simple1[['playerShort', 'fractionYellow', 'fractionYellowRed', 'fractionRed',
                              'refNum', 'refCountry', 'games', 'position', 'mean_rater']]
Data_Simple2


# In[12]:

allpositions = (Data_Simple2['position'])
unique_pos = set(allpositions)
unique_pos_list = list(unique_pos)

unique_pos_list


# In[13]:

# we must convert players positions into proxy numbers (floats) to run random forest
position_proxy = []
A = len(allpositions)
for i in range (0,A):
        if allpositions[i] == 'NaN':
            position_proxy.append(0);
        elif allpositions[i] == 'Center Midfielder':
            position_proxy.append(1);
        elif allpositions[i] == 'Attacking Midfielder':
            position_proxy.append(2);
        elif allpositions[i] == 'Goalkeeper':
            position_proxy.append(3);
        elif allpositions[i] == 'Right Winger':
            position_proxy.append(4);
        elif allpositions[i] == 'Left Winger':
            position_proxy.append(5);
        elif allpositions[i] == 'Center Forward':
            position_proxy.append(6);
        elif allpositions[i] == 'Right Fullback':
            position_proxy.append(7);
        elif allpositions[i] == 'Right Midfielder':
            position_proxy.append(8);
        elif allpositions[i] == 'Defensive Midfielder':
            position_proxy.append(9);
        elif allpositions[i] == 'Center Back':
            position_proxy.append(10);
        elif allpositions[i] == 'Left Fullback':
            position_proxy.append(11);
        elif allpositions[i] == 'Left Midfielder':
            position_proxy.append(12);
        else:
            position_proxy.append(99);


       




# In[14]:

Data_Simple2['position_proxy'] = position_proxy
Data_Simple3 = Data_Simple2[['playerShort', 'fractionYellow', 'fractionYellowRed', 'fractionRed',
                              'refNum', 'refCountry', 'games', 'position_proxy', 'mean_rater']]
Data_Simple3.head()


# In[15]:

colRate = ['mean_rater']
Col_Rating = Data_Simple3[colRate].values
Ratings_Scale = []; 
Col_Rating


# In[16]:

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
        
Data_Simple3['raterScale'] = Ratings_Scale
Data_Simple3.head()

## Some of the values in trainRes_1 are larger than one! We must delete them from the simple data set to avoid errors in the training process.


# In[17]:

# drop values on scale which are equal to 99
Data_Simple4 = Data_Simple3[Data_Simple3.raterScale != 99]
Data_Simple5 = Data_Simple4[Data_Simple4.position_proxy != 99]
Data_Simple5.dropna(axis=0)
Data_Simple5


# # II. Preparing the training & test data : Fraction version

# ### 1) Create the Training and Testing Datframes with only select data

# In[18]:

#create test and training matrix

cols = ['games', 'fractionYellow', 'fractionYellowRed', 'fractionRed', 'refNum', 'refCountry', 'position_proxy']
exclude = ['raterScale','mean_rater', 'playerShort']
colsRes1 = ['raterScale']


# Take a random 80% sample of the Data for the Training Sample
Data_Training = Data_Simple5.sample(frac=0.8)

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
Input_Data_Training = Data_Training.drop(exclude, axis=1)

#Results_Data_Training = list(Data_Training.raterAvg.values)
Results_Data_Training = Data_Training[colsRes1]
Input_Data_Training.head()


# In[19]:

# Take a random 20% sample of the Data for the Testing Sample
#Data_Testing = Data_Simple1.loc[~Data_Simple1.index.isin(Data_Training.index)]

# Need to split this into the data and the results columns
# http://stackoverflow.com/questions/34246336/python-randomforest-unknown-label-error
#Input_Data_Testing = Data_Testing.drop(colsRes, axis=1)
#Results_Data_Testing = list(Data_Testing.raterAvg.values)


# In[20]:

# Need to make arrays
# http://www.analyticbridge.com/profiles/blogs/random-forest-in-python
trainArr = Input_Data_Training.as_matrix() #training array
#trainRes = Results_Data_Training.as_matrix(colsRes) #training results
trainRes_1 = Data_Training['raterScale'].values
trainArr


# # III. Random Forest

# In[21]:

#Initialize
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr,trainRes_1)

# Take the same decision trees and run it on the test data
Data_Testing = Data_Simple5.sample(frac=0.2)
Input_Data_Testing = Data_Testing.drop(exclude, axis=1)
testArr = Input_Data_Testing.as_matrix()
results = forest.predict(testArr)

Data_Testing['predictions'] = results
Data_Testing.head()


# In[23]:

#see percentage of right predictions
correct = list(Data_Testing[Data_Testing['raterScale'] == Data_Testing['predictions']].index)
A = len(correct)
percCorrect = A/Data_Testing['raterScale'].size
percCorrect


# The first attempt resulted in a 69,4% success of predicions with n_estimatos = 100. 

# In[25]:

#See features importance
importances = forest.feature_importances_
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(trainArr.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))



# redCountry, Games, Position, and redNum are the most important features. We could therefore drop some features already, such as fraction yellow and fraction yellowRed & fraction Red. Let us delete all cards and see if we can better predict this. 

# In[27]:

#make necessary changes to parameters
exclude2 = ['raterScale','mean_rater', 'playerShort', 'fractionYellowRed', 'fractionRed', 'fractionYellow']
exclude3 = ['raterScale','mean_rater', 'playerShort', 'fractionYellowRed', 'fractionRed', 'fractionYellow', 'predictions']
Input_Data_Training2 = Data_Training.drop(exclude2, axis=1)
trainArr2 = Input_Data_Training2.as_matrix() #training array
trainRes_2 = Data_Training['raterScale'].values


Input_Data_Testing2 = Data_Testing.drop(exclude3, axis=1)
testArr2 = Input_Data_Testing2.as_matrix()

testArr2


# In[37]:

#Re-Initialize Classifier
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr2,trainRes_2)

# Take the same decision trees and run it on the test data
results2 = forest.predict(testArr2)

Data_Testing['predictions2'] = results2
Data_Testing.head()


# In[38]:

#see percentage of right predictions
correct = list(Data_Testing[Data_Testing['raterScale'] == Data_Testing['predictions2']].index)
A = len(correct)
percCorrect = A/Data_Testing['raterScale'].size
percCorrect


# Accuracy goes down to 67.3% from changing the input parameters...

# In[39]:

#See features importance
importances = forest.feature_importances_
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(trainArr2.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))



# The most important feature in this case is refNum, games, refCountry, position_proxy

# Alternatively we can see what happens when we only use the number of cards...

# In[31]:

exclude4 = ['raterScale','mean_rater', 'playerShort', 'refNum', 'refCountry', 'games', 'position_proxy']
exclude5 = ['raterScale','mean_rater', 'playerShort', 'refNum', 'refCountry', 'games', 'position_proxy', 'predictions', 'predictions2']
Input_Data_Training3 = Data_Training.drop(exclude4, axis=1)
trainArr3 = Input_Data_Training3.as_matrix() #training array
trainRes_3 = Data_Training['raterScale'].values


Input_Data_Testing3 = Data_Testing.drop(exclude5, axis=1)
testArr3 = Input_Data_Testing3.as_matrix()

testArr3


# In[32]:

#Re-Initialize Classifier
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data and create the decision trees
forest = forest.fit(trainArr3,trainRes_3)

# Take the same decision trees and run it on the test data
results3 = forest.predict(testArr3)

Data_Testing['predictions3'] = results3
Data_Testing.head()


# In[33]:

#see percentage of right predictions
correct = list(Data_Testing[Data_Testing['raterScale'] == Data_Testing['predictions3']].index)
A = len(correct)
percCorrect = A/Data_Testing['raterScale'].size
percCorrect


# The percentage of correct ratings drops to 32%...

# BONUS Question: We can try to analyze accuracy across the scale for the three cases above and see if there is bias in any extreme

# In[34]:

# Curve for Test 1 - all variables
Test1 = [];
for i in range (0,20):
    count = list(Data_Testing[Data_Testing['predictions']==i].index)
    A = len(count)
    Test1.append(A)
# Curve for Test 2 - exclude card variables
Test2 = [];
for i in range (0,20):
    count2 = list(Data_Testing[Data_Testing['predictions2']==i].index)
    B = len(count2)
    Test2.append(B)
# Curve for Test 3 - only card variables
Test3 = [];
for i in range (0,20):
    count3 = list(Data_Testing[Data_Testing['predictions3']==i].index)
    C = len(count3)
    Test3.append(C)
# Real Curve
Test4 = [];
for i in range (0,20):
    count4 = list(Data_Testing[Data_Testing['raterScale']==i].index)
    D = len(count4)
    Test4.append(D)


# In[35]:

import matplotlib.patches as mpatches

X = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20];
T1 = plt.plot(X, Test1,'b')
T2 = plt.plot(X, Test2, 'r')
T3 = plt.plot(X, Test3, 'g')
T4 = plt.plot(X, Test4, 'y')

plt.ylabel('Count')
plt.xlabel('Rater Scale')
plt.show()


# The first two models slightly overestimate number of players on the lower end of the scale, while slightly underestimating players on the middle and higher end. Conversely, when using only card numbers, there is a huge bias around the 6-7 values, with a significant overshoot, while completely underestimating other values. 

# In[ ]:



