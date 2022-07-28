#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:29:27 2022

@author: ninathomas
"""

import json
import pandas as pd
import requests 
import numpy as np
from datetime import datetime

import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time
import spotipy

# -------------------------------------------------------------------------- #
#
# TO ADDRESS IN THE FUTURE:
    # 1. Fix the noise plot so that it updates in correspondance with the time series
    # and fix the boxplot so that it updates in correspondance with what you select
    # on the time series
    # 2. change the formatting to look better (particularly the colors)
    # 3. Merge on the count to identify the songs that were played the most
    # - 3. Reformat the summary statistics
    # - 3. add better data so you can talk about more recent news
    # 4. find places in the data that correspond to specific life events
    # 5. for the top songs, take averages to find the song that best matches 
    # your music taste (find song that best matches the averages)
    # 6. You should also be able to input notes from your journal given certain
    # days
    # 7. Look at the on_repeat playlist that you have and figure out a way to 
    # summarize it
    # 8. You can do a wordcloud for the lyrics in your songs, or you can
    # refer to the lecture from 3/30/22 to find the code to get better text 
    # analysis
    # 9. Look for daily trends
    # 10. Kmeans clustering on the number of times songs were listened to (and 
    # identifying the best predictors for the number of times a song was 
    # listened to)
    # 11. Inserting album art to make the dashboard more visually appealing!
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

from dash import Dash, html, dcc, Input, Output 

pd.set_option('max_columns', None)

# -------------------------------------------------------------------------- #
#
# SET UP ACCESS TO SPOTIFY API
# 
# -------------------------------------------------------------------------- #

spotify_url = 'https://api.spotify.com/v1'

client_id = '' 

client_secret = '' 

redirect_uri = 'https://cathomas.georgetown.domains/ANLY560/AboutMe.html'

scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = redirect_uri,
                                               scope=scope))

complete_df = pd.read_csv('combined_df.csv')
measures = ['valence', 'energy', 'mode', 'danceability', 'key', 'tempo']

# -------------------------------------------------------------------------- #
#
# ADDITIONAL APPLICATION GOALS
# 
# The goal is that when you select a region on the graph, a bar plot
# on the side will show up with the ranked songs
# Additionally, the summary statistics will correspond to that selected 
# region of the plot 
# 
# -------------------------------------------------------------------------- #
# remove columns you don't really want 
complete_df_reduced = complete_df[['end_time', 'artist_name', 'track_name',
                                   'id'] + measures]

# may have to pivot the complete_df in order for this to work 
complete_melt = pd.melt(complete_df_reduced, 
                     id_vars = ['id', 'track_name', 'artist_name', 'end_time'],
                     var_name = 'feature')

# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Other/Dash_Introduction/intro.py
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# -------------------------------------------------------------------------- #
#
# CODE FOR CREATING A FREQUENCY BAR PLOT
#
# -------------------------------------------------------------------------- #

# obtain the frequencies for each song id
counts_listened = (complete_df.groupby(['id'])
                  .count()
                  .reset_index()
                  [['id','end_time']] # select two columns
                  .rename(columns = {'end_time': 'count'}) # rename to count
                  .sort_values('count', ascending = False) # rank from greatest to least
                  .reset_index(drop = True))

# df with counts now, merge based on song id
complete_df_count = complete_df.merge(counts_listened, how = 'left',
                                on = 'id')

# remove the rows with not enough data
complete_df_count_clean = complete_df_count[complete_df_count['count'] > 5]

# use groupby so that each song appears only once
grouped_complete_count = (complete_df_count_clean
                          .groupby(['track_name', 'artist_name', 'id']).mean('count')
                          .sort_values('count', ascending = False)
                          .reset_index())

# remove songs that have duplicate track names
grouped_clean_count = grouped_complete_count.drop_duplicates(subset='track_name', keep=False)
                                                       
# one song doesn't seem to belong... this is because the query in the initial data would
# occassionally lead to the incorrect result
# for the most time, it's correct
counts = px.bar(grouped_clean_count.iloc[0:15], # top 15 songs
                x='track_name', 
                y='count',
                title = 'Top 15 Songs In Selected Period',
                hover_name = 'track_name', # title is the song name
                # hover_data =  ['artist_name'] + measures,
                color = 'count',
                text_auto = True,
                labels = dict(track_name = 'Track', 
                          count = '# of Times Played'),
                color_continuous_scale = 'sunsetdark',
                hover_data = {
                    'track_name': False,
                    'count': False,
                    'artist_name': True,
                    'danceability': True,
                    'energy': True,
                    'key': True,
                    'mode': True,
                    'tempo': True,
                    'valence': True}
                ) # includes the feature values


counts.update_traces(textfont_size=16, # for labels
                    textangle=0, 
                    textposition="outside", 
                    cliponaxis=False)

counts.update_xaxes(showticklabels = False,
                    tickfont = dict(size = 16),
                    title_font=dict(size=20, color='#05204A'),
                    tickangle = 35)

counts.update_yaxes(
                    tickfont = dict(size = 16),
                    title_font=dict(size=20, color='#05204A'))

# here's where we can have a gradient of colors
counts.update_layout(
    plot_bgcolor='#FFFFFF',
    yaxis_range = [0, max(grouped_clean_count['count'])],
    title_font_size = 30,
    width = 800,
    height = 650,
    font_color = '#05204A',
    font_family = 'Optima',
    hoverlabel=dict(
        font_size=16,
        font_family = "Optima"),
    title={
        'y':0.95,
        'x':0.45,
        'font_size': 30,
        'xanchor': 'center',
        'yanchor': 'top'})

# -------------------------------------------------------------------------- #
#
# CREATE A BAR PLOT OF THE STATS OF YOUR ENTIRE STREAMING HISTORY
# 
# -------------------------------------------------------------------------- #

# The categories are:
    # 1. VALENCE
    # 2. ENERGY
    # 3. MODE
    # 4. DANCEABILITY
    # 5. KEY
    # 6. TEMPO
    
# select the columns you want 
complete_df_reduced = complete_df[['end_time', 'artist_name', 'track_name',
                                   'id'] + measures]

# may have to pivot the complete_df in order for this to work 
complete_melt = pd.melt(complete_df_reduced, 
                     id_vars = ['id', 'track_name', 'artist_name', 'end_time'],
                     var_name = 'feature')

# have to turn the values into percentages so they can be relative
# Maximum values for the categories are:
    # 1. 1
    # 2. 1
    # 3. 1
    # 4. 1
    # 5. 11
    # 6. 220

# create the appropriate proportions for features whose maximum values are not 1    
complete_melt['value'] = np.where(complete_melt['feature'] == 'key',
                                 complete_melt['value']/11,
                                 complete_melt['value'])
complete_melt['value'] = np.where(complete_melt['feature'] == 'tempo',
                                 complete_melt['value']/220,
                                 complete_melt['value'])

# now need to grouby this whole thing 
# make sure to keep the names/ids to identify
averages = (complete_melt.groupby(['feature'])
                  .mean().round(2)
                  .reset_index())                  
                    # [['id','end_time']])
                  # .rename(columns = {'end_time': 'average'})
                  # .sort_values('count', ascending = False)
                  # .reset_index(drop = True)
                  # )
   
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features                   
averages['description'] = [
    'Danceability describes how suitable a track is for dancing based on a<br>combination of musical elements including tempo, rhythm stability, beat strength,<br>and overall regularity.<br>A value of 0.0 is least danceable and 1.0 is most danceable.',
    'Energy represents a perceptual measure of intensity and activity.<br>Typically, energetic tracks feel fast, loud, and noisy<br>A value of 0.0 is least energetic and 1.0 is most energetic.',
    'The key the track is in.<br>Integers map to pitches using standard Pitch Class notation.<br>0 = C, 1 = C♯/D♭, 2 = D, and so on until 11.<br>If no key was detected, the value is -1.',
    'Mode indicates the modality (major or minor) of a track,<br>the type of scale from which its melodic content is derived.<br>Major chords are associated with happier songs,<br>while minor chords appear in more subdued songs.<br>Major is represented by 1 and minor is 0.',
    'The overall estimated tempo of a track in beats per minute (BPM).<br>The max tempo in this dataset is 220.',
    'A measure describing the musical positiveness conveyed by a track.<br>Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),<br>while tracks with low valence sound more negative (e.g. sad, depressed, angry).<br>Valence values range from 0.0 to 1.0.'
    ]
              
# create a list of the bar colors
bar_colors = ['#DE3163', '#FB5607', '#028090', '#05204A', '#C70039', '#FFBF00']

# associate each feature with a color
bar_color_dict = {'danceability': '#DE3163',
                  'energy': '#FB5607',
                  'key': '#028090',
                  'mode': '#05204A',
                  'tempo': '#C70039',
                  'valence': '#FFBF00'}
# creat the bar chart
percentages = px.bar(averages, 
                x='feature', 
                y='value',
                # text_auto = '0.2s',
                #color_continuous_scale = bar_colors,
                title = 'Average Values of Track Features Across All Streaming History',
                labels = dict(feature = 'Features', 
                          value = 'Percent (%)'),
                text_auto = True,
                hover_name = 'feature',
                hover_data = {
                    'feature': False,
                    'value': False,
                    'description': True # looks very odd
                    })

# update chart characteristics
percentages.update_xaxes(
                         tickfont = dict(size = 16),
                         title_font=dict(size=20, color='#05204A'))
percentages.update_yaxes(
                         tickfont = dict(size = 16),
                         title_font=dict(size=20, color='#05204A'))
percentages.update_traces(textfont_size=20, # for labels
                          textangle=0, 
                          textposition="outside", 
                          cliponaxis=False
                          )
percentages.update_traces(marker_color=bar_colors) # for borders                 
percentages.update_layout(plot_bgcolor='#FFFFFF',
                          yaxis_range = [0, 1],
                          font_family = 'Optima',
                          font_color = '#05204A',
                          height = 650,
                          yaxis_tickformat = ',.0%',
                           title={
                               'y':0.95,
                               'x':0.5,
                               'font_size': 30,
                               'xanchor': 'center',
                               'yanchor': 'top'},
                           hoverlabel=dict(font_size=16,
                                           font_family="Optima"))

# -------------------------------------------------------------------------- #
#
# CODE FOR VALENCE TIME SERIES
#
# -------------------------------------------------------------------------- #
complete_df_copy = complete_df.copy() # create a copy of the dataframe
non_dt_complete_df = complete_df.copy() 

complete_df_copy['end_time'] = pd.to_datetime(complete_df_copy['end_time'])

# keep date for the time series
dt_complete_df = complete_df_copy.set_index('end_time', inplace=False)

# start with valence as the initial feature to analyze
analysis = dt_complete_df[['valence']].copy()

# decompose the data in order to access the trend
decompose_result_mult = seasonal_decompose(analysis, 
                                           model="additive", 
                                           period = int(len(analysis)/12))

trend = decompose_result_mult.trend.to_frame().reset_index() # will be visualized
seasonal = decompose_result_mult.seasonal
residual = decompose_result_mult.resid

# create the graph that will depict the music feature trends over time
valence = px.line(
    trend,  # sort values to be plotted chronologically
    x='end_time',
    y='trend',
    color_discrete_sequence = px.colors.qualitative.Bold,
    title="Valence History (trends)",
    labels={"end_time": "Time"})

valence.update_xaxes(rangeslider_visible=True)
valence.update_layout(hovermode="x",
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


valence.update_layout(hovermode="x",
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

app.layout = html.Div(children=[
    
    html.H1(children='Music Journal', 
            style = {'font-family': 'Optima',
                     'text-align': 'center',
                     'color': '#355C7D'}),

    html.Br(),
    
    html.Div([
        dcc.Graph(id = 'averages_graph',
                  figure = percentages)
        ], style = {'width': '50%',
                    'display': 'inline-block'}),
                    
    html.Div([        
        dcc.Graph(id='count_boxplot', 
              figure = counts),
        
        html.Br()

        ], style = {'width': '48%',
                    'height': 300,
                    'float': 'right',
                    'display': 'inline-block'}),
    
    html.Div([
        html.Label('Select which feature you would like to see: ',
                   style = { 'color': '#355C7D'}),
        dcc.Dropdown(measures,
                     'valence',
                     id='dropdown_feature', 
                     style = {'width': '50%'}),
        
        dcc.Graph(id='feature_graph', 
              figure=valence)
        ], style = {'width': '100%',
                    'float': 'left',
                    'display': 'inline-block',
                    'font-family': 'Optima'}), 
    ], style = {'font-family': 'Optima'})

@app.callback(
    Output('feature_graph', 'figure'), # output reg time series
    # Output('noisy_graph', 'figure'), # output noise graph
    Input('dropdown_feature', 'value'))
def update_time_series(dropdown_feature): 
    
    value_color = bar_color_dict[dropdown_feature]
    
    analysis = dt_complete_df[[dropdown_feature]].copy()
    
    decompose_result_mult = seasonal_decompose(analysis, model="additive", period = int(len(analysis)/12))
    
    trend = decompose_result_mult.trend.to_frame().reset_index()
    
    # seasonal = decompose_result_mult.seasonal
    # residual = decompose_result_mult.resid
    # decompose_result_mult.plot();   
    
    time_series = px.line(
        trend,  
        x='end_time',
        y='trend',
        color_discrete_sequence = px.colors.qualitative.Bold,
        title=str(dropdown_feature).capitalize() + " History (trends)",
        labels= {"end_time": "Time"}
        # hover_name = 'track_name',
        # hover_data = ['artist_name'] + measures
        )

    time_series.update_xaxes(rangeslider_visible=True)
    time_series.update_layout(hovermode="x",
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
    
    
    return time_series         
      
if __name__ == '__main__':
    app.run_server(debug=True)
 
