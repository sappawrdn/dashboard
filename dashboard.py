import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv('day_data.csv')
hour_df = pd.read_csv('hour_data.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.sidebar.image("cycling.png") 
st.sidebar.markdown("### Rentang Waktu")

start_date = st.sidebar.date_input('Mulai Tanggal', value=pd.to_datetime('2011-01-01'))
end_date = st.sidebar.date_input('Akhir Tanggal', value=pd.to_datetime('2012-12-31'))

filtered_data = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
hour_data = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

grouped_data = hour_data.groupby('hr')['cnt'].sum().reset_index()
avg_data = hour_data.groupby('hr')['cnt'].mean().reset_index()

grouped_by_season = filtered_data.groupby('season')['cnt'].agg(['sum', 'mean']).reset_index()

total_casual = filtered_data['casual'].sum()
total_registered = filtered_data['registered'].sum()
total_orders = filtered_data['cnt'].sum()

st.header('Bike Sharing Collection Dashboard :sparkles:')
st.subheader('Daily Rentals')
st.metric("Total rentals", f"{total_orders}")

st.line_chart(filtered_data.set_index('dteday')['cnt'])

st.subheader('Rentals by Seasons')
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='font-size:16px;'>Total Pengguna per Musim</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='season', y='sum', data=grouped_by_season, ax=ax, palette='Set2')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Pengguna')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Winter', 'Spring', 'Summer', 'Fall'])
    st.pyplot(fig)

with col2:
    st.markdown("<h3 style='font-size:16px;'>Rata-rata Pengguna per Musim</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='season', y='mean', data=grouped_by_season, ax=ax, palette='Set2')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Pengguna')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Winter', 'Spring', 'Summer', 'Fall'])
    st.pyplot(fig)

st.subheader('Rentals by Hours')
col3, col4 = st.columns(2)

with col3:
    st.markdown("<h3 style='font-size:16px;'>Total Pengguna per Jam</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='hr', y='cnt', data=grouped_data, ax=ax, color="#90CAF9")
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Pengguna')
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='x', rotation=45) 
    st.pyplot(fig)

with col4:
    st.markdown("<h3 style='font-size:16px;'>Rata-rata Pengguna per Jam</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='hr', y='cnt', data=avg_data, ax=ax, color="#B1D690")
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Pengguna')
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

st.subheader('User Demographic')
fig, ax = plt.subplots(figsize=(4, 3))
colors = ["#90CAF9", "#D3D3D3"] if total_casual > total_registered else ["#D3D3D3", "#90CAF9"]
labels = ['Casual Users', 'Registered Users']
counts = [total_casual, total_registered]
ax.bar(labels, counts, color=colors)
ax.set_ylabel('Total Users')
st.pyplot(fig)
