import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Game Analytics Dashboard", layout="wide")

# Generate Sample Data
np.random.seed(42)

data = {
    "Player_ID": range(1, 501),
    "Age": np.random.randint(15, 35, 500),
    "Level_Reached": np.random.randint(1, 11, 500),
    "Time_Spent_Min": np.random.randint(30, 500, 500),
    "Sessions": np.random.randint(1, 20, 500),
    "In_Game_Purchase": np.random.choice(["Yes", "No"], 500),
    "Game_Mode": np.random.choice(["Easy", "Medium", "Hard"], 500),
    "Win_Rate": np.random.randint(40, 100, 500)
}

df = pd.DataFrame(data)
df["Engagement_Score"] = df["Time_Spent_Min"] * df["Sessions"]

st.title("🎮 Game Player Analytics Dashboard")

# Sidebar Filter
st.sidebar.header("Filter Options")

mode_filter = st.sidebar.selectbox("Select Game Mode", df["Game_Mode"].unique())

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (18, 30)
)

filtered_df = df[
    (df["Game_Mode"] == mode_filter) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Time Spent (min)", round(filtered_df["Time_Spent_Min"].mean(), 2))
col3.metric("Avg Win Rate (%)", round(filtered_df["Win_Rate"].mean(), 2))

st.divider()

# Level Distribution
st.subheader("Level Distribution")
level_counts = filtered_df["Level_Reached"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
level_counts.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Level Reached")
ax1.set_ylabel("Number of Players")
st.pyplot(fig1)

# Purchase vs Time
st.subheader("Purchase vs Time Spent")

purchase_analysis = filtered_df.groupby("In_Game_Purchase")["Time_Spent_Min"].mean()

fig2, ax2 = plt.subplots()
purchase_analysis.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Average Time (Minutes)")
st.pyplot(fig2)

# Correlation Heatmap
st.subheader("Correlation Heatmap")

fig3, ax3 = plt.subplots()
sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, ax=ax3)
st.pyplot(fig3)


st.subheader("Key Insights")

st.write("""
- Players in selected mode show varying retention patterns.
- Purchasers generally spend more time in-game.
- Engagement increases with number of sessions.
""")