import streamlit as st
import subprocess

st.title('🚀 Study Buddy 📚')
st.markdown(
    """
    <style>
        .title {
            color: #FF5733;
            text-align: center !important; /* Center align the title */
            font-size: 48px;
            margin-bottom: 30px;
        }
        .description {
            color: #666666;
            text-align: center;
            font-size: 20px;
            margin-bottom: 50px;
        }
    </style>
    """, unsafe_allow_html=True
)
st.markdown('<p class="description">Welcome to the Study Buddy Dashboard. Explore various functionalities with just a click!</p>', unsafe_allow_html=True)

# Button options with icons
options = {
    "📝 Task Manager": "task_manager.py",
    "📅 Schedule Manager": "schedule_manager.py",
    "❓ Quiz Generator": "quiz2.py",
    "📑 Text Summarizer": "Text_summarizer.py",
    "📖 Study Planner": "Study_planner.py",
    "🗒️ Note Maker": "cornell_notes_taker.py",
    "📺 Youtube Video Recommender": "youtube.py",
    "📺 AVA: CHATBOT": "chat.py",
    "❓ Doubt Solver": "doubt.py",
}

# Display buttons in a grid layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("Tools")
    for option, file in list(options.items())[:4]:
        if st.button(option):
            subprocess.Popen(["streamlit", "run", file], shell=True)

with col2:
    st.subheader("Utilities")
    for option, file in list(options.items())[4:]:
        if st.button(option):
            subprocess.Popen(["streamlit", "run", file], shell=True)
