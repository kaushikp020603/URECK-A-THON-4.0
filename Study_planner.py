import streamlit as st
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Title and description
st.title('Study Planner')
st.write("Welcome to the Study Planner. Plan your study sessions and track your progress here!")

# Create database connection and table
conn = sqlite3.connect('study_plan.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Date DATE,
                Subject TEXT,
                DayOfWeek TEXT,
                HoursStudied FLOAT
            )''')
conn.commit()

# Sidebar for user input
st.sidebar.header("Study Session Details")
study_date = st.sidebar.date_input("Date")
subject = st.sidebar.selectbox("Subject", ["Math", "Science", "History", "English", "Other"])
day_of_week = study_date.strftime('%A')
hours_studied = st.sidebar.number_input("Hours Studied", min_value=0.0, step=0.5)

# Add study session to database
if st.sidebar.button("Add Study Session"):
    cur.execute('''INSERT INTO study_sessions (Date, Subject, DayOfWeek, HoursStudied) 
                    VALUES (?, ?, ?, ?)''', (study_date, subject, day_of_week, hours_studied))
    conn.commit()
    st.sidebar.success("Study session added successfully!")

# Load study session data from database
study_data = pd.read_sql_query("SELECT * FROM study_sessions", conn)

# Train machine learning model
if study_data.shape[0] >= 5:  # Train model only if there are at least 5 study sessions
    # Preprocess categorical variables
    categorical_features = ['Subject', 'DayOfWeek']
    transformer = ColumnTransformer(transformers=[('encoder', OneHotEncoder(handle_unknown='ignore'), categorical_features)], remainder='passthrough')

    # Define pipeline
    pipeline = Pipeline(steps=[('preprocessor', transformer), ('regressor', LinearRegression())])

    # Splitting data into features (X) and target (y)
    X = study_data[['Subject', 'DayOfWeek']]
    y = study_data['HoursStudied']

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training the model
    model = pipeline.fit(X_train, y_train)

    # Make predictions
    prediction_data = pd.DataFrame({'Subject': [subject], 'DayOfWeek': [day_of_week]})
    prediction = model.predict(prediction_data)

    st.subheader("Predicted Study Time")
    st.write(f"Estimated study time for {subject} on {day_of_week}: {prediction[0]:.2f} hours")

    # Display additional information
    st.subheader("Additional Information")
    st.write("Past Study Patterns:")
    st.write(study_data[(study_data['Subject'] == subject) & (study_data['DayOfWeek'] == day_of_week)])

# Close database connection
conn.close()
