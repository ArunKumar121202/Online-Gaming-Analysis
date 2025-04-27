import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Online Gaming Analytics", layout="wide")

# Load the dataset
data = pd.read_csv('online_gaming_behavior_dataset.csv')

# Sidebar for section selection
st.sidebar.title("📂 Select Analysis Section")
section = st.sidebar.radio(
    "Go to",
    ("Player Demographics", "Game Behavior Metrics")
)

# Main Title
st.title("🎮 Online Gaming Behavior Dashboard")
st.markdown("Analyze player engagement, demographics, and gaming behavior.")

st.markdown("---")

# Section 1: Player Demographics
if section == "Player Demographics":
    st.header("👥 Player Demographics")

    # KPIs
    st.subheader("🔹 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Players", data['PlayerID'].nunique())
    with col2:
        st.metric("Avg Playtime (hrs)", f"{data['PlayTimeHours'].mean():.2f}")
    with col3:
        st.metric("Total Avg Sessions/Week", f"{data['SessionsPerWeek'].mean():.1f}")
    with col4:
        st.metric("Average Age", f"{data['Age'].mean():.1f}")
    with col5:
        st.metric("Age Range", f"{data['Age'].min()} - {data['Age'].max()} yrs")

    st.markdown("---")

    # Visual 1: Gender Distribution (Percentage)
    st.subheader("🔸 Percentage of Players by Gender")
    gender_counts = data['Gender'].value_counts(normalize=True) * 100
    gender_fig = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title="Gender Distribution (%)",
        hole=0.4
    )
    st.plotly_chart(gender_fig, use_container_width=True)

    # Visual 2: Players by Location
    st.subheader("🔸 Players Count by Location")
    location_counts = data['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'PlayerCount']
    location_fig = px.bar(
        location_counts,
        x='Location',
        y='PlayerCount',
        text='PlayerCount',
        title="Players by Location",
        color='Location'
    )
    location_fig.update_traces(textposition='outside')
    location_fig.update_layout(showlegend=False)
    st.plotly_chart(location_fig, use_container_width=True)

    # Visual 3: Players by Engagement Level
    st.subheader("🔸 Players by Engagement Level")
    engagement_counts = data['EngagementLevel'].value_counts().reset_index()
    engagement_counts.columns = ['EngagementLevel', 'PlayerCount']
    engagement_fig = px.bar(
        engagement_counts,
        x='EngagementLevel',
        y='PlayerCount',
        text='PlayerCount',
        title="Players by Engagement Level",
        color='EngagementLevel'
    )
    engagement_fig.update_traces(textposition='outside')
    engagement_fig.update_layout(showlegend=False)
    st.plotly_chart(engagement_fig, use_container_width=True)

    # Visual 4: Players by Game Difficulty
    st.subheader("🔸 Players by Game Difficulty Level")
    difficulty_counts = data['GameDifficulty'].value_counts().reset_index()
    difficulty_counts.columns = ['GameDifficulty', 'PlayerCount']
    difficulty_fig = px.bar(
        difficulty_counts,
        x='GameDifficulty',
        y='PlayerCount',
        text='PlayerCount',
        title="Players by Game Difficulty Level",
        color='GameDifficulty'
    )
    difficulty_fig.update_traces(textposition='outside')
    difficulty_fig.update_layout(showlegend=False)
    st.plotly_chart(difficulty_fig, use_container_width=True)

# Section 2: Game Behavior Metrics
elif section == "Game Behavior Metrics":
    st.header("🎯 Game Behavior Metrics")

    # Visual 1: Average Playtime Hours by Player Level
    st.subheader("🔸 Average Playtime Hours by Player Level")
    playtime_by_level = data.groupby('PlayerLevel')['PlayTimeHours'].mean().reset_index()
    playtime_level_fig = px.bar(
        playtime_by_level,
        x='PlayerLevel',
        y='PlayTimeHours',
        text='PlayTimeHours',
        title="Avg Playtime Hours by Player Level",
        color='PlayerLevel'
    )
    playtime_level_fig.update_traces(textposition='outside')
    playtime_level_fig.update_layout(showlegend=False)
    st.plotly_chart(playtime_level_fig, use_container_width=True)

    # Visual 2: Average Sessions/Week by Engagement Level and Age (Line Plot)
    st.subheader("🔸 Average Sessions/Week by Engagement Level and Age")
    sessions_by_engagement_age = data.groupby(['EngagementLevel', 'Age'])['SessionsPerWeek'].mean().reset_index()
    sessions_engagement_age_fig = px.line(
        sessions_by_engagement_age,
        x='Age',
        y='SessionsPerWeek',
        color='EngagementLevel',
        markers=True,
        title="Avg Sessions/Week by Engagement Level and Age"
    )
    st.plotly_chart(sessions_engagement_age_fig, use_container_width=True)

    # Visual 3: Average Achievements by Game Genre
    st.subheader("🔸 Average Achievements Unlocked by Game Genre")
    achievements_by_genre = data.groupby('GameGenre')['AchievementsUnlocked'].mean().reset_index()
    achievements_fig = px.bar(
        achievements_by_genre,
        x='GameGenre',
        y='AchievementsUnlocked',
        text='AchievementsUnlocked',
        title="Avg Achievements Unlocked by Game Genre",
        color='GameGenre'
    )
    achievements_fig.update_traces(textposition='outside')
    achievements_fig.update_layout(showlegend=False)
    st.plotly_chart(achievements_fig, use_container_width=True)

    # Visual 4: Average Session Duration Minutes by Difficulty Level
    st.subheader("🔸 Avg Session Duration Minutes by Game Difficulty Level")
    avg_session_duration = data.groupby('GameDifficulty')['AvgSessionDurationMinutes'].mean().reset_index()
    session_duration_fig = px.bar(
        avg_session_duration,
        x='GameDifficulty',
        y='AvgSessionDurationMinutes',
        text='AvgSessionDurationMinutes',
        title="Avg Session Duration by Game Difficulty",
        color='GameDifficulty'
    )
    session_duration_fig.update_traces(textposition='outside')
    session_duration_fig.update_layout(showlegend=False)
    st.plotly_chart(session_duration_fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")

