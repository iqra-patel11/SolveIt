import sqlite3

def init_db():
    conn = sqlite3.connect("solveit.db")
    c = conn.cursor()
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    # Questions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("solveit.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password) VALUES (?,?)", (username, password))
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError:
        # username exists
        c.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = c.fetchone()[0]
    conn.close()
    return user_id

def get_user_by_username(username):
    conn = sqlite3.connect("solveit.db")
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_question(user_id, title, description):
    conn = sqlite3.connect("solveit.db")
    c = conn.cursor()
    c.execute("INSERT INTO questions(user_id, title, description) VALUES (?,?,?)", (user_id, title, description))
    conn.commit()
    conn.close()

def get_questions():
    conn = sqlite3.connect("solveit.db")
    c = conn.cursor()
    c.execute("""
        SELECT q.id, q.title, q.description, u.username
        FROM questions q
        JOIN users u ON q.user_id = u.id
        ORDER BY q.id DESC
    """)
    questions = c.fetchall()
    conn.close()
    return questions
