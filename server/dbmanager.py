import sqlite3
from math import ceil

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
    
def get_amount():
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    result = int(c.fetchone()[0])
    conn.close()

    return int(ceil(result/1000.0))

def get_all_by(type, page):
    conn = sqlite3.connect("/Arachna/database/users.db")
    c = conn.cursor()
    
    result = list(c.execute("SELECT * FROM users ORDER BY " + type + " DESC LIMIT 1000 OFFSET ? ", (1000 * (page-1),)))
    conn.close()

    return result

def get_all_by_problems(page):
    return get_all_by("problems", page)

def get_all_by_score(page):
    return get_all_by("score", page)

