import os
import sqlite3


def ensure_created():
    if not os.path.exists("test.db"):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute(
            """create table posts (
    id integer primary key autoincrement,
    title varchar(255) not null,
    content text not null,
    published bool not null,
    rating int null
    )"""
        )
        conn.commit()
    else:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

    cursor.row_factory = sqlite3.Row
    return conn, cursor
