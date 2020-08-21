import sqlite3

def get_connection_db():
    return sqlite3.connect('telegram.db')
def init_db():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS telegram(
        userid INT(24) PRIMARY KEY NOT NULL,
        phone VARCHAR(15) NOT NULL,
        username VARCHAR(34) NULL
    )
    """)
    c.execute("CREATE INDEX phone_idx ON telegram(phone)")
    c.execute("CREATE INDEX username_idx ON telegram(username)")
    conn.commit()
def push_db_to_sql():
    print("start")
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("PRAGMA synchronous = 0")
    c.execute("PRAGMA journal_mode = 0")
    with open("telegram_40M.txt") as f:
        for index, line in enumerate(f):
            if not(index == 0):
                raw = str.strip(line).split("|")[2:-1]
                add_db(raw[-4], raw[-3], raw[-2], c)
                if index % 500000 == 0:
                    print(index/1000, raw)
                    conn.commit()
        conn.commit()
def get_userid(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute('SELECT phone, userid, username  FROM telegram WHERE  userid=?', (userid,))
    conn.commit()
    return c.fetchone()
def add_db(phone, userid, username, c):
    try:
        print(f"{phone}, {userid}, {username}")
        c.execute('INSERT INTO telegram (phone, userid, username) SELECT ?, ?, ?', (phone, userid, username))
        print(e, f"{phone}, {userid}, {username}")
    except Exception as e:
        pass
def count_elem():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(userid)  FROM telegram')
    conn.commit()
    conn.commit()
    for i in c.fetchall():
        print(i)
def print_db(limit=50):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute('SELECT userid FROM telegram LIMIT ?', (limit,))
    conn.commit()
    for i in c.fetchall():
        print(i)
def get_phone(number):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute('SELECT * FROM telegram WHERE phone=?', (number,))
    conn.commit()
    for i in c.fetchall():
        print(i)

    


    