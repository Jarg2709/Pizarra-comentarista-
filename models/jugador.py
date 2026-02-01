class Jugador:
    def __init__(self, numero, nombre, posicion=None, capitan=False):
        self.numero = numero
        self.nombre = nombre
        self.posicion = posicion
        self.capitan = capitan

    def __str__(self):
        if self.capitan:
            return f"{self.numero} {self.nombre} C"
        return f"{self.numero} {self.nombre}"
    

