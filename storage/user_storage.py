from models.user import User
from storage.local_db import LocalDB


class UserStorage:
    def __init__(self):
        self.db = LocalDB()

    def get_by_nombre(self, nombre: str) -> User | None:
        cursor = self.db.conn.execute(
            "SELECT id, nombre, rol FROM users WHERE nombre = ?",
            (nombre,)
        )
        row = cursor.fetchone()
        if row:
            return User(id=row[0], nombre=row[1], rol=row[2])
        return None

    def crear_usuario(self, nombre: str, rol: int) -> User:
        cursor = self.db.conn.execute(
            "INSERT INTO users (nombre, rol) VALUES (?, ?)",
            (nombre, rol)
        )
        self.db.conn.commit()
        return User(id=cursor.lastrowid, nombre=nombre, rol=rol)