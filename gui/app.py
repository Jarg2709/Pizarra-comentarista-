import tkinter as tk
from tkinter import ttk
from gui.cancha import Cancha


class NarradorGUI:
    def __init__(self, root, narrador):
        self.root = root
        self.narrador = narrador

        self.root.title("Narrador de Fútbol")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e1e")

        self.form_local = tk.StringVar(value="4-4-2")
        self.form_visita = tk.StringVar(value="4-3-3")

        self._crear_widgets()

    def _crear_widgets(self):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=5)

        ttk.Label(frame, text="Local:").grid(row=0, column=0, padx=5)
        ttk.Combobox(
            frame,
            textvariable=self.form_local,
            values=["4-4-2", "4-3-3", "3-5-2"],
            width=7,
            state="readonly"
        ).grid(row=0, column=1)

        ttk.Label(frame, text="Visitante:").grid(row=0, column=2, padx=5)
        ttk.Combobox(
            frame,
            textvariable=self.form_visita,
            values=["4-4-2", "4-3-3", "3-5-2"],
            width=7,
            state="readonly"
        ).grid(row=0, column=3)

        ttk.Button(
            frame,
            text="Aplicar",
            command=self.aplicar_formaciones
        ).grid(row=0, column=4, padx=10)

        self.cancha = Cancha(self.root, on_resize=self.aplicar_formaciones)

    # =========================
    def calcular_formacion(self, formacion, lado):
        esquemas = {
            "4-4-2": [1, 4, 4, 2],
            "4-3-3": [1, 4, 3, 3],
            "3-5-2": [1, 3, 5, 2]
        }

        filas = esquemas[formacion]
        posiciones = []

        if lado == "local":
            xs = [0.08, 0.25, 0.45, 0.65]
        else:
            xs = [0.92, 0.75, 0.55, 0.35]

        for x, n in zip(xs, filas):
            for i in range(n):
                y = (i + 1) / (n + 1)
                posiciones.append((x, y))

        return posiciones

    # =========================
    def aplicar_formaciones(self):
        local = self.narrador.partido.equipo_local
        visita = self.narrador.partido.equipo_visitante

        pos_local = self.calcular_formacion(self.form_local.get(), "local")
        pos_visita = self.calcular_formacion(self.form_visita.get(), "visitante")

        for jugador, (nx, ny) in zip(local.jugadores, pos_local):
            jugador.nx, jugador.ny = nx, ny
            if not hasattr(jugador, "_grafico"):
                self.cancha.dibujar_jugador(jugador, "#1976d2")
            else:
                self.cancha.mover_jugador(jugador)

        for jugador, (nx, ny) in zip(visita.jugadores, pos_visita):
            jugador.nx, jugador.ny = nx, ny
            if not hasattr(jugador, "_grafico"):
                self.cancha.dibujar_jugador(jugador, "#d32f2f")
            else:
                self.cancha.mover_jugador(jugador)
