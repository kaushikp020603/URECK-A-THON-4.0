import streamlit as st
import sqlite3
from datetime import datetime

# Function to create connection to SQLite database
def create_connection():
    conn = sqlite3.connect('cornell_notes.db')
    return conn

# Function to create a table to store file paths
def create_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filepath TEXT)''')
    conn.commit()

# Function to generate Cornell notes and save them in a text file
def generate_and_save_cornell_notes(main_points, key_details, summary, filename):
    # Generate Cornell notes
    cornell_notes = []
    cornell_notes.append("Main Points:")
    for point in main_points.split('\n'):
        cornell_notes.append(f"- {point.strip()}")
    cornell_notes.append("\nKey Details:")
    for detail in key_details.split('\n'):
        cornell_notes.append(f"- {detail.strip()}")
    cornell_notes.append("\nSummary:")
    cornell_notes.append(summary)

    # Save Cornell notes in a text file with the specified filename
    with open(filename, 'w') as file:
        file.write('\n'.join(cornell_notes))

    return filename

# Main function
def main():
    # Create a connection to the database
    conn = create_connection()
    create_table(conn)

    # Page title
    st.title("Cornell Note-Taking System")

    # Text inputs for main points, key details, summary, and filename
    main_points = st.text_area("Main Points")
    key_details = st.text_area("Key Details")
    summary = st.text_area("Summary")
    filename = st.text_input("Filename", "cornell_notes")

    # Button to generate and save Cornell notes
    if st.button("Generate & Save Cornell Notes"):
        if not main_points or not key_details or not summary or not filename:
            st.warning("Please fill in all fields.")
        else:
            # Generate and save Cornell notes
            filename_with_extension = f"{filename}.txt"
            saved_filename = generate_and_save_cornell_notes(main_points, key_details, summary, filename_with_extension)

            # Save file path in database
            cur = conn.cursor()
            cur.execute("INSERT INTO notes(filepath) VALUES (?)", (saved_filename,))
            conn.commit()

            st.success(f"Cornell notes saved successfully as '{saved_filename}'")

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
