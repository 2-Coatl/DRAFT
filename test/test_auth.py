from services.auth_service import AuthService


def test_auth():
    auth_service = AuthService()

    # Intentar login con usuario existente (admin)
    usuario = auth_service.login("admin")
    if usuario:
        print(f"Login exitoso: {usuario.nombre}, rol: {usuario.rol}")
    else:
        print("Usuario no encontrado")

    # Registrar nuevo usuario
    nuevo = auth_service.registrar("usuario_normal")
    print(f"Nuevo usuario registrado: {nuevo.nombre}, rol: {nuevo.rol}")


if __name__ == "__main__":
    test_auth()