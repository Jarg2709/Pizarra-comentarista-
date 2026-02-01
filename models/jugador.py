class Jugador:
    def __init__(self, numero, nombre, posicion=None, capitan=False, x=0, y=0):
        self.numero = numero
        self.nombre = nombre
        self.posicion = posicion
        self.capitan = capitan
        self.x = x
        self.y = y

    def __str__(self):
        if self.capitan:
            return f"{self.numero} {self.nombre} C"
        return f"{self.numero} {self.nombre}"
    

