import sqlite3

def create_task_db():
    """Create task database."""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                priority TEXT,
                completed INTEGER)''')  # Add 'priority' column to the table
    conn.commit()
    conn.close()

def create_schedule_db():
    """Create schedule database."""
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date DATE)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_task_db()
    create_schedule_db()
