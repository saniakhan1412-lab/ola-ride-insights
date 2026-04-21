import streamlit as st
import pandas as pd

df = pd.read_csv('OLA_Cleaned.csv')

st.set_page_config(page_title="OLA Ride Insights", layout="wide")
st.title('🚗 OLA Ride Insights Dashboard')
st.markdown('Interactive analytics for OLA ride data - By Sania Khan')

st.sidebar.header('🔍 Filters')
vehicle_filter = st.sidebar.multiselect(
    'Select Vehicle Type',
    options=df['Vehicle_Type'].unique(),
    default=df['Vehicle_Type'].unique()
)

status_filter = st.sidebar.multiselect(
    'Select Booking Status',
    options=df['Booking_Status'].unique(),
    default=df['Booking_Status'].unique()
)

filtered_df = df[
    (df['Vehicle_Type'].isin(vehicle_filter)) &
    (df['Booking_Status'].isin(status_filter))
]

st.subheader('📊 Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Rides', f"{len(filtered_df):,}")
col2.metric('Total Revenue', f"₹{filtered_df['Booking_Value'].sum():,.0f}")
col3.metric('Avg Driver Rating', f"{filtered_df[filtered_df['Driver_Ratings']>0]['Driver_Ratings'].mean():.2f}")
col4.metric('Total Cancellations', f"{len(filtered_df[filtered_df['Booking_Status'].str.contains('Canceled')]):,}")

st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader('📈 Booking Status Breakdown')
    status_counts = filtered_df['Booking_Status'].value_counts()
    st.bar_chart(status_counts)

with col2:
    st.subheader('💰 Revenue by Payment Method')
    payment_revenue = filtered_df[filtered_df['Payment_Method'] != 'Not Applicable'].groupby('Payment_Method')['Booking_Value'].sum()
    st.bar_chart(payment_revenue)

col3, col4 = st.columns(2)

with col3:
    st.subheader('❌ Customer Cancellation Reasons')
    customer_cancel = filtered_df[filtered_df['Canceled_Rides_by_Customer'] != 'Not Applicable']['Canceled_Rides_by_Customer'].value_counts()
    st.bar_chart(customer_cancel)

with col4:
    st.subheader('🚗 Rides by Vehicle Type')
    vehicle_counts = filtered_df['Vehicle_Type'].value_counts()
    st.bar_chart(vehicle_counts)

st.markdown('---')
st.subheader('📋 Raw Data')
st.dataframe(filtered_df.head(100))
