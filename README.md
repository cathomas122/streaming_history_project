# streaming_history_project
A simple analysis &amp; visualization of the valence, energy, mode, danceability, key, and tempo of a year's worth of my Spotify streaming history.

## Accessing the dashboard
1. Run create_dashboard.py in order to generate the local address in which Dash will run.
2. Copy the generated address into a web browser (ie. Google Chrome) in order to see the dashboard

## Using the dashboard
Since this dashboard is not ready for full production/deployment, there are only three features:
1. The "Average Values of Track Features Across All Streaming History" graph demonstrates the average value of each specified feature across the year's worth of streaming history.
2. The "Top 15 Songs in Selected Period" display the top 15 most frequently-listened to songs from the past year.
3. The time series allows the user to select a feature and see how the value of that feature has changed over time. If they are curious about a particular time period, they may select the times that they wish to examine in more detail. 

## Future analysis 
1. Identify which features/combination of features would be the best predictor for how many times a song is listened to.
2. Update the "Average Values of Track Features Across All Streaming History" and "Top 15 Songs in Selected Period" graphs accordingly, depending on what the user selects on the time series graph. 
3. Add a scatter plot for each feature that identifies the actual song and its valence, depending on the time period selected in the time series graph
4. Create a collage of album art for each period of time
