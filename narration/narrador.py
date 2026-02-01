from .eventos import Evento

class Narrador:
    def __init__(self, partido):
        self.partido = partido
        self.eventos = []
    
    def narrar_inicio(self):
        print("Muy buenas tardes")
        print(self.partido.informacion_general())

    def gol(self, minuto, jugador, equipo):
        evento = Evento(
            minuto,
            f"GOOOOL de {jugador.nombre} para {equipo.nombre}")
        self.eventos.append(evento)
        return evento
    
    def falta(self, minuto, jugador):
        evento = Evento(
            minuto, 
            f"Falta cometida por {jugador.nombre}"
        )
        self.eventos.append(evento)
        return evento
        