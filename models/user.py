class User:
    def __init__(self, id: int, nombre: str, rol: int):
        self.id = id
        self.nombre = nombre
        self.rol = rol

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            nombre=data['nombre'],
            rol=data['rol']
        )