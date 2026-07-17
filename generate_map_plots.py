import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")
spacex_df = df[['LaunchSite', 'Latitude', 'Longitude', 'Class']]

# 1. Slide 35: All launch sites
site_map_df = spacex_df.groupby(['LaunchSite', 'Latitude', 'Longitude']).size().reset_index(name='class')
fig1 = px.scatter_mapbox(site_map_df, lat="Latitude", lon="Longitude", hover_name="LaunchSite", 
                         color_discrete_sequence=["blue"], zoom=4, height=600)
fig1.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
fig1.write_image("plots/map_all_sites.png")

# 2. Slide 36: Color-labeled launch outcomes on the map
colors = ['red' if c == 0 else 'green' for c in spacex_df['Class']]
fig2 = px.scatter_mapbox(spacex_df, lat="Latitude", lon="Longitude", hover_name="LaunchSite", 
                         color=colors, color_discrete_map="identity", zoom=4, height=600)
fig2.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
fig2.write_image("plots/map_colored_outcomes.png")

# 3. Slide 37: Selected launch site proximities
# KSC LC 39A: 28.573255, -80.646895
# Coastline approximate: 28.56367, -80.57163 (example)
lat1, lon1 = 28.573255, -80.646895
lat2, lon2 = 28.56367, -80.57163
fig3 = go.Figure(go.Scattermapbox(
    lat=[lat1, lat2],
    lon=[lon1, lon2],
    mode='markers+lines',
    marker=go.scattermapbox.Marker(size=9, color='red'),
    line=go.scattermapbox.Line(width=2, color='blue')
))
fig3.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=dict(lat=28.57, lon=-80.6), zoom=12),
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig3.write_image("plots/map_proximity.png")

print("Map plots generated.")
