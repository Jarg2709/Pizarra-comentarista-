class Arbitro:
    def __init__(self, nombre, rol, departamento):
        self.nombre = nombre
        self.rol = rol
        self.departamento = departamento

    def __str__(self):
        return f"{self.rol}: {self.nombre} ({self.departamento})"
        