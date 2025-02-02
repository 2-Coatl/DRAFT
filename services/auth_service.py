from storage.user_storage import UserStorage
from models.user import User


class AuthService:
    def __init__(self):
        self.user_storage = UserStorage()

    def login(self, nombre: str) -> User | None:
        """
        Intenta autenticar un usuario por nombre.
        Retorna el usuario si existe, None si no.
        """
        return self.user_storage.get_by_nombre(nombre)

    def registrar(self, nombre: str, rol: int = 2) -> User:
        """
        Registra un nuevo usuario.
        Por defecto asigna rol=2 (asumiendo 1=admin, 2=usuario normal)
        """
        return self.user_storage.crear_usuario(nombre, rol)