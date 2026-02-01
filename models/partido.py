class Partido:
    def __init__(self, equipo_local, equipo_visitante, estadio, arbitros):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.estadio = estadio
        self.arbitros = arbitros
        self.minuto = 0

    def informacion_general(self):
        info = (
            f"Estadio: {self.estadio}\n"
            f"Partido: {self.equipo_local} vs {self.equipo_visitante}"
            f"Árbitros: \n"
        )

        for a in self.arbitros:
            info += f" - {a}\n"
        return info  