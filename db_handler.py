import sqlite3
from datetime import datetime

DATABASE_PATH = "db/db.db"
time_now = datetime.now().isoformat()


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    create_version_table = """CREATE TABLE IF NOT EXISTS versions (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                  version_number TEXT NOT NULL,
                                                  creationdate TIMESTAMP)"""

    create_category_table = """CREATE TABLE IF NOT EXISTS categorys (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                  category TEXT NOT NULL,
                                                  creationdate TIMESTAMP)"""
    
    create_entry_table = """CREATE TABLE IF NOT EXISTS entrys (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  version TEXT NOT NULL, 
                                                  category TEXT NOT NULL, 
                                                  entry_text TEXT NOT NULL,
                                                  language TEXT NOT NULL,
                                                  creationdate TIMESTAMP)"""

    cursor.execute(create_version_table)
    cursor.execute(create_category_table)
    cursor.execute(create_entry_table)

    conn.commit()
    conn.close()

####################_____________VERSIONS_____________####################
def get_versions():

    version_list = []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM versions""")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        version_list.append(row[1])

    return version_list


def add_version(version):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO versions (version_number, creationdate) VALUES (?, ?)""", (version, time_now))
    conn.commit()
    conn.close()


####################_____________CATEGORYS_____________####################

def get_categorys():

    categorys_list = []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM categorys""")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        categorys_list.append(row[1])
    return categorys_list


def add_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO categorys (category, creationdate) VALUES (?, ?)""", (category, time_now))
    conn.commit()
    conn.close()

####################_____________ENTRYS_____________####################

def get_entrys():

    entrys_list = []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM entrys""")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        entrys_list.append(row[1])
    return entrys_list

def add_entry(version, category, update_text, language):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO entrys (version, category, entry_text, language, creationdate) VALUES (?, ?, ?, ?, ?)""", (version, category, update_text, language, time_now))
    conn.commit()
    conn.close()
