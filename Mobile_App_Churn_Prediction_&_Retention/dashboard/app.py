import streamlit as st
import pandas as pd
import plotly.express as px
from mssql_config import get_mssql_connection

st.set_page_config(layout="wide")
st.title("📊 Real-Time Churn Prediction Dashboard")

# Connect to the database
conn = get_mssql_connection()

# ==============================
# Section 1: Recent User Activity
# ==============================
st.header("🟢 Recent User Activities")
activity_df = pd.read_sql("SELECT TOP 100 * FROM user_activity ORDER BY timestamp DESC", conn)
activity_df['timestamp'] = pd.to_datetime(activity_df['timestamp'])

st.dataframe(activity_df)

# Activity Trend Chart
st.subheader("📅 User Activity Over Time")
activity_time_chart = activity_df.groupby(activity_df['timestamp'].dt.date).size().reset_index(name='activity_count')
fig_activity = px.line(activity_time_chart, x='timestamp', y='activity_count', title='Daily User Activities')
st.plotly_chart(fig_activity, use_container_width=True)

# ==============================
# Section 2: Churn Predictions
# ==============================
st.header("🔴 Churn Predictions")
pred_df = pd.read_sql("SELECT * FROM churn_predictions", conn)
pred_df['prediction_time'] = pd.to_datetime(pred_df['prediction_time'])

st.dataframe(pred_df.sort_values('prediction_time', ascending=False).head(50))

# Time Series of Predictions
st.subheader("📊 Churn Predictions Over Time")
churn_over_time = pred_df.groupby(pred_df['prediction_time'].dt.date)['predicted_churn'].mean().reset_index()
fig_churn_trend = px.line(churn_over_time, x='prediction_time', y='predicted_churn',
                          title='Churn Probability Over Time', labels={'predicted_churn': 'Avg Churn Probability'})
st.plotly_chart(fig_churn_trend, use_container_width=True)

# ==============================
# Section 3: Churn Statistics
# ==============================
st.header("📈 Churn Summary")

# KPI Section
col1, col2, col3 = st.columns(3)

total_predictions = len(pred_df)
churn_count = pred_df['predicted_churn'].sum()
non_churn_count = total_predictions - churn_count
churn_rate = churn_count / total_predictions * 100

col1.metric("🔢 Total Predictions", total_predictions)
col2.metric("⚠️ Churned Users", int(churn_count))
col3.metric("📉 Churn Rate", f"{churn_rate:.2f}%")

# Pie Chart of Churn
st.subheader("🥧 Churn vs Non-Churn Distribution")
churn_dist = pred_df['predicted_churn'].value_counts().rename({0: 'No Churn', 1: 'Churn'})
fig_pie = px.pie(names=churn_dist.index, values=churn_dist.values, title='Churn Distribution')
st.plotly_chart(fig_pie, use_container_width=True)
