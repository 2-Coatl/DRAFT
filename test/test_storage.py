from storage.user_storage import UserStorage


def test_storage():
    storage = UserStorage()

    # Crear usuario
    nuevo_usuario = storage.crear_usuario("admin", 1)
    print(f"Usuario creado: {nuevo_usuario.nombre}")

    # Buscar usuario
    usuario = storage.get_by_nombre("admin")
    if usuario:
        print(f"Usuario encontrado: {usuario.nombre}")


if __name__ == "__main__":
    test_storage()