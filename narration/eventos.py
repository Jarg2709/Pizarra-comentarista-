class Evento:
    def __init__(self, minuto, descripcion):
        self.minuto = minuto
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.minuto}'] {self.descripcion}"
