import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Title and description
st.title('Text Summarization App')
st.write("Enter your text below and click the button to summarize it.")

# Text area for user input
user_input = st.text_area("Enter your text here:")

# Function to summarize text
def summarize_text(text):
    if text:
        summary = summarizer(text, max_length=1000, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    else:
        return ""

# Button to trigger summarization
if st.button("Summarize"):
    summary_text = summarize_text(user_input)
    if summary_text:
        st.subheader("Summary:")
        st.write(summary_text)
    else:
        st.write("Please enter some text to summarize.")
