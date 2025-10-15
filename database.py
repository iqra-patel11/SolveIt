import sqlite3

DB_FILE = 'app.db'

def init_db():
    """Create database and tables if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create questions table
    c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Create answers table
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
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO questions (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()

def get_questions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    data = c.fetchall()
    conn.close()
    return data

def add_answer(question_id, answer):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, answer))
    conn.commit()
    conn.close()

def get_answers(question_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT answer FROM answers WHERE question_id=?', (question_id,))
    data = c.fetchall()
    conn.close()
    return [d[0] for d in data]
