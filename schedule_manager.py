import streamlit as st
import sqlite3
from datetime import datetime

# Function to create connection to SQLite database
def create_connection():
    conn = sqlite3.connect('schedule.db')
    return conn

# Function to create a new schedule item
def create_schedule_item(conn, title, datetime_obj):
    sql = ''' INSERT INTO schedule(title, date)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (title, datetime_obj))
    conn.commit()
    return cur.lastrowid

# Function to delete a schedule item
def delete_schedule_item(conn, item_id):
    sql = ''' DELETE FROM schedule WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (item_id,))
    conn.commit()

# Function to display schedule items
def show_schedule(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedule ORDER BY date ASC")
    schedule_items = cur.fetchall()
    return schedule_items

# Main function
def main():
    # Create a connection to the database
    conn = create_connection()

    # Page title
    st.title("Schedule Manager")

    # Input form to add new schedule item
    new_title = st.text_input("Title:")
    new_date = st.date_input("Date:")
    new_time = st.time_input("Time:")
    if st.button("Add Schedule Item") and new_title and new_date and new_time:
        # Combine date and time into datetime object
        dt = datetime.combine(new_date, new_time)
        create_schedule_item(conn, new_title, dt)
        st.success("Schedule item added successfully!")
        st.experimental_rerun()

    # Display schedule items
    schedule_items = show_schedule(conn)
    if schedule_items:
        st.header("Schedule:")
        for item in schedule_items:
            item_id, title, datetime_obj = item
            st.write(f"**{title}** - {datetime_obj}")
            if st.button("Delete", key=f"delete_{item_id}"):
                delete_schedule_item(conn, item_id)
                st.success("Schedule item deleted!")
                st.experimental_rerun()

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
