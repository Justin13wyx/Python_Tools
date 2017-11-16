import os
import sqlite3 as sql

if os.name == 'nt':
    USER_HOME = os.getenv("HOME")  # Win下获得用户家目录的方法??
elif os.name == 'posix':
    USER_HOME = os.getenv('HOME')
else:
    USER_HOME = "~"

DB_PATH = os.path.join(USER_HOME, "fucking.db")


def connect():
    try:
        conn = sql.connect(DB_PATH, timeout=3)
    except ConnectionError:
        print("Cannot connect to the database")
        exit(-1)
    return conn


def init():
    if not os.path.exists(DB_PATH):
        print("First run. Initing database...")
        conn = connect()
        for n in range(4):
            conn.execute(
                'CREATE TABLE IF NOT EXISTS diction_{0} (id integer primary key autoincrement not null, \
                  word VARCHAR(255) not null, \
                  symbols VARCHAR(255), \
                  means VARCHAR(255) NOT NULL)'.format(str(n)))
        conn.close()
    else:
        pass


def select(_id, location):
    get_sql = 'SELECT word, symbols, means FROM diction_{0} WHERE id = ?'.format(location)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(get_sql, _id)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def lookup(word):
    part = get_location(word)
    lookup_sql = 'SELECT id FROM diction_{0} WHERE word = ?'.format(part)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(lookup_sql, (word,))
    _id = cursor.fetchall()
    cursor.close()
    conn.close()
    if _id:
        return select(_id[0], part)
    else:
        return False


def save(info):
    part = get_location(info['word'])
    save_sql = 'INSERT INTO diction_{0} (word, symbols, means) VALUES (?, ?, ?)'.format(part)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(save_sql, (
        info['word'],
        str(info['symbols']),
        str(info['means'])  # TODO: 这里, 存储的时候要想办法搞一个可序列化的字符串 才行
    ))
    conn.commit()
    cursor.close()
    conn.close()


def get_location(word):
    asc = ord(word[0])
    if asc in range(97, 103) or asc in range(65, 70):
        return "0"
    if asc in range(103, 109) or asc in range(71, 76):
        return "1"
    if asc in range(109, 116) or asc in range(77, 83):
        return "2"
    if asc in range(116, 123) or asc in range(84, 90):
        return "3"
    else:
        print(asc)
        raise UnknownWordException


class UnknownWordException(BaseException):
    pass