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

        # ----- SELECCIÓN DE FORMACIÓN -------
        frame_formacion = tk.Frame(self.root, bg="#1e1e1e")
        frame_formacion.pack(pady=5)

        ttk.Label(frame_formacion, text="Fomración:").pack(side="left", padx=5)
        self.formacion = tk.StringVar(value="4-4-2")

        combo = ttk.Combobox(
            frame_formacion,
            textvariable=self.formacion,
            values=["4-4-2", "4-3-3", "3-5-2"],
            width=10,
            state="readonly"
        )
        combo.pack(side="left",padx=5)

        ttk.Button(
            frame_formacion,
            text="Aplicar",
            command=self.aplicar_formacion
        ).pack(side="left", padx=10)


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
        self.aplicar_formacion()

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
    
    def calcular_posciones(self, formacion, lado="local"):
        """
        Retorna una lista de (x,y) según la formacion
        """
        w, h = 500, 300
        margen_x = 60

        if lado == "local":
            base_x = margen_x
            direccion = 1
        else:
            base_x = w - margen_x
            direccion = -1

        formaciones = {
            "4-4-2": [1, 4, 4, 2],
            "4-3-3": [1, 4, 3, 3],
            "3-5-2": [1, 3, 5, 2]
        }

        filas =formaciones[formacion]
        posiciones = []

        for i, cantidad in enumerate(filas):
            x = base_x + direccion * i * 70
            for j in range(cantidad):
                y = (h / (cantidad + 1)) * (j + 1)
                posiciones.append((x,y))
        
        return posiciones
    
    def aplicar_formacion(self):
        # Limpiar cancha
        self.cancha.canvas.delete("all")
        self.cancha.dibujar_cancha()

        # Local
        posiciones_local = self.calcular_posciones(
            self.formacion.get(), lado="local"
        )

        for jugador, (x, y) in zip(
            self.narrador.partido.equipo_local.jugadores,
            posiciones_local
        ):
            jugador.x = x
            jugador.y = y
            self.cancha.dibujar_jugador(jugador, "#1976d2")

        # Visitante
        posiciones_visita = self.calcular_posciones(
            self.formacion.get(), lado="visitante"
        )

        for jugador, (x, y) in zip(
            self.narrador.partido.equipo_visitante.jugadores,
            posiciones_visita
        ):
            jugador.x = x
            jugador.y = y
            self.cancha.dibujar_jugador(jugador, "#d32f2f")