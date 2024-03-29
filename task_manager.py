import streamlit as st
import sqlite3

# Function to create connection to SQLite database
def create_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

# Function to create a new task
def create_task(conn, task):
    sql = ''' INSERT INTO tasks(task, completed)
              VALUES(?,0) '''
    cur = conn.cursor()
    cur.execute(sql, (task,))
    conn.commit()
    return cur.lastrowid

# Function to mark a task as completed
def complete_task(conn, task_id):
    sql = ''' UPDATE tasks
              SET completed = 1
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# Function to delete a task
def delete_task(conn, task_id):
    sql = ''' DELETE FROM tasks WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# Function to display tasks
def show_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY completed ASC")  # Order by completion status (incomplete tasks first)
    tasks = cur.fetchall()
    return tasks

# Main function
def main():
    # Create a connection to the database
    conn = create_connection()

    # Page title
    st.title("Task Manager")

    # Input form to add new tasks
    new_task = st.text_input("Add new task:")
    if st.button("Add Task") and new_task:
        create_task(conn, new_task)
        st.success("Task added successfully!")
        st.experimental_rerun()

    # Display tasks
    tasks = show_tasks(conn)
    if tasks:
        st.header("Tasks:")
        for task in tasks:
            task_id, task_desc, completed = task
            if completed:
                st.write(f"~~{task_desc}~~ (Completed)")
            else:
                col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
                col1.write("")
                if col2.checkbox(task_desc, key=f"checkbox_{task_id}"):
                    complete_task(conn, task_id)
                    st.write("Task marked as completed!")
                    st.experimental_rerun()
                if not completed and col3.button("❌", key=f"delete_{task_id}"):
                    delete_task(conn, task_id)
                    st.success("Task deleted!")
                    st.experimental_rerun()

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
