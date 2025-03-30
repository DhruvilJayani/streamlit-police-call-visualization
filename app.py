import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.cloud import bigquery
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/warm-now-452506-m5-e01671b38c39.json"


client = bigquery.Client()

query_params = st.experimental_get_query_params()
filter_type = query_params.get("filter", [""])[0]
filter_value = query_params.get("value", [""])[0]


query = "SELECT * FROM `warm-now-452506-m5.police_call.police-call-2023`"
df = client.query(query).to_dataframe()


df['START_DATE'] = pd.to_datetime(df['START_DATE'], errors='coerce')
df['MONTH'] = df['START_DATE'].dt.month


priority_options = ['All'] + df['PRIORITY'].unique().tolist() 
selected_priority = st.sidebar.selectbox("Select Priority Level", priority_options)


final_dispo_options = ['All'] + df['FINAL_DISPO'].unique().tolist()
selected_final_dispo = st.sidebar.selectbox("Select Final Disposition", final_dispo_options)


if selected_priority == 'All' and selected_final_dispo == 'All':
    filtered_df = df  
elif selected_priority == 'All':
    filtered_df = df[df['FINAL_DISPO'] == selected_final_dispo]
elif selected_final_dispo == 'All':
    filtered_df = df[df['PRIORITY'] == selected_priority]
else:
    filtered_df = df[(df['PRIORITY'] == selected_priority) & (df['FINAL_DISPO'] == selected_final_dispo)]


crime_trend = filtered_df.groupby("MONTH")["CALL_NUMBER"].count()


plt.figure(figsize=(10, 5))
crime_trend.plot(kind="line", marker='o', color="blue")
plt.xlabel("Month")
plt.ylabel("Number of Incidents")
plt.title(f"Crime Trends Over the Months (Priority: {selected_priority}, Final Disposition: {selected_final_dispo})")
plt.grid(True)


st.pyplot(plt)
