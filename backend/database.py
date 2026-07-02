import sqlite3


def execute_sql(sql_query):
    conn = sqlite3.connect("data/employees.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(sql_query)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]