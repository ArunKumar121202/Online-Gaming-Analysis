import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Online Gaming Analysis", layout="wide")

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

### Section 1: Player Demographics

st.header("📊 **Player Demographics**")

# KPIs
st.subheader("🔹 Key Metrics")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Players", filtered_data['PlayerID'].nunique())
with col2:
    st.metric("Avg Playtime (hrs)", f"{filtered_data['PlayTimeHours'].mean():.2f}")
with col3:
    st.metric("Avg Sessions/Week", f"{filtered_data['SessionsPerWeek'].mean():.1f}")
with col4:
    st.metric("Avg Age", f"{filtered_data['Age'].mean():.1f}")
with col5:
    st.metric("Age Range", f"{filtered_data['Age'].min()} - {filtered_data['Age'].max()}")
with col6:
    st.metric("Avg Player Level", f"{filtered_data['PlayerLevel'].mean():.1f}")

# Visualizations
st.subheader("📊 Visual Analysis")

# 1. Percentage of Players by Gender
st.markdown("#### Percentage of Players by Gender")
gender_counts = filtered_data["Gender"].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']
gender_counts['Percentage'] = (gender_counts['Count'] / gender_counts['Count'].sum()) * 100

gender_fig = px.pie(
    gender_counts, 
    names='Gender', 
    values='Percentage', 
    title="Percentage of Players by Gender"
)
st.plotly_chart(gender_fig, use_container_width=True)

# 2. Count of Players by Location
st.markdown("#### Count of Players by Location")
location_counts = filtered_data["Location"].value_counts().reset_index()
location_counts.columns = ['Location', 'Count']

location_fig = px.bar(
    location_counts,
    x='Location',
    y='Count',
    color='Location',
    title="Count of Players by Location",
    text='Count'
)
st.plotly_chart(location_fig, use_container_width=True)

# 3. Count of Players by Engagement Level
st.markdown("#### Count of Players by Engagement Level")
engagement_counts = filtered_data["EngagementLevel"].value_counts().reset_index()
engagement_counts.columns = ['EngagementLevel', 'Count']

engagement_fig = px.bar(
    engagement_counts,
    x='EngagementLevel',
    y='Count',
    color='EngagementLevel',
    title="Count of Players by Engagement Level",
    text='Count'
)
st.plotly_chart(engagement_fig, use_container_width=True)

# 4. Count of Players by Game Difficulty Level
st.markdown("#### Count of Players by Game Difficulty Level")
difficulty_counts = filtered_data["GameDifficulty"].value_counts().reset_index()
difficulty_counts.columns = ['GameDifficulty', 'Count']

difficulty_fig = px.bar(
    difficulty_counts,
    x='GameDifficulty',
    y='Count',
    color='GameDifficulty',
    title="Count of Players by Game Difficulty Level",
    text='Count'
)
st.plotly_chart(difficulty_fig, use_container_width=True)

st.markdown("---")

### Section 2: Game Behavior KPIs

st.header("📊 **Game Behavior KPIs**")

# Visualizations
st.subheader("📊 Visual Analysis")

# 1. Average Playtime Hours by Player Level
st.markdown("#### Average Playtime Hours by Player Level")
playtime_by_level = filtered_data.groupby('PlayerLevel')['PlayTimeHours'].mean().reset_index()

playtime_level_fig = px.line(
    playtime_by_level,
    x='PlayerLevel',
    y='PlayTimeHours',
    title="Average Playtime Hours by Player Level"
)
st.plotly_chart(playtime_level_fig, use_container_width=True)

# 2. Average Sessions/Week by Engagement Level and Age
st.markdown("#### Average Sessions/Week by Engagement Level and Age")
sessions_by_engagement_age = filtered_data.groupby(['EngagementLevel', 'Age'])['SessionsPerWeek'].mean().reset_index()

sessions_engagement_age_fig = px.line(
    sessions_by_engagement_age,
    x='Age',
    y='SessionsPerWeek',
    color='EngagementLevel',
    title="Average Sessions/Week by Engagement Level and Age"
)
st.plotly_chart(sessions_engagement_age_fig, use_container_width=True)

# 3. Achievements Unlocked by Game Genre
st.markdown("#### Achievements Unlocked by Game Genre")
achievements_by_genre = filtered_data.groupby('GameGenre')['AchievementsUnlocked'].sum().reset_index()

achievements_genre_fig = px.bar(
    achievements_by_genre,
    x='GameGenre',
    y='AchievementsUnlocked',
    color='GameGenre',
    title="Achievements Unlocked by Game Genre",
    text='AchievementsUnlocked'
)
st.plotly_chart(achievements_genre_fig, use_container_width=True)

# 4. Average Session Duration by Difficulty Level
st.markdown("#### Average Session Duration by Difficulty Level")
session_duration_by_difficulty = filtered_data.groupby('GameDifficulty')['AvgSessionDurationMinutes'].mean().reset_index()

session_duration_diff_fig = px.bar(
    session_duration_by_difficulty,
    x='GameDifficulty',
    y='AvgSessionDurationMinutes',
    color='GameDifficulty',
    title="Average Session Duration by Difficulty Level"
)
st.plotly_chart(session_duration_diff_fig, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
