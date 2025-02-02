import sqlite3


class LocalDB:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.crear_tablas()

    def crear_tablas(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            rol INTEGER NOT NULL
        )
        ''')
        self.conn.commit()