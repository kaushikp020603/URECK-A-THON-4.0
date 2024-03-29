import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to tokenize paragraphs
def tokenize_paragraphs(passage):
    paragraphs = passage.split('\n\n')  # Split by double newline for paragraphs
    tokenized_paragraphs = [sent_tokenize(para) for para in paragraphs]
    return tokenized_paragraphs

# Function to identify key elements in a sentence
def identify_key_elements(sentence):
    # Placeholder function, you can replace it with your own logic
    return sentence.split()[:3]  # Just taking the first three words as key elements for simplicity

# Function to generate quiz questions
def generate_quiz(passage):
    tokenized_sentences = sent_tokenize(passage)
    questions = []
    for sentence in tokenized_sentences:
        # Tokenize the sentence into words
        words = nltk.word_tokenize(sentence)
        # Identify nouns, verbs, and adjectives as potential key elements
        key_elements = [word for word, pos in nltk.pos_tag(words) if pos in ['NN', 'NNS', 'VB', 'VBP', 'JJ']]
        if len(key_elements) >= 1:  # Ensure at least one key element is found
            # Choose a random key element as the one to be omitted
            omitted_word = random.choice(key_elements)
            # Replace the omitted word in the sentence with a blank
            blank_sentence = ' '.join(['_____' if word == omitted_word else word for word in words])
            question = f"Fill in the blank: {blank_sentence}?"
            questions.append((sentence, question))  # Include the original sentence and the question
    random.shuffle(questions)
    return questions