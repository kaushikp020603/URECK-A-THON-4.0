import streamlit as st
import spacy
import random

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Function to generate questions based on input paragraph
def generate_questions(paragraph):
    doc = nlp(paragraph)
    questions = []

    # Extract noun phrases from the paragraph
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    # Generate questions based on noun phrases
    for noun_phrase in noun_phrases:
        question = f"What is {noun_phrase}?"
        questions.append(question)

    return questions

# Streamlit UI
def main():
    st.title("Quiz Generator")

    # Input paragraph
    paragraph = st.text_area("Enter a paragraph:")

    if st.button("Generate Questions"):
        if paragraph:
            questions = generate_questions(paragraph)
            st.write("Generated Questions:")
            for question in questions:
                st.write(question)
        else:
            st.warning("Please enter a paragraph.")

if __name__ == "__main__":
    main()
