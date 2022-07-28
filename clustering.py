#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 19:20:39 2022

@author: ninathomas
"""

# -------------------------------------------------------------------------- # 
#
# CLUSTER SONGS WITH SIMILAR CHARACTERISTICS
#
# and then perhaps from here, you can take averages of your entire thing
# and then see where your clusters fit
# 
# -------------------------------------------------------------------------- # 

import pandas as pd
import json
import numpy as np
import requests 
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------- #
#
# ALLOW FOR INTERACTIVE GRAPHICS
# 
# -------------------------------------------------------------------------- #

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


from statsmodels.tsa.seasonal import seasonal_decompose


# -------------------------------------------------------------------------- #
#
# ALOOW FOR CLUSTERING
#
# -------------------------------------------------------------------------- #

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.graph_objs as pgo


# -------------------------------------------------------------------------- #
#
# ALLOW FOR VISUALIZING THE NETWORKS 
# using igraph
# wait would you even need a network to do this? since there's not really connections?
# 
# -------------------------------------------------------------------------- #

streaming_history = pd.read_csv('combined_df.csv')

# DO VALUE_COUNTS TO FIND THE SONGS THAT HAVE LESS THAN ONE PLAY AND REMOVE
values = streaming_history['id'].value_counts().to_frame()

values = values[values['id'] > 5]

ids = list(values.index) # puts each song into a list of tuples (song, artist)

# GROUP BY SONG NAME
grouped_songs = (streaming_history
                 .groupby(['track_name', 'artist_name', 'id'])
                 .mean('count')
                 .reset_index())

clean_songs = grouped_songs[grouped_songs['id'].isin(ids)]

# CLUSTER BASED ON FEATURES
# https://plotly.com/python/v3/ipython-notebooks/baltimore-vital-signs/
clean_songs = clean_songs.set_index(['track_name', 'artist_name', 'id'])

# create an array
song_array = np.array(clean_songs)
scaler = StandardScaler()
songs_scaled = scaler.fit_transform(song_array)

pca = PCA()
pca.fit(songs_scaled)

PCA(copy=True, n_components=2, whiten=False)

len(pca.components_) # the amoung of dimensions used in principle component analysis, 13

# the indexed number tells how many of the principle components account for variance
# all the components count pretty evenly
print('Explained Variance Ratio = ', sum(pca.explained_variance_ratio_[: 5])) 

df_songs_scaled = pd.DataFrame(songs_scaled, index=clean_songs.index) # assigns all the k means to each song/feature

# clustering function
def cluster(n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(songs_scaled)
    Z = kmeans.predict(songs_scaled)
    return kmeans, Z

# test the optimal number of clusters
# https://predictivehacks.com/k-means-elbow-method-code-for-python/
distortions = []
K = range(1,13)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(songs_scaled)
    distortions.append(kmeanModel.inertia_)
    
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k') # think it says 9
plt.show()

n_clusters = 7
model, Z = cluster(n_clusters)

df_songs_scaled["cluster"] = Z

pca_2 = PCA(n_components=2)
pc_2 = pd.DataFrame(pca_2.fit_transform(plotX.drop(["Cluster"], axis=1)))

