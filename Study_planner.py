import streamlit as st
import pandas as pd

# Title and description
st.title('Study Planner')
st.write("Welcome to the Study Planner. Plan your study sessions and track your progress here!")

# Sidebar for user input
st.sidebar.header("Study Session Details")
study_date = st.sidebar.date_input("Date")
subject = st.sidebar.selectbox("Subject", ["Math", "Science", "History", "English", "Other"])
hours_studied = st.sidebar.number_input("Hours Studied", min_value=0.0, step=0.5)

# Load existing data or create a new DataFrame
if 'study_data' not in st.session_state:
    st.session_state.study_data = pd.DataFrame(columns=['Date', 'Subject', 'Hours Studied'])

# Add study session to DataFrame
if st.sidebar.button("Add Study Session"):
    new_data = pd.DataFrame({'Date': [study_date], 'Subject': [subject], 'Hours Studied': [hours_studied]})
    st.session_state.study_data = pd.concat([st.session_state.study_data, new_data], ignore_index=True)
    st.sidebar.success("Study session added successfully!")

# Display study data table
st.subheader("Study Sessions")
st.write(st.session_state.study_data)

# Calculate total hours studied
total_hours = st.session_state.study_data['Hours Studied'].sum()
st.sidebar.subheader("Total Hours Studied")
st.sidebar.write(total_hours)
