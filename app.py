import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="Campaign Performance",
    page_icon="📈",
    layout="wide",
)

# Custom CSS to style the app
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff; /* White background */
    }
    h1 {
        color: #ff9800; /* Orange title */
    }
    h3 {
        color: #ff9800; /* Orange subheadings */
    }
    .stMetric {
        background-color: #ff9800; /* Orange background for metrics */
        color: white; /* White text for metrics */
        border-radius: 10px;
        padding: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #ff9800; /* Orange sidebar background */
        color: white; /* White text in sidebar */
        border-radius: 10px;
        padding: 10px;
    }
    .sidebar h2, .sidebar h3, .sidebar label {
        color: white; /* White text for sidebar headings and labels */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("Campaign Performance")

# Description
st.write("This app helps you pick the best performing campaign.")

# Load the CSV file
@st.cache_data
def load_data():
    data = pd.read_csv('final_detailed_campaign_report.csv')
    return data

# Call the function to load the data
data = load_data()

# Sidebar for filtering
st.sidebar.header("Filter Options")

# Add 'All' option for campaign_id
campaign_ids = ['All'] + data['campaign_id'].unique().tolist()
selected_campaign_id = st.sidebar.selectbox("Select Campaign ID", campaign_ids)

# Add 'All' option for message_status
message_statuses = ['All'] + data['message_status'].unique().tolist()
selected_message_status = st.sidebar.selectbox("Select Message Status", message_statuses)

# Add 'All' option for organization
organizations = ['All'] + data['organization'].unique().tolist()
selected_organization = st.sidebar.selectbox("Select Organization", organizations)

# Filter data based on selections
filtered_data = data.copy()

if selected_campaign_id != 'All':
    filtered_data = filtered_data[filtered_data['campaign_id'] == selected_campaign_id]

if selected_message_status != 'All':
    filtered_data = filtered_data[filtered_data['message_status'] == selected_message_status]

if selected_organization != 'All':
    filtered_data = filtered_data[filtered_data['organization'] == selected_organization]

# Tiles calculations
no_of_learners = filtered_data['whatsapp_phone_number'].nunique()
messages_sent = filtered_data.shape[0]
messages_delivered = filtered_data[filtered_data['message_status'].isin(['read', 'responded', 'delivered'])].shape[0]
messages_read = filtered_data[filtered_data['message_status'] == 'read'].shape[0]
messages_responded = filtered_data[filtered_data['message_status'] == 'responded'].shape[0]
invalid_messages = filtered_data[filtered_data['message_status'] == 'invalid_user'].shape[0]

# Display the tiles
st.write("### Campaign Summary")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("No. of Learners", no_of_learners)
col2.metric("Messages Sent", messages_sent)
col3.metric("Messages Delivered", messages_delivered)
col4.metric("Messages Read", messages_read)
col5.metric("Messages Responded", messages_responded)
col6.metric("Invalid Messages", invalid_messages)

# Funnel area chart data preparation using the filtered DataFrame (excluding invalid messages)
funnel_chart_data = pd.DataFrame({
    'message_status': ['sent', 'delivered', 'read', 'responded'],
    'message_count': [
        messages_sent,
        messages_delivered,
        messages_read,
        messages_responded
    ]
})

# Create the funnel area chart
fig = px.funnel_area(
    names=funnel_chart_data['message_status'].tolist(),
    values=funnel_chart_data['message_count'].tolist(),
    title="Message Status Funnel Area Chart"
)

# Display the chart above the filtered data table
st.write("### Funnel Area Chart of Message Status")
st.plotly_chart(fig)

# Display the filtered data as a table below the chart
st.write("### Filtered Campaign Data")
st.dataframe(filtered_data)
