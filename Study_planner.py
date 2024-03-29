import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Title and description
st.title('Study Planner')
st.write("Welcome to the Study Planner. Plan your study sessions and track your progress here!")

# Sidebar for user input
st.sidebar.header("Study Session Details")
study_date = st.sidebar.date_input("Date")
subject = st.sidebar.selectbox("Subject", ["Math", "Science", "History", "English", "Other"])
# Adding day of the week
day_of_week = study_date.strftime('%A')
hours_studied = st.sidebar.number_input("Hours Studied", min_value=0.0, step=0.5)

# Load existing data or create a new DataFrame
if 'study_data' not in st.session_state:
    st.session_state.study_data = pd.DataFrame(columns=['Date', 'Subject', 'Day of Week', 'Hours Studied'])

# Add study session to DataFrame
if st.sidebar.button("Add Study Session"):
    new_data = pd.DataFrame({'Date': [study_date], 'Subject': [subject], 'Day of Week': [day_of_week], 'Hours Studied': [hours_studied]})
    st.session_state.study_data = pd.concat([st.session_state.study_data, new_data], ignore_index=True)
    st.sidebar.success("Study session added successfully!")

# Display study data table
st.subheader("Study Sessions")
st.write(st.session_state.study_data)

# Train machine learning model
if st.session_state.study_data.shape[0] >= 5:  # Train model only if there are at least 10 study sessions
    # Preprocess categorical variables
    categorical_features = ['Subject', 'Day of Week']
    transformer = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_features)], remainder='passthrough')

    # Define pipeline
    pipeline = Pipeline(steps=[('preprocessor', transformer), ('regressor', LinearRegression())])

    # Splitting data into features (X) and target (y)
    X = st.session_state.study_data[['Subject', 'Day of Week']]
    y = st.session_state.study_data['Hours Studied']

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training the model
    model = pipeline.fit(X_train, y_train)

# Make predictions
    prediction_data = pd.DataFrame({'Subject': [subject], 'Day of Week': [day_of_week]})
    prediction = model.predict(prediction_data)

    st.subheader("Predicted Study Time")
    st.write(f"Estimated study time for {subject} on {day_of_week}: {prediction[0]:.2f} hours")

    # Display additional information
    st.subheader("Additional Information")
    st.write("Past Study Patterns:")
    st.write(st.session_state.study_data[(st.session_state.study_data['Subject'] == subject) & 
                                        (st.session_state.study_data['Day of Week'] == day_of_week)])
