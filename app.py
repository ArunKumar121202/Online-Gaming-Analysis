# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Player Engagement Analysis", layout="wide")

# Load the dataset
data = pd.read_csv('online_gaming_behavior_dataset.csv')

# Sidebar
with st.sidebar:
    st.title("🎮 Filter Options")
    
    location_filter = st.multiselect(
        "Select Location:",
        options=data["Location"].unique(),
        default=data["Location"].unique()
    )

    genre_filter = st.multiselect(
        "Select Game Genre:",
        options=data["GameGenre"].unique(),
        default=data["GameGenre"].unique()
    )

    difficulty_filter = st.multiselect(
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

# Main Title
st.title("🎯 Player Engagement Dashboard")
st.markdown("Gain insights into player behavior, engagement, and game preferences.")

st.markdown("---")

# KPIs
st.subheader("🔹 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Players", filtered_data['PlayerID'].nunique())
with col2:
    st.metric("Avg Playtime (hrs)", f"{filtered_data['PlayTimeHours'].mean():.2f}")
with col3:
    st.metric("Avg Sessions/Week", f"{filtered_data['SessionsPerWeek'].mean():.1f}")
with col4:
    st.metric("Avg Player Level", f"{filtered_data['PlayerLevel'].mean():.1f}")

st.markdown("---")

# Charts section
st.subheader("📊 Visual Analysis")

# 1. Player Distribution by Game Genre
st.markdown("#### Player Distribution by Game Genre")
genre_counts = filtered_data["GameGenre"].value_counts().reset_index()
genre_counts.columns = ['GameGenre', 'Count']

genre_fig = px.bar(
    genre_counts,
    x='GameGenre',
    y='Count',
    color='GameGenre',
    title="Number of Players per Game Genre",
    text='Count'
)
genre_fig.update_layout(showlegend=False)
st.plotly_chart(genre_fig, use_container_width=True)

# 2. Engagement Level by Location
st.markdown("#### Engagement Level by Location")
engagement_fig = px.histogram(
    filtered_data,
    x="EngagementLevel",
    color="Location",
    barmode="group",
    title="Engagement Level Distribution Across Locations"
)
st.plotly_chart(engagement_fig, use_container_width=True)

# 3. Playtime vs Player Level
st.markdown("#### Playtime vs Player Level")
plt.figure(figsize=(10,6))
sns.scatterplot(data=filtered_data, x="PlayTimeHours", y="PlayerLevel", hue="Gender")
plt.xlabel("Playtime (Hours)")
plt.ylabel("Player Level")
plt.title("Playtime vs Player Level (Colored by Gender)")
st.pyplot(plt.gcf())

# 4. Average Session Duration Distribution
st.markdown("#### Average Session Duration Distribution")
plt.figure(figsize=(10,6))
sns.histplot(filtered_data["AvgSessionDurationMinutes"], kde=True, color="purple")
plt.xlabel("Avg Session Duration (Minutes)")
plt.title("Distribution of Average Session Duration")
st.pyplot(plt.gcf())

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")

