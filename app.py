import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Online Gaming Analytics", layout="wide")

# Dummy credentials (replace or secure appropriately)
VALID_USERNAME = "Arun Kumar"
VALID_PASSWORD = "Loginpage@123"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    st.title("🔐 Login Page")
    st.markdown("Please enter your credentials to access the dashboard.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Show login page if not logged in
if not st.session_state.logged_in:
    login()
    st.stop()
# Load the dataset
data = pd.read_csv('online_gaming_behavior_dataset.csv')

# Sidebar for section selection
st.sidebar.title("📂 Select Analysis Section")
section = st.sidebar.radio(
    "Go to",
    ("Player Demographics", "Game Behavior Metrics", "Purchase Behavior Analysis", "Engagement, Relationship & Performance Analysis")
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
# Main Title
st.title("🎮 Online Gaming Behavior Dashboard")
st.markdown("Analyze player engagement, demographics, and gaming behavior.")
st.markdown("---")

# Section 1: Player Demographics
if section == "Player Demographics":
    st.header("👥 Player Demographics")

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 Key KPIs", "📈 Analysis"])

    with tab1:
        st.subheader("🔹 Key KPIs")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Players", data['PlayerID'].nunique())
        with col2:
            st.metric("Avg Playtime (hrs)", f"{data['PlayTimeHours'].mean():.2f}")
        with col3:
            st.metric("Avg Sessions/Week", f"{data['SessionsPerWeek'].mean():.2f}")
        with col4:
            st.metric("Average Age", f"{data['Age'].mean():.2f}")
        with col5:
            st.metric("Age Range", f"{data['Age'].min()} - {data['Age'].max()} yrs")

    with tab2:
        st.subheader("🔸 Percentage of Players by Gender")
        gender_counts = data['Gender'].value_counts(normalize=True) * 100
        gender_fig = px.pie(
            names=gender_counts.index,
            values=gender_counts.values,
            title="Gender Distribution (%)",
            hole=0.4
        )
        st.plotly_chart(gender_fig, use_container_width=True)

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
        location_fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        location_fig.update_layout(showlegend=False)
        st.plotly_chart(location_fig, use_container_width=True)

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
        engagement_fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        engagement_fig.update_layout(showlegend=False)
        st.plotly_chart(engagement_fig, use_container_width=True)

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
        difficulty_fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        difficulty_fig.update_layout(showlegend=False)
        st.plotly_chart(difficulty_fig, use_container_width=True)

# Section 2: Game Behavior Metrics
elif section == "Game Behavior Metrics":
    st.header("🎯 Game Behavior Metrics")

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 Key KPIs", "📈 Analysis"])

    with tab1:
        st.subheader("🔹 Key KPIs")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Playtime (hrs)", f"{data['PlayTimeHours'].mean():.2f}")
        with col2:
            st.metric("Avg Sessions/Week", f"{data['SessionsPerWeek'].mean():.2f}")
        with col3:
            st.metric("Avg Achievements Unlocked", f"{data['AchievementsUnlocked'].mean():.2f}")
        with col4:
            min_achievements = data['AchievementsUnlocked'].min()
            max_achievements = data['AchievementsUnlocked'].max()
            st.metric("Achievements Range", f"{min_achievements} - {max_achievements}")

    with tab2:
        st.subheader("🔸 Average Playtime Hours by Player Level")
        playtime_by_level = data.groupby('PlayerLevel')['PlayTimeHours'].mean().reset_index()
        playtime_by_level['PlayTimeHours'] = playtime_by_level['PlayTimeHours'].round(2)
        playtime_level_fig = px.bar(
            playtime_by_level,
            x='PlayerLevel',
            y='PlayTimeHours',
            text='PlayTimeHours',
            title="Avg Playtime Hours by Player Level",
            color='PlayerLevel'
        )
        playtime_level_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        playtime_level_fig.update_layout(showlegend=False)
        st.plotly_chart(playtime_level_fig, use_container_width=True)

        st.subheader("🔸 Average Sessions/Week by Engagement Level and Age")
        sessions_by_engagement_age = data.groupby(['EngagementLevel', 'Age'])['SessionsPerWeek'].mean().reset_index()
        sessions_by_engagement_age['SessionsPerWeek'] = sessions_by_engagement_age['SessionsPerWeek'].round(2)
        sessions_engagement_age_fig = px.line(
            sessions_by_engagement_age,
            x='Age',
            y='SessionsPerWeek',
            color='EngagementLevel',
            markers=True,
            title="Avg Sessions/Week by Engagement Level and Age"
        )
        st.plotly_chart(sessions_engagement_age_fig, use_container_width=True)

        st.subheader("🔸 Average Achievements Unlocked by Game Genre")
        achievements_by_genre = data.groupby('GameGenre')['AchievementsUnlocked'].mean().reset_index()
        achievements_by_genre['AchievementsUnlocked'] = achievements_by_genre['AchievementsUnlocked'].round(2)
        achievements_fig = px.pie(
            achievements_by_genre,
            names='GameGenre',
            values='AchievementsUnlocked',
            title="Avg Achievements Unlocked by Game Genre",
            hole=0.5
        )
        achievements_fig.update_traces(textposition='inside', texttemplate='%{label}: %{value:.2f}')
        st.plotly_chart(achievements_fig, use_container_width=True)

        st.subheader("🔸 Avg Session Duration Minutes by Game Difficulty Level")
        avg_session_duration = data.groupby('GameDifficulty')['AvgSessionDurationMinutes'].mean().reset_index()
        avg_session_duration['AvgSessionDurationMinutes'] = avg_session_duration['AvgSessionDurationMinutes'].round(2)
        session_duration_fig = px.bar(
            avg_session_duration,
            y='GameDifficulty',
            x='AvgSessionDurationMinutes',
            orientation='h',
            text='AvgSessionDurationMinutes',
            title="Avg Session Duration by Game Difficulty",
            color='GameDifficulty'
        )
        session_duration_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        session_duration_fig.update_layout(showlegend=False)
        st.plotly_chart(session_duration_fig, use_container_width=True)

        st.subheader("🔸 Average Player Count by Player Level")
        player_count_by_level = data['PlayerLevel'].value_counts().reset_index()
        player_count_by_level.columns = ['PlayerLevel', 'PlayerCount']
        player_count_fig = px.bar(
            player_count_by_level,
            x='PlayerLevel',
            y='PlayerCount',
            text='PlayerCount',
            title="Average Player Count by Player Level",
            color='PlayerLevel'
        )
        player_count_fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        player_count_fig.update_layout(showlegend=False)
        st.plotly_chart(player_count_fig, use_container_width=True)
        
# Purchase Behavior Analysis Section
elif section == "Purchase Behavior Analysis":
    st.header("💰 Purchase Behavior Analysis")

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 Key KPIs", "📈 Analysis"])

    with tab1:
        st.subheader("🔹 Key Performance Indicators")

        # Calculate values
        total_players = data.shape[0]
        purchasers = data[data['InGamePurchases'] == 1].shape[0]
        non_purchasers = data[data['InGamePurchases'] == 0].shape[0]
        purchase_rate = (purchasers / total_players) * 100
        non_purchase_rate = (non_purchasers / total_players) * 100

        # Purchase Rate by Gender
        purchase_by_gender = data.groupby('Gender')['InGamePurchases'].mean() * 100

        # KPI Layout
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Purchasers", purchasers)
        with col2:
            st.metric("Non-Purchasers", non_purchasers)
        with col3:
            st.metric("Purchase Rate", f"{purchase_rate:.2f}%")
        with col4:
            st.metric("Non-Purchase Rate", f"{non_purchase_rate:.2f}%")
        with col5:
            male_rate = purchase_by_gender.get('Male', 0)
            female_rate = purchase_by_gender.get('Female', 0)
            st.metric("Male Purchase Rate", f"{male_rate:.2f}%")
            st.metric("Female Purchase Rate", f"{female_rate:.2f}%")

    with tab2:
        st.subheader("🔸 Purchasers vs Non-Purchasers")
        purchase_status_counts = data['InGamePurchases'].value_counts().reset_index()
        purchase_status_counts.columns = ['PurchaseStatus', 'Count']
        purchase_status_counts['PurchaseStatus'] = purchase_status_counts['PurchaseStatus'].replace({1: 'Purchaser', 0: 'Non-Purchaser'})

        fig_purchase_status = px.pie(
            purchase_status_counts,
            names='PurchaseStatus',
            values='Count',
            title="Purchasers vs Non-Purchasers",
            hole=0.4
        )
        st.plotly_chart(fig_purchase_status, use_container_width=True)

        st.subheader("🔸 Purchasers by Location")
        purchasers_location = data[data['InGamePurchases'] == 1]['Location'].value_counts().reset_index()
        purchasers_location.columns = ['Location', 'Purchasers']

        fig_location = px.bar(
            purchasers_location,
            x='Location',
            y='Purchasers',
            color='Location',
            text='Purchasers',
            title="Purchasers by Location"
        )
        fig_location.update_traces(texttemplate='%{text}', textposition='outside')
        fig_location.update_layout(showlegend=False)
        st.plotly_chart(fig_location, use_container_width=True)

        st.subheader("🔸 Purchasers by Game Genre")
        purchasers_genre = data[data['InGamePurchases'] == 1]['GameGenre'].value_counts().reset_index()
        purchasers_genre.columns = ['GameGenre', 'Purchasers']

        fig_genre = px.bar(
            purchasers_genre,
            x='GameGenre',
            y='Purchasers',
            color='GameGenre',
            text='Purchasers',
            title="Purchasers by Game Genre"
        )
        fig_genre.update_traces(texttemplate='%{text}', textposition='outside')
        fig_genre.update_layout(showlegend=False)
        st.plotly_chart(fig_genre, use_container_width=True)

        st.subheader("🔸 Purchasers by Game Difficulty Level")
        purchasers_difficulty = data[data['InGamePurchases'] == 1]['GameDifficulty'].value_counts().reset_index()
        purchasers_difficulty.columns = ['GameDifficulty', 'Purchasers']

        fig_difficulty = px.bar(
            purchasers_difficulty,
            x='GameDifficulty',
            y='Purchasers',
            color='GameDifficulty',
            text='Purchasers',
            title="Purchasers by Game Difficulty"
        )
        fig_difficulty.update_traces(texttemplate='%{text}', textposition='outside')
        fig_difficulty.update_layout(showlegend=False)
        st.plotly_chart(fig_difficulty, use_container_width=True)

        st.subheader("🔸 Purchasers vs Non-Purchasers by Engagement Level")
        purchasers_engagement = data.groupby(['EngagementLevel', 'InGamePurchases']).size().reset_index(name='Count')
        purchasers_engagement['PurchaseStatus'] = purchasers_engagement['InGamePurchases'].replace({1: 'Purchaser', 0: 'Non-Purchaser'})

        fig_engagement = px.bar(
            purchasers_engagement,
            x='EngagementLevel',
            y='Count',
            color='PurchaseStatus',
            barmode='group',
            text='Count',
            title="Purchasers vs Non-Purchasers by Engagement Level"
        )
        fig_engagement.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig_engagement, use_container_width=True)

        st.subheader("🔸 Purchasers by Age (Bins)")
        # Purchasers by Age (Bins)
        bins = [14, 19, 24, 29, 34, 39, 44, 49]
        labels = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49']
        data['AgeGroup'] = pd.cut(data['Age'], bins=bins, labels=labels, right=True)
        
        purchasers_age_bins = data[data['InGamePurchases'] == 1]['AgeGroup'].value_counts().sort_index().reset_index()
        purchasers_age_bins.columns = ['AgeGroup', 'PurchaserCount']
        
        fig_age_bins = px.bar(
            purchasers_age_bins,
            x='AgeGroup',
            y='PurchaserCount',
            text='PurchaserCount',
            title="Purchasers by Age Group",
            color='AgeGroup'
        )
        fig_age_bins.update_traces(texttemplate='%{text}', textposition='outside')
        fig_age_bins.update_layout(showlegend=False)
        st.plotly_chart(fig_age_bins, use_container_width=True)


elif section == "Engagement, Relationship & Performance Analysis":
    st.header("🎯 Engagement, Relationship & Performance Analysis")

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 KPIs", "📈 Analysis"])

    with tab1:
        st.subheader("🔹 Engagement, Relationship & Performance KPIs")

        engagement_counts = data['EngagementLevel'].value_counts(normalize=True) * 100
        avg_achievements = data['AchievementsUnlocked'].mean()
        avg_player_level = data['PlayerLevel'].mean()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("High Engagement %", f"{engagement_counts.get('High', 0):.1f}%")
        col2.metric("Medium Engagement %", f"{engagement_counts.get('Medium', 0):.1f}%")
        col3.metric("Low Engagement %", f"{engagement_counts.get('Low', 0):.1f}%")
        col4.metric("Avg Achievements", f"{avg_achievements:.1f}")
        col5.metric("Avg Player Level", f"{avg_player_level:.1f}")

    with tab2:
        st.subheader("🔸 Engagement & Performance Analysis")

        # Boxplots: Good for understanding distribution across categories
        st.plotly_chart(
            px.box(data, x='EngagementLevel', y='SessionsPerWeek', title="Sessions per Week by Engagement Level"),
            use_container_width=True
        )
        st.plotly_chart(
            px.box(data, x='EngagementLevel', y='PlayTimeHours', title="Playtime Hours by Engagement Level"),
            use_container_width=True
        )

        # Histogram: Still useful for seeing engagement distribution
        st.plotly_chart(
            px.histogram(data, x='EngagementLevel', title="Engagement Level Distribution"),
            use_container_width=True
        )

        # Replaced dense scatter with a 2D Heatmap
        st.plotly_chart(
            px.density_heatmap(
                data, x='PlayTimeHours', y='AchievementsUnlocked',
                nbinsx=30, nbinsy=30,
                color_continuous_scale='Blues',
                title="Achievements vs Playtime Hours (Density Heatmap)"
            ),
            use_container_width=True
        )

        # Modified scatter plot with opacity to reduce clutter
        st.plotly_chart(
            px.scatter(
                data, x='SessionsPerWeek', y='AchievementsUnlocked',
                opacity=0.3,
                title="Achievements vs Sessions per Week (with Transparency)"
            ),
            use_container_width=True
        )

        # Binned Player Level Distribution
        bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
        labels = ['1-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99']
        data['PlayerLevelGroup'] = pd.cut(data['PlayerLevel'], bins=bins, labels=labels, right=True)

        player_level_group_counts = data['PlayerLevelGroup'].value_counts().sort_index().reset_index()
        player_level_group_counts.columns = ['PlayerLevelGroup', 'Count']

        fig_level_group = px.bar(
            player_level_group_counts,
            x='PlayerLevelGroup',
            y='Count',
            text_auto=True,
            color='PlayerLevelGroup',
            title="Player Level Distribution (Binned)"
        )

        fig_level_group.update_traces(
            textfont_size=12,
            textangle=0,
            textposition="outside",
            cliponaxis=False
        )

        fig_level_group.update_layout(
            showlegend=False,
            xaxis_title='Player Level Group',
            yaxis_title='Number of Players',
            uniformtext_minsize=10,
            uniformtext_mode='hide',
            bargap=0.3
        )

        st.plotly_chart(fig_level_group, use_container_width=True)


# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
