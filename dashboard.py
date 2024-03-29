import streamlit as st
import subprocess

# Title and description
st.title('Study Buddy')
st.write("Welcome to the Study Buddy  Dashboard. Explore various functionalities with just a click!")

# Button options with icons
options = {
    "🗓️ Task Manager": "task_manager.py",
    "👩‍🎓 Schedule Manager": "schedule_manager.py",
    "📋 Quiz Generator": "gui.py",
    "📚 Text Summarizer": "Text_summarizer.py",
    "📋 Study Planner": "Study_planner.py",
    "🗓️ Note Maker": "cornell_notes_taker",
    "🗓️ Youtube Video Recommender": "youtube.py",
    "🗓️ Doubt Solver": "doubt.py",


}

# Display buttons vertically
st.subheader("Select an Option")
for option, file in options.items():
    if st.button(option):
        subprocess.Popen(["streamlit", "run", file], shell=True)
