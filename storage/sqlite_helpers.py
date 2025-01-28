

import sqlite3


def lazy_load_data(db_file, query, *args, **kwargs):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, *args, **kwargs)
        while True:
            row = cursor.fetchall()
            if not row:
                break
            yield row