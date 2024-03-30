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
        
        # Create a dictionary to store items by date
        items_by_date = {}
        for item in schedule_items:
            item_id, title, datetime_str = item
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            date_str = datetime_obj.strftime('%Y-%m-%d')
            if date_str not in items_by_date:
                items_by_date[date_str] = []
            items_by_date[date_str].append((title, datetime_obj.strftime('%H:%M')))
        
        # Display schedule in a calendar-like table
        for date, items in items_by_date.items():
            st.subheader(date)
            table_data = []
            for title, time in items:
                table_data.append([time, title])
            st.table(table_data)

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
