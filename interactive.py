#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 18:45:40 2022

@author: ninathomas
"""


import json
import pandas as pd
import requests 
import numpy as np
from datetime import datetime
from IPython.display import display

import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time
# import Image
import spotipy

# -------------------------------------------------------------------------- #
#
# ALLOW FOR INTERACTIVE GRAPHICS
# 
# -------------------------------------------------------------------------- #

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from ipywidgets import interactive, HBox, VBox

from statsmodels.tsa.seasonal import seasonal_decompose

# https://dash.plotly.com/interactive-graphing
from dash import Dash, html, dcc, Input, Output 

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

complete_df = pd.read_csv('combined_df.csv')
measures = ['danceability', 'energy', 'key', 'mode', 'tempo', 'valence']

# -------------------------------------------------------------------------- #
#
# NEED A WAY TO VISUALIZE THE SONGS WITH THE GREATEST/LEAST VALUES
#
# AND WHEN THEY WERE LISTENED TO 
#
# -------------------------------------------------------------------------- #

# -------------------------------------------------------------------------- #
#
# THIS COULD ALSO BE SHOWN ON A TIME SERIES PLOT
#
# ONLY SELECT THE ONES WITH THE GREATEST VALUES (SHAPE/COLOR A SPECIFIC WAY) 
# AND PLOT ON THE DAYS THAT THEY WERE PLAYED
#
# -------------------------------------------------------------------------- #

non_dt_complete_df = complete_df.copy()
# convert end_time to datetime object
complete_df['end_time'] = pd.to_datetime(complete_df['end_time'])

dt_complete_df = complete_df.set_index('end_time', inplace=False)


valence_noise = go.FigureWidget([go.Scatter(
        x = dt_complete_df.index,
        y = dt_complete_df["valence"],
        name = "valence",
        hovertemplate = "%{x}: <br>%{y} </br>",
        mode='markers')]) # could make a list of many figure widgets 


valence_noise.update_layout(hovermode="x",
                      font_family = "Optima",
                      plot_bgcolor='#FFFFFF',
                      font_color = '#05204A',
                      height = 650,
                      title={
                            'y':0.95,
                            'x':0.5,
                            'font_size': 30,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                      hoverlabel=dict(font_size=16,
                                      font_family="Optima"))

scatter = valence_noise.data[0] 

# pio.write_html(valence_noise, file="interactive.html", auto_open=True)

t = go.FigureWidget([go.Table(
    header=dict(values=['artist_name','track_name','valence'],
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=[dt_complete_df[col] for col in ['artist_name','track_name','valence']],
               fill = dict(color='#F5F8FF'),
               align = ['left'] * 5))])

def selection_fn(trace,points,selector):
    t.data[0].cells.values = [dt_complete_df.loc[points.point_inds][col] for col in ['artist_name','track_name','valence']]

scatter.on_selection(selection_fn)

box = HBox([VBox(t)]) # layout={'border': '3px solid black','width':'55%'})
# display(box)
# pio.write_html(t, file="box.html", auto_open=True)


"""
with open('interactive_graphs.html', 'w') as f:
    f.write(valence_noise.to_html(full_html=False, include_plotlyjs='cdn')) # perhaps the key to getting the arrays 
    f.write(t.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(box.to_html(full_html=False, include_plotlyjs='cdn'))
"""    



