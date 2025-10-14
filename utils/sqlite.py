# Utility to provide connector for SQLite

import sqlite3

def get_conn():
    conn = sqlite3.connect("stork.db")
    return conn

def close_conn(conn):
    conn.close()

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    #commit to everything :)
    conn.commit()
    return cursor

# All-in one - get conn, query then close
def query_db_and_close(query):
    conn = get_conn()
    cursor = execute_query(conn, query)
    result = cursor.fetchall()
    close_conn(conn)
    return result



    