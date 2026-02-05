import tkinter as tk
from gui.app import NarradorGUI
from models.jugador import Jugador
from models.equipo import Equipo
from models.arbitro import Arbitro
from models.estadio import Estadio
from models.partido import Partido
from narration.narrador import Narrador

# Datos
estadio = Estadio("Centenario", "Armenia")

local = Equipo("Llaneros FC", "José Luis García")
visitante = Equipo("Deportivo Pereira", "Arturo Reyes")

for i in range(1, 12):
    local.agregar_jugador(Jugador(i, f"Jugador L{i}"))
    visitante.agregar_jugador(Jugador(i, f"Jugador V{i}"))
arbitros = [Arbitro("Ricardo A. Pabón", "Central", "XXX")]

partido = Partido(local, visitante, estadio, arbitros)
narrador = Narrador(partido)

# GUI
root = tk.Tk()
app = NarradorGUI(root, narrador)
root.mainloop()