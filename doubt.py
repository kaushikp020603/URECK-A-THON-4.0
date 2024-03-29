import streamlit as st
from transformers import pipeline

def main():
    st.title("Question Answering App")

    model_name = "deepset/roberta-base-squad2"

    # Load the model and tokenizer
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

    # Create input fields for question and context
    question = st.text_input("Enter your question:")
    context = st.text_area("Enter the context:")

    # Submit button
    if st.button("Submit") and question and context:
        QA_input = {'question': question, 'context': context}
        res = nlp(QA_input)
        answer_value = res['answer']
        st.write("Answer:", answer_value)

if __name__ == "__main__":
    main()
