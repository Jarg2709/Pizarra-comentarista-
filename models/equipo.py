class Equipo:
    def __init__(self, nombre, director_tecnico):
        self.nombre = nombre
        self.director_tecnico = director_tecnico
        self.jugadores = []
    
    def __str__(self):
        return self.nombre

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def listar_jugadores(self):
        return "\n".join(str(j) for j in self.jugadores)
    
