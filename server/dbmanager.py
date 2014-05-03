import sqlite3
from math import ceil
import os

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

DISK = "/Arachna/database/users.db"
MEMORY = ":memory:"
done = "Arachna/database/DONE"
db = None

def create(users_dict):
    conn = sqlite3.connect(DISK)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username VARCHAR(50), problems INTEGER, score REAL)")

    users_list = [(key, value[0], value[1]) for key, value in users_dict.items()]

    c.executemany("INSERT INTO users VALUES (?, ?, ?)", users_list)

    conn.commit()
    conn.close()
    touch(done)

def copy():
    conn = sqlite3.connect(DISK)
    c = conn.cursor()
    result = list(c.execute("SELECT * FROM users"))
    conn.close()

    conn = sqlite3.connect(MEMORY)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username VARCHAR(50), problems INTEGER, score REAL)")
    c.executemany("INSERT INTO users VALUES (?, ?, ?)", result)
    global db
    db = c 

def execute(query, param=None):
    if os.path.isfile(done):
        os.remove(done)
        db.close()
        copy()
    if param:
        return db.execute(query, param)
    return db.execute(query)

def get_user(user):
    execute("SELECT * FROM users WHERE username = ?", (user,))
    result = db.fetchone()
    return result
    
def get_amount():
    execute("SELECT COUNT(*) FROM users")
    result = int(db.fetchone()[0])
    return int(ceil(result/1000.0))

def get_all_by(type, page):
    result = list(execute("SELECT * FROM users ORDER BY " + type + " DESC LIMIT 1000 OFFSET ? ", (1000 * (page-1),)))
    return result

def get_all_by_problems(page):
    return get_all_by("problems", page)

def get_all_by_score(page):
    return get_all_by("score", page)

