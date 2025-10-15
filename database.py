import sqlite3

# Connect to SQLite database (creates file if not exist)
conn = sqlite3.connect('app.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    answer TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
)
''')

conn.commit()
conn.close()

# Functions to interact with database

def add_question(title, description):
    """Add a new question"""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('INSERT INTO questions (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()

def get_questions():
    """Return all questions"""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    data = c.fetchall()
    conn.close()
    return data

def add_answer(question_id, answer):
    """Add an answer to a question"""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, answer))
    conn.commit()
    conn.close()

def get_answers(question_id):
    """Return all answers for a question"""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT answer FROM answers WHERE question_id=?', (question_id,))
    data = c.fetchall()
    conn.close()
    # Flatten the list of tuples to a list
    return [d[0] for d in data]
