#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 02:32:53 2022

@author: ninathomas
"""

import json
import pandas as pd
import requests 
import numpy as np

import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time
# import Image
import spotipy

# -------------------------------------------------------------------------- #
#
# SUGGESTIONS
# 1. SMOOTH TRENDLINES
# 2. CONNECT EXCERPTS IN THE JOURNAL 
# 3. FIND THE SONGS THAT WERE TOP PLAYED
    # CONNECT THE EMOTIONS YOU FEEL TOWARDS THOSE SONGS
# 4. CREATE A MORE INTERACTIVE DASHBOARD
# 5. MODE AND KEY WOULD LIKELY BE BETTER AS DIFFERENT TYPES OF VISUALS
    # DROPDOWN
# 6. WHAT IS THE POTENTIAL FOR HEATMAPS AND ENERGY
# 7. LOOK AT ASSOCIATIONS BETWEEN NIGHTTIME AND DAYTIME 
# 8. PLOT AN AVERAGE OF SOME SORT FOR EACH OF THESE FEATURES
# 9. FIGURE OUT HOW YOU CAN ADD MORE DATA
# 10. SELECT A SONG AND SEE HOW THE FREQUENCY OF IT HAS CHANGED OVER TIME 
#
# -------------------------------------------------------------------------- #

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


pd.set_option('max_columns', None)

# -------------------------------------------------------------------------- #
#
# SET UP ACCESS TO SPOTIFY API
# 
# -------------------------------------------------------------------------- #

spotify_url = 'https://api.spotify.com/v1'

client_id = '86519bf4cf3e4d258b5d102a86732510' # 86519bf4cf3e4d258b5d102a86732510

client_secret = 'b07ea5ec997442f6abac1f594c74c22b' # b07ea5ec997442f6abac1f594c74c22b

redirect_uri = 'https://cathomas.georgetown.domains/ANLY560/AboutMe.html'

# client_credentials_manager = SpotifyClientCredentials(client_id = client_id, 
                                                      # client_secret = client_secret)
scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = redirect_uri,
                                               scope=scope))

complete_df = pd.read_csv('combined_df.csv') # because the file was made as combined


# -------------------------------------------------------------------------- #
#
# VALENCE
# 
# -------------------------------------------------------------------------- #
complete_df['date_time'] = pd.to_datetime(complete_df['end_time'])


complete_df.set_index('date_time', inplace=True)

analysis = complete_df[['valence']].copy()


decompose_result_mult = seasonal_decompose(analysis, model="additive", period = int(len(analysis)/12))

trend = decompose_result_mult.trend.to_frame().reset_index()
seasonal = decompose_result_mult.seasonal
residual = decompose_result_mult.resid

decompose_result_mult.plot();

valence = px.line(
    trend,  # sort values to be plotted chronologically
    x='date_time',
    y='trend',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-2, 2],
    title="Nina's Spotify Streaming Valence from February 15th, 2021 – March 3, 2021",
    labels={"date_time": "Time", "trend": "Valence"},
)
valence.update_layout(hovermode="x")



pio.write_html(valence, file="valence.html", auto_open=True)



# -------------------------------------------------------------------------- #
#
# ENERGY
# 
# -------------------------------------------------------------------------- #

energy = px.line(
    complete_df.sort_values('end_time'),  # sort values to be plotted chronologically
    x='end_time',
    y='energy',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-2, 2],
    title="Nina's Spotify Streaming Energy from February 15th, 2021 – March 3, 2021",
    labels={"end_time": "Time", "energy": "Energy"},
)

pio.write_html(energy, file="energy.html", auto_open=True)


# -------------------------------------------------------------------------- #
#
# MODE
# 
# -------------------------------------------------------------------------- #

mode = px.line(
    complete_df.sort_values('end_time'),  # sort values to be plotted chronologically
    x='end_time',
    y='mode',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-2, 2],
    title="Nina's Spotify Streaming Mode from February 15th, 2021 – March 3, 2021",
    labels={"end_time": "Time", "mode": "Mode"},
)

pio.write_html(mode, file="mode.html", auto_open=True)

# -------------------------------------------------------------------------- #
#
# DANCEABILITY
# 
# -------------------------------------------------------------------------- #

danceability = px.line(
    complete_df.sort_values('end_time'),  # sort values to be plotted chronologically
    x='end_time',
    y='danceability',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-2, 2],
    title="Nina's Spotify Streaming Danceability from February 15th, 2021 – March 3, 2021",
    labels={"end_time": "Time", "danceability": "Danceability"},
)

pio.write_html(danceability, file="danceability.html", auto_open=True)

# -------------------------------------------------------------------------- #
#
# KEY
#
# WOULD DEFINITELY BE MORE APPEALING WITH A BAR GRAPH OF SOME SORT
# 
# -------------------------------------------------------------------------- #

key = px.line(
    complete_df.sort_values('end_time'),  # sort values to be plotted chronologically
    x='end_time',
    y='key',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-1, 15],
    title="Nina's Spotify Streaming Key from February 15th, 2021 – March 3, 2021",
    labels={"end_time": "Time", "key": "Key"},
)

pio.write_html(key, file="key.html", auto_open=True)

# -------------------------------------------------------------------------- #
#
# TEMPO
# 
# -------------------------------------------------------------------------- #

tempo = px.line(
    complete_df.sort_values('end_time'),  # sort values to be plotted chronologically
    x='end_time',
    y='tempo',
    color_discrete_sequence=px.colors.qualitative.Bold,
    range_y=[-10, 250],
    title="Nina's Spotify Streaming Tempo from February 15th, 2021 – March 3, 2021",
    labels={"end_time": "Time", "tempo": "Tempo"},
)

pio.write_html(tempo, file="tempo.html", auto_open=True)















