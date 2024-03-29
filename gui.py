import streamlit as st
from quiz import generate_quiz

# Set up the layout
st.title("Quiz Generator")
st.write("Enter paragraph or some textual content to generate a quiz for efficient learning!!")

# Create a text input field
text_input = st.text_area("Text Input", height=200)

# Button to generate quiz
if st.button("Generate Quiz"):
    if text_input:
        questions = generate_quiz(text_input)
        st.write("Generated Quiz:")
        for i, question in enumerate(questions):
            st.write(f"{i+1}. {question}")
    else:
        st.write("Please enter some text to generate a quiz.")

# Button to clear text
if st.button("Clear"):
    text_input = ""  # Clear the text input field