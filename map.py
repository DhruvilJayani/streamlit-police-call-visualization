import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from google.cloud import bigquery
import os
from io import BytesIO

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/warm-now-452506-m5-e01671b38c39.json"


project_id = "warm-now-452506-m5"
client = bigquery.Client(project=project_id)


query = """
SELECT * FROM `warm-now-452506-m5.police_call.police_call_lat_long`
""" 

query_job = client.query(query)
df_location = query_job.to_dataframe()


map_center = [37.3382, -121.8863]
mymap = folium.Map(location=map_center, zoom_start=12)


offense_types = df_location['CALL_TYPE'].unique().tolist() 
selected_offense_type = st.selectbox('Select Offense Type', ['All'] + offense_types) 


if selected_offense_type != 'All':
    filtered_df = df_location[df_location['CALL_TYPE'] == selected_offense_type]
else:
    filtered_df = df_location


marker_cluster = MarkerCluster().add_to(mymap)


for _, row in filtered_df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Call Type: {row['CALL_TYPE']}<br>Date: {row['START_DATE']}",
        ).add_to(marker_cluster)


map_file = "police_call_map.html"
mymap.save(map_file)


with open(map_file, 'r') as f:
    map_html = f.read()
    st.components.v1.html(map_html, height=600)


# streamlit run map.py --server.port 8502
