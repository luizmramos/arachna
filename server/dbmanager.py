import sqlite3

def create(users_dict):
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username VARCHAR(50), problems INTEGER, score REAL)")

    users_list = [(key, value[0], value[1]) for key, value in users_dict.items()]

    c.executemany("INSERT INTO users VALUES (?, ?, ?)", users_list)

    conn.commit()
    conn.close()

def get_user(user):
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE username = ?", (user,))
    result = c.fetchone()
    conn.close()

    return result
    
def get_all_by_problems():
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()
    
    result = list(c.execute("SELECT * FROM users ORDER BY problems DESC"))
    conn.close()

    return result

def get_all_by_score():
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()
    
    result = list(c.execute("SELECT * FROM users ORDER BY score DESC"))
    conn.close()

    return result
