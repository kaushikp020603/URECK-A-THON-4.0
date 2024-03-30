import streamlit as st
import sqlite3

# Function to create connection to SQLite database
def create_connection(db_name='tasks.db'):
    conn = sqlite3.connect(db_name)
    return conn

# Function to create a new task
def create_task(conn, task, priority):
    sql = ''' INSERT INTO tasks(task, priority, completed)
              VALUES(?,?,0) '''
    cur = conn.cursor()
    cur.execute(sql, (task, priority))
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
def show_tasks(conn, completed=False):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE completed = ? ORDER BY priority DESC", (1 if completed else 0,))  
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
    priority = st.selectbox("Priority:", ["Low", "Medium", "High"])
    if st.button("Add Task") and new_task:
        create_task(conn, new_task, priority)
        st.success("Task added successfully!")
        st.experimental_rerun()

    # Display tasks
    completed_tasks = show_tasks(conn, completed=True)
    incomplete_tasks = show_tasks(conn)
    
    if incomplete_tasks:
        st.header("Incomplete Tasks:")
        for task in incomplete_tasks:
            task_id, task_desc, task_priority, completed = task
            st.write(f"**{task_desc}** - Priority: {task_priority}")
            if st.checkbox("Complete", key=f"checkbox_{task_id}"):
                complete_task(conn, task_id)
                st.write("Task marked as completed!")
                st.experimental_rerun()
            if st.button("Delete", key=f"delete_{task_id}"):
                delete_task(conn, task_id)
                st.success("Task deleted!")
                st.experimental_rerun()

    if completed_tasks:
        st.header("Completed Tasks:")
        for task in completed_tasks:
            task_id, task_desc, task_priority, completed = task
            st.write(f"~~{task_desc}~~ - Priority: {task_priority}")

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
