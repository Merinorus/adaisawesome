
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[3]:

filename ="CrowdstormingDataJuly1st.csv"
Data = pd.read_csv(filename)


# In[5]:

Data.ix[:10,:13]


# In[7]:

Data.ix[:10,13:28]


# In[31]:

test = Data[Data['yellowReds']>0]
test = test.reset_index()
test.ix[:10,13:28]


# In[ ]:

# TODO: disaggregate


# In[36]:

from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt

def main():
    #create the training & test sets, skipping the header row with [1:]
    dataset = genfromtxt(open(Data,'r'), delimiter=',', dtype='f8')[1:]    
    target = [x[0] for x in dataset]
    train = [x[1:] for x in dataset]
    test = genfromtxt(open(Data,'r'), delimiter=',', dtype='f8')[1:]
    
    #create and train the random forest
    #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train, target)

    savetxt('Data/submission2.csv', rf.predict(test), delimiter=',', fmt='%f')

if __name__=="__main__":
    main()


# In[ ]:



