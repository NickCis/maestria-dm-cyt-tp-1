#! /usr/bin/env python3

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN

df = pd.read_csv('./dataset/dm-ct-tp1-dataset.csv')

external_validation_columns = [
    'artists',
    'album_name',
    'release_date',
    'genre'
]

audio_features_columns = [
  'danceability',
  'energy',
  'key',
  'loudness',
  'mode',
  'speechiness',
  'acousticness',
  'instrumentalness',
  'liveness',
  'valence',
  'tempo',
  'duration_ms',
  'time_signature'
]

audio_analysis_columns = ['timbre_mean_%d' % x for x in range(0, 12)] + ['timbre_std_%d' % x for x in range(0, 12)] + ['pitches_mean_%d' % x for x in range(0, 12)] + ['pitches_std_%d' % x for x in range(0, 12)]

standard_scaler = StandardScaler()
df_scaled = df.copy()
df_scaled.dropna(subset = audio_features_columns + external_validation_columns, inplace = True)

df_scaled[audio_features_columns + audio_analysis_columns] = standard_scaler.fit_transform(df_scaled[audio_features_columns + audio_analysis_columns])


kmeans_model = KMeans(n_clusters = 6).fit(df_scaled[audio_features_columns + audio_analysis_columns])
df_scaled['kmeans'] = kmeans_model.labels_

agglomerative_model = AgglomerativeClustering(n_clusters = 8, affinity = 'euclidean', linkage = 'ward').fit(df_scaled[audio_features_columns + audio_analysis_columns])
df_scaled['agglomerative'] = agglomerative_model.labels_

dbscan_model = DBSCAN(eps = 8, min_samples = 2).fit(df_scaled[audio_features_columns + audio_analysis_columns])
df_scaled['dbscan'] = dbscan_model.labels_

df_scaled.to_csv('./dataset/result.csv', header = True, index = True, columns = ['kmeans', 'agglomerative', 'dbscan'])
