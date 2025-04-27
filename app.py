import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Online Gaming Analysis", layout="wide")

# Load the dataset
data = pd.read_csv('online_gaming_behavior_dataset.csv')

# Sidebar for Section Selection
with st.sidebar:
    st.title("🎮 Choose Section")
    section = st.radio("Select Section:", [
        "Player Demographics",
        "Game Behavior Metrics"
    ])

# Section 1: Player Demographics
if section == "Player Demographics":
    st.title("👥 Player Demographics")
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", f"{data['PlayerID'].nunique()}")
    with col2:
        st.metric("Avg Playtime (hrs)", f"{data['PlayTimeHours'].mean():.2f}")
    with col3:
        st.metric("Total Sessions/Week", f"{data['SessionsPerWeek'].sum():.2f}")
    with col4:
        st.metric("Avg Age", f"{data['Age'].mean():.2f}")

    col5, col6 = st.columns(2)
    with col5:
        st.metric("Youngest Player Age", f"{data['Age'].min():.2f}")
    with col6:
        st.metric("Oldest Player Age", f"{data['Age'].max():.2f}")

    st.markdown("---")

    # 1. Percentage of Players by Gender
    st.markdown("#### Percentage of Players by Gender")
    gender_counts = data['Gender'].value_counts(normalize=True).reset_index()
    gender_counts.columns = ['Gender', 'Percentage']
    gender_counts['PercentageFormatted'] = gender_counts['Percentage'].apply(lambda x: f"{x*100:.2f}%")

    gender_fig = px.pie(
        gender_counts,
        names='Gender',
        values='Percentage',
        title="Player Distribution by Gender",
        hole=0.4
    )
    gender_fig.update_traces(textinfo='percent+label')
    st.plotly_chart(gender_fig, use_container_width=True)

    # 2. Count of Players by Location
    st.markdown("#### Count of Players by Location")
    location_counts = data['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Count']
    location_counts['CountFormatted'] = location_counts['Count'].apply(lambda x: f"{x:.2f}")

    location_fig = px.bar(
        location_counts,
        x='Location',
        y='Count',
        text='CountFormatted',
        title="Player Count by Location",
        color='Location'
    )
    location_fig.update_layout(showlegend=False)
    st.plotly_chart(location_fig, use_container_width=True)

    # 3. Count of Players by Engagement Level
    st.markdown("#### Count of Players by Engagement Level")
    engagement_counts = data['EngagementLevel'].value_counts().reset_index()
    engagement_counts.columns = ['EngagementLevel', 'Count']
    engagement_counts['CountFormatted'] = engagement_counts['Count'].apply(lambda x: f"{x:.2f}")

    engagement_fig = px.bar(
        engagement_counts,
        x='EngagementLevel',
        y='Count',
        text='CountFormatted',
        title="Player Count by Engagement Level",
        color='EngagementLevel'
    )
    engagement_fig.update_layout(showlegend=False)
    st.plotly_chart(engagement_fig, use_container_width=True)

    # 4. Count of Players by Game Difficulty
    st.markdown("#### Count of Players by Game Difficulty")
    difficulty_counts = data['GameDifficulty'].value_counts().reset_index()
    difficulty_counts.columns = ['GameDifficulty', 'Count']
    difficulty_counts['CountFormatted'] = difficulty_counts['Count'].apply(lambda x: f"{x:.2f}")

    difficulty_fig = px.bar(
        difficulty_counts,
        x='GameDifficulty',
        y='Count',
        text='CountFormatted',
        title="Player Count by Game Difficulty",
        color='GameDifficulty'
    )
    difficulty_fig.update_layout(showlegend=False)
    st.plotly_chart(difficulty_fig, use_container_width=True)

# Section 2: Game Behavior Metrics
elif section == "Game Behavior Metrics":
    st.title("🎮 Game Behavior Metrics")
    st.markdown("---")

    # 1. Average Playtime Hours by Player Level
    st.markdown("#### Average Playtime Hours by Player Level")
    avg_playtime_level = data.groupby('PlayerLevel')['PlayTimeHours'].mean().reset_index()
    avg_playtime_level['PlayTimeHoursFormatted'] = avg_playtime_level['PlayTimeHours'].apply(lambda x: f"{x:.2f}")

    playtime_fig = px.bar(
        avg_playtime_level,
        x='PlayerLevel',
        y='PlayTimeHours',
        text='PlayTimeHoursFormatted',
        title="Avg Playtime Hours by Player Level",
        color='PlayerLevel'
    )
    playtime_fig.update_layout(showlegend=False)
    st.plotly_chart(playtime_fig, use_container_width=True)

    # 2. Average Sessions/Week by Engagement Level and Age (Line Chart)
    st.markdown("#### Average Sessions/Week by Engagement Level and Age")
    sessions_by_engagement_age = data.groupby(['EngagementLevel', 'Age'])['SessionsPerWeek'].mean().reset_index()
    sessions_by_engagement_age['SessionsPerWeekFormatted'] = sessions_by_engagement_age['SessionsPerWeek'].apply(lambda x: f"{x:.2f}")

    sessions_fig = px.line(
        sessions_by_engagement_age,
        x='Age',
        y='SessionsPerWeek',
        color='EngagementLevel',
        title="Avg Sessions/Week by Engagement Level and Age"
    )
    st.plotly_chart(sessions_fig, use_container_width=True)

    # 3. Avg Achievements by Game Genre
    st.markdown("#### Avg Achievements by Game Genre")
    achievements_by_genre = data.groupby('GameGenre')['AchievementsUnlocked'].mean().reset_index()
    achievements_by_genre['AchievementsUnlockedFormatted'] = achievements_by_genre['AchievementsUnlocked'].apply(lambda x: f"{x:.2f}")

    achievements_fig = px.bar(
        achievements_by_genre,
        x='GameGenre',
        y='AchievementsUnlocked',
        text='AchievementsUnlockedFormatted',
        title="Avg Achievements Unlocked by Game Genre",
        color='GameGenre'
    )
    achievements_fig.update_layout(showlegend=False)
    st.plotly_chart(achievements_fig, use_container_width=True)

    # 4. Average Session Duration Minutes by Difficulty
    st.markdown("#### Avg Session Duration by Difficulty Level")
    avg_session_duration = data.groupby('GameDifficulty')['AvgSessionDurationMinutes'].mean().reset_index()
    avg_session_duration['AvgSessionDurationFormatted'] = avg_session_duration['AvgSessionDurationMinutes'].apply(lambda x: f"{x:.2f}")

    session_duration_fig = px.bar(
        avg_session_duration,
        x='GameDifficulty',
        y='AvgSessionDurationMinutes',
        text='AvgSessionDurationFormatted',
        title="Avg Session Duration by Game Difficulty",
        color='GameDifficulty'
    )
    session_duration_fig.update_layout(showlegend=False)
    st.plotly_chart(session_duration_fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
