#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import statistics as stat
import networkx as nx
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import LSTM, Dense, Input, Embedding, Reshape
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from glob import glob


# In[ ]:





# In[2]:


# meta data includes the course title, run dates
AM_meta = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-meta.csv')
AM_meta


# In[3]:


# complete course structure and module descriptions
# list of student identifiers and performance statistics, certification, and enrollment data
# problem UTF-encoding error

AM_modules = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-modules.txt', sep='\t', encoding='utf-16')
AM_modules


# In[4]:


# session level edge data
AM_edges_sessionLevel01 = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/edges/MITxPRO+AMxB+1T2018-stdAgg-edgeList-sessionLevel-1.csv')
AM_edges_sessionLevel01[AM_edges_sessionLevel01['user_id'] == 15779327][100:150]


# In[7]:


# for each student this is list of numerical id's for the URLs - removing duplicates
def get_trajectory(df):
    order = [0]
    for url in df['order']:
        if url != order[-1]:
            order.append(url)
    order.append(0)
    return order

trajectories = []

for fname in glob('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/edges/*.csv'):
    df = pd.read_csv(fname)
    trajectories.append(df)
    
trajectories = pd.concat(trajectories)
trajectories = trajectories.groupby('user_id').apply(get_trajectory)
traj_lengths = trajectories.map(len).values

plt.hist(traj_lengths)
max(traj_lengths)
trajectories[:25]


# In[96]:


# x = np.zeros((31, 520))
# for i, traj in enumerate(trajectories.values):
#     x[i, : len(traj)] = traj

# y = x[:, 1:].reshape(31, -1, 1)
# x = x[:, :-1]

x = []
y = []
for traj in trajectories.values:
    x.append(np.array(traj[:-1]).reshape(1,-1))
    y.append(np.array(traj[1:]).reshape(-1,1))
x


# In[97]:


hidden_dim = 30
embedding_dim = 30
number_of_URL = 1121
optimizer = Adam(learning_rate=0.001)

input_ = Input(shape=(None,))
embed = Embedding(number_of_URL, embedding_dim)(input_)

rnn = LSTM(hidden_dim, return_sequences=True)(embed)

predicted_URL = Dense(number_of_URL, activation = 'softmax')(rnn)

model = Model(inputs=input_, outputs=predicted_URL)
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['acc'])
model.summary()


# In[98]:


model.fit(x,y, batch_size=1, epochs=90)


# In[ ]:


# user list key - session level
AM_userList = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-stdAgg-userList-key-sessionLevel.csv')
AM_userList


# In[5]:


# learning pathway network edge lists - edge list for each student in the course that represent a directed 
# transitions networks  of students pathway through the courses content modules.  this is all students.
AM_edgelist = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-stdAgg-edges-cohort.csv')
AM_edgelist[:5]


# In[6]:


G = nx.DiGraph()
edges = [x[1].values for x in AM_edgelist.iloc[:,:3].iterrows() if x[1][2] > 20]
G.add_weighted_edges_from(edges)


# In[7]:


#pos=nx.kamada_kawai_layout(G)
# plt.figure(figsize=(12,12))
# nx.draw(G, node_size=10)
# plt.show()


# In[8]:


# node list of all students' learning pathway networks
AM_nodelist = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-stdAgg-nodes-cohort.csv')
AM_nodelist


# In[9]:


# appendix to the node list that provides a set of XY coordinates to generate a common layout for all networks 
# produced in the analysis.  force atlas with parameterization <- what is this?
AM_node_coord = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO+AMxB+1T2018-stdAgg-nodes-coordinates-FA2.csv')
AM_node_coord[:5]


# In[10]:


# student identifiers and performance statistics, certification, and enrollment data
AM_id_and_performance = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+AMxB+1T2018/MITxPRO-AMxB-1T2018-auth_user-students.csv')
AM_id_and_performance[:5]


# In[11]:


# meta data includes the course title, run dates
LaaL_meta = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO+LASERxB1+1T2019-meta.csv')
LaaL_meta


# In[12]:


# complete course structure and module descriptions
# list of student identifiers and performance statistics, certification, and enrollment data
# problem UTF-encoding error

# LaaL_edgelist = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO+LASERxB1+1T2019-modules.csv')
# LaaL_edgelist


# In[13]:


LaaL_edelist = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO+LASERxB1+1T2019-stdAgg-edges.csv')
LaaL_edelist[:5]


# In[14]:


LaaL_nodelist = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO+LASERxB1+1T2019-stdAgg-nodes.csv')
LaaL_nodelist[:5]


# In[15]:


LaaL_node_coord = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO+LASERxB1+1T2019-stdAgg-nodes-coordinates-FA2.csv')
LaaL_node_coord[:5]


# In[16]:


LaaL_id_and_performance = pd.read_csv('edx-learnerpathway-modeling/data/MITxPRO+LASERxB1+1T2019/MITxPRO-LASERxB1-1T2019-auth_user-students.csv')
LaaL_id_and_performance[:5]


# In[ ]:





# In[ ]:





# In[ ]:




