#! /usr/bin/env python3

import numpy as np
import pandas as pd

df_tracks = pd.read_pickle('./dataset/tracks.pickle')
df_af = pd.read_pickle('./dataset/audio_features.pickle')
df_aa = pd.read_pickle('./dataset/audio_analysis.pickle')

def date_formator(date):
    if '-' in date:
        year = pd.to_datetime(date, format = '%Y-%m-%d').year
        return int(year)
    elif int(date)>0:
        year = pd.to_datetime(date, format = '%Y').year
        return int(year)
    return None

df_tracks['release_date'] = df_tracks['album'].map(lambda x: x['release_date'])
df_tracks['release_date'] = df_tracks['release_date'].apply(date_formator)
df_tracks['album_name'] = df_tracks['album'].map(lambda x: x['name'])
df_track_af = pd.merge(df_tracks, df_af, on = 'id')

df_aa_ids = df_aa.id.unique()
timbre = []
pitches = []

for track_id in df_aa_ids:
    rows = df_aa[df_aa['id'] == track_id]
    t = np.vstack(rows['timbre'].values)
    timbre_mean = t.mean(0)
    timbre_std = t.std(0)
    timbre.append(np.hstack([timbre_mean, timbre_std]))

    p = np.vstack(rows['pitches'].values)
    pitches_mean = p.mean(0)
    pitches_std = p.std(0)
    pitches.append(np.hstack([pitches_mean, pitches_std]))

X_timbre = pd.DataFrame(
    timbre,
    index = df_aa_ids,
    columns = ['timbre_mean_%d' % x for x in range(0, 12)] + ['timbre_std_%d' % x for x in range(0, 12)]
)
X_timbre.index.name = 'id'

X_pitches = pd.DataFrame(
    pitches,
    index = df_aa_ids,
    columns = ['pitches_mean_%d' % x for x in range(0, 12)] + ['pitches_std_%d' % x for x in range(0, 12)]
)
X_pitches.index.name = 'id'

df_all = pd.merge(df_track_af, X_timbre, on = 'id')
df_all = pd.merge(df_all, X_pitches, on = 'id')

df_all.rename(
    columns = {
        'duration_ms_x': 'duration_ms'
    },
    inplace = True,
 )
del df_all['duration_ms_y']
del df_all['type_x']
del df_all['type_y']
del df_all['uri_x']
del df_all['uri_y']

df_all.to_csv('./dataset/dm-ct-tp1-dataset.csv', header = True, index = True)
