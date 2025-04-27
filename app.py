import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Online Gaming Analysis", layout="wide")

# Load the dataset
data = pd.read_csv('online_gaming_behavior_dataset.csv')

# Sidebar: Select Sections
with st.sidebar:
    st.title("🎮 Choose Section")
    
    section = st.radio(
        "Select Section to Explore:",
        options=["Player Demographics", "Game Behavior KPIs"]
    )

# Main Title
st.title("🎯 Player Engagement Dashboard")
st.markdown("Gain insights into player behavior, engagement, and game preferences.")

st.markdown("---")

### Section 1: Player Demographics
if section == "Player Demographics":
    st.header("📊 **Player Demographics**")

    # KPIs
    st.subheader("🔹 Key Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Players", data['PlayerID'].nunique())
    with col2:
        st.metric("Avg Playtime (hrs)", f"{data['PlayTimeHours'].mean():.2f}")
    with col3:
        st.metric("Avg Sessions/Week", f"{data['SessionsPerWeek'].mean():.1f}")
    with col4:
        st.metric("Avg Age", f"{data['Age'].mean():.1f}")
    with col5:
        st.metric("Age Range", f"{data['Age'].min()} - {data['Age'].max()}")
    with col6:
        st.metric("Avg Player Level", f"{data['PlayerLevel'].mean():.1f}")

    # Visualizations
    st.subheader("📊 Visual Analysis")

    # 1. Percentage of Players by Gender
    st.markdown("#### Percentage of Players by Gender")
    gender_counts = data["Gender"].value_counts().reset_index()
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
    location_counts = data["Location"].value_counts().reset_index()
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
    engagement_counts = data["EngagementLevel"].value_counts().reset_index()
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
    difficulty_counts = data["GameDifficulty"].value_counts().reset_index()
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
if section == "Game Behavior KPIs":
    st.header("📊 **Game Behavior KPIs**")

    # KPIs
    st.subheader("🔹 Key Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Avg Achievements per Player", f"{data['AchievementsUnlocked'].mean():.2f}")
    with col2:
        st.metric("Avg Playtime per Genre (hrs)", f"{data.groupby('GameGenre')['PlayTimeHours'].mean().mean():.2f}")
    with col3:
        st.metric("Avg Sessions per Player", f"{data['SessionsPerWeek'].mean():.2f}")
    with col4:
        st.metric("Avg Session Duration (mins)", f"{data['AvgSessionDurationMinutes'].mean():.1f}")
    with col5:
        st.metric("Percentage of Players Unlocking Achievements", f"{(data['AchievementsUnlocked'] > 0).mean() * 100:.1f}%")
    with col6:
        st.metric("Avg Player Level", f"{data['PlayerLevel'].mean():.1f}")

    # Visualizations
    st.subheader("📊 Visual Analysis")

    # 1. Average Playtime Hours by Game Genre
    st.markdown("#### Average Playtime Hours by Game Genre")
    playtime_by_genre = data.groupby('GameGenre')['PlayTimeHours'].mean().reset_index()

    playtime_genre_fig = px.bar(
        playtime_by_genre,
        x='GameGenre',
        y='PlayTimeHours',
        color='GameGenre',
        title="Average Playtime Hours by Game Genre"
    )
    st.plotly_chart(playtime_genre_fig, use_container_width=True)

    # 2. Average Sessions/Week by Engagement Level and Age
    st.markdown("#### Average Sessions/Week by Engagement Level and Age")
    sessions_by_engagement_age = data.groupby(['EngagementLevel', 'Age'])['SessionsPerWeek'].mean().reset_index()
    
    sessions_engagement_age_fig = px.line(
        sessions_by_engagement_age,
        x='Age',
        y='SessionsPerWeek',
        color='EngagementLevel',
        markers=True,  # shows points on the lines too
        title="Average Sessions/Week by Engagement Level and Age"
    )
    st.plotly_chart(sessions_engagement_age_fig, use_container_width=True)


    # 3. Achievements Unlocked by Game Genre
    st.markdown("#### Achievements Unlocked by Game Genre")
    achievements_by_genre = data.groupby('GameGenre')['AchievementsUnlocked'].sum().reset_index()

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
    session_duration_by_difficulty = data.groupby('GameDifficulty')['AvgSessionDurationMinutes'].mean().reset_index()

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
