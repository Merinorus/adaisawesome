
# coding: utf-8

# ## Assignment:

# BONUS: build the communication graph (unweighted and undirected) among the different email senders and recipients using the NetworkX library. Find communities in this graph with community.best_partition(G) method from the community detection module. Print the most frequent 20 words used by the email authors of each community. Do these word lists look similar to what you've produced at step 3 with LDA? Can you identify clear discussion topics for each community? Discuss briefly the obtained results.

# ### Make the Graph 

# In[22]:

import pandas as pd
import numpy as np
import networkx as nx
import math


# In[47]:

G=nx.Graph()
emails = pd.read_csv('hillary-clinton-emails/emails.csv')
receivers = pd.read_csv('hillary-clinton-emails/EmailReceivers.csv')

nodes = pd.DataFrame()

emails = emails[pd.notnull(emails['SenderPersonId'])]

nodes['EmailID'] = emails['Id']
nodes['SenderID'] = emails['SenderPersonId']
nodes.SenderID = nodes.SenderID.astype(int)
nodes['ReceiverID'] = 'nan'

nodes.head()


# In[49]:

#Now we need to link the receivers (all of them) to the EmailID.

nodes_short = nodes.head(5)
for index, row in nodes_short.iterrows():
    #print(row['EmailID'])
    #for index, row in receivers[row['EmailID']]:
        #print('HI')

    #G.add_edges_from[(a,b)]
#print(list(G.edges()))


# ### Partition the Graph 

# In[4]:

community.best_partition(G)


# In[ ]:



