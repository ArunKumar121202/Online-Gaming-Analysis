import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Player Engagement Analysis", layout="wide")

# Load the dataset
data = pd.read_csv('player_data.csv')

# Sidebar filters
st.sidebar.header("Filter Options")
location_filter = st.sidebar.multiselect(
    "Select Location:",
    options=data["Location"].unique(),
    default=data["Location"].unique()
)

genre_filter = st.sidebar.multiselect(
    "Select Game Genre:",
    options=data["GameGenre"].unique(),
    default=data["GameGenre"].unique()
)

difficulty_filter = st.sidebar.multiselect(
    "Select Game Difficulty:",
    options=data["GameDifficulty"].unique(),
    default=data["GameDifficulty"].unique()
)

# Apply Filters
filtered_data = data[
    (data["Location"].isin(location_filter)) &
    (data["GameGenre"].isin(genre_filter)) &
    (data["GameDifficulty"].isin(difficulty_filter))
]

# Title
st.title("🎮 Player Engagement Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Players", filtered_data['PlayerID'].nunique())
with col2:
    st.metric("Average Playtime (hrs)", f"{filtered_data['PlayTimeHours'].mean():.2f}")
with col3:
    st.metric("Average Sessions/Week", f"{filtered_data['SessionsPerWeek'].mean():.1f}")
with col4:
    st.metric("Average Player Level", f"{filtered_data['PlayerLevel'].mean():.1f}")

st.markdown("---")

# Charts section
st.subheader("Player Distribution by Game Genre")
genre_fig = px.bar(
    filtered_data["GameGenre"].value_counts().reset_index(),
    x='index',
    y='GameGenre',
    labels={'index': 'Game Genre', 'GameGenre': 'Number of Players'},
    color='index',
    title="Players per Game Genre"
)
st.plotly_chart(genre_fig, use_container_width=True)

st.subheader("Engagement Level by Location")
engagement_fig = px.histogram(
    filtered_data,
    x="EngagementLevel",
    color="Location",
    barmode="group",
    title="Engagement Level Distribution by Location"
)
st.plotly_chart(engagement_fig, use_container_width=True)

st.subheader("Playtime vs. Player Level")
plt.figure(figsize=(10,6))
sns.scatterplot(data=filtered_data, x="PlayTimeHours", y="PlayerLevel", hue="Gender")
st.pyplot(plt.gcf())

st.subheader("Average Session Duration Distribution")
plt.figure(figsize=(10,6))
sns.histplot(filtered_data["AvgSessionDurationMinutes"], kde=True, color="purple")
st.pyplot(plt.gcf())

