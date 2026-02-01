import tkinter as tk
from tkinter import ttk
from gui.cancha import Cancha
class NarradorGUI:
    def __init__(self, root, narrador):
        self.root = root
        self.narrador = narrador

        # Configuración ventana
        self.root.title("🎙️ Narrador de Fútbol")
        self.root.geometry("750x650")
        self.root.configure(bg="#1e1e1e")

        self._crear_estilos()
        self._crear_widgets()

    # =========================
    # ESTILOS
    # =========================
    def _crear_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=6
        )

        style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="white",
            font=("Segoe UI", 11)
        )

    # =========================
    # WIDGETS
    # =========================
    def _crear_widgets(self):

        # ----- TÍTULO -----
        lbl_titulo = ttk.Label(
            self.root,
            text="Narración del Partido",
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack(pady=10)

        # ----- INFO PARTIDO -----
        info = self.narrador.partido.informacion_general()
        self.lbl_info = ttk.Label(
            self.root,
            text=info,
            justify="center"
        )
        self.lbl_info.pack(pady=5)

        # ----- CANCHA -----
        self.cancha = Cancha(self.root)

        # Dibujar jugadores
        self._dibujar_jugadores()

        # ----- ÁREA DE NARRACIÓN -----
        self.texto = tk.Text(
            self.root,
            height=8,
            bg="#2b2b2b",
            fg="white",
            font=("Consolas", 10),
            state="disabled"
        )
        self.texto.pack(padx=15, pady=10, fill="x")

        # ----- BOTONES -----
        frame_botones = tk.Frame(self.root, bg="#1e1e1e")
        frame_botones.pack(pady=10)

        ttk.Button(
            frame_botones,
            text="⚽ Gol Local",
            command=self.gol_local
        ).pack(side="left", padx=10)

        ttk.Button(
            frame_botones,
            text="🚫 Falta Visitante",
            command=self.falta_visitante
        ).pack(side="left", padx=10)

    # =========================
    # LÓGICA DE GUI
    # =========================
    def _dibujar_jugadores(self):
        """Dibuja todos los jugadores en la cancha"""
        for j in self.narrador.partido.equipo_local.jugadores:
            self.cancha.dibujar_jugador(j, color="#1976d2")  # azul

        for j in self.narrador.partido.equipo_visitante.jugadores:
            self.cancha.dibujar_jugador(j, color="#d32f2f")  # rojo

    def escribir(self, mensaje):
        self.texto.config(state="normal")
        self.texto.insert("end", mensaje + "\n")
        self.texto.config(state="disabled")
        self.texto.see("end")

    # =========================
    # EVENTOS DEL PARTIDO
    # =========================
    def gol_local(self):
        jugador = self.narrador.partido.equipo_local.jugadores[0]
        equipo = self.narrador.partido.equipo_local

        evento = self.narrador.gol(23, jugador, equipo)
        self.escribir(str(evento))

    def falta_visitante(self):
        jugador = self.narrador.partido.equipo_visitante.jugadores[0]

        evento = self.narrador.falta(35, jugador)
        self.escribir(str(evento))
