import customtkinter as ctk
import tkinter as tk
from src.utils.constantes import *
from src.logica.formaciones import GestorFormaciones

class CanchaWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Canvas sin tamaño fijo inicial (se ajustará con pack/grid)
        self.canvas = tk.Canvas(
            self, bg=COLOR_CESPED, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)
        
        # --- ESTADO (Memoria) ---
        # Guardamos qué se está mostrando para poder redibujarlo al cambiar el tamaño
        self.formacion_local = None
        self.formacion_visita = None
        self.nombres_jugadores_local = []
        self.nombres_jugadores_visita = []
        self.nombre_equipo_local = "LOCAL"
        self.nombre_equipo_visita = "VISITANTE"

        # EVENTO CLAVE: Cuando cambia el tamaño, ejecutamos 'al_redimensionar'
        self.canvas.bind("<Configure>", self.al_redimensionar)

    def al_redimensionar(self, event):
        """Se ejecuta automáticamente al estirar la ventana"""
        w, h = event.width, event.height
        self.dibujar_todo(w, h)

    def dibujar_todo(self, w, h):
        self.canvas.delete("all") # Borrón y cuenta nueva
        self.dibujar_campo_base(w, h)
        
        # Redibujar equipos si existen
        if self.formacion_local:
            coords = GestorFormaciones.obtener_coordenadas_local(self.formacion_local, w, h)
            self._dibujar_fichas(coords, self.nombres_jugadores_local, COLOR_FICHA_LOCAL)
            
        if self.formacion_visita:
            coords = GestorFormaciones.obtener_coordenadas_visitante(self.formacion_visita, w, h)
            self._dibujar_fichas(coords, self.nombres_jugadores_visita, COLOR_FICHA_VISITANTE)

        # Redibujar Nombres de Equipos (escalados)
        font_size = int(h * 0.04) # Fuente dinámica
        self.canvas.create_text(w * 0.25, h * 0.05, text=self.nombre_equipo_local, 
                               fill=COLOR_FICHA_LOCAL, font=("Arial", font_size, "bold"))
        self.canvas.create_text(w * 0.75, h * 0.05, text=self.nombre_equipo_visita, 
                               fill=COLOR_FICHA_VISITANTE, font=("Arial", font_size, "bold"))

    def dibujar_campo_base(self, w, h):
        # Márgenes dinámicos
        mx = w * 0.05
        my = h * 0.08
        
        # Rectángulo de juego
        self.canvas.create_rectangle(mx, my, w-mx, h-my, outline=COLOR_LINEAS, width=3)
        # Línea central
        self.canvas.create_line(w/2, my, w/2, h-my, fill=COLOR_LINEAS, width=2)
        # Círculo central
        radio_centro = h * 0.12
        self.canvas.create_oval((w/2)-radio_centro, (h/2)-radio_centro, (w/2)+radio_centro, (h/2)+radio_centro, outline=COLOR_LINEAS, width=2)
        
        # Áreas (Simplificadas para escalar bien)
        area_h = h * 0.45
        area_w = w * 0.15
        
        # Área Local
        self.canvas.create_rectangle(mx, (h/2)-(area_h/2), mx+area_w, (h/2)+(area_h/2), outline=COLOR_LINEAS, width=2)
        # Área Visita
        self.canvas.create_rectangle(w-mx-area_w, (h/2)-(area_h/2), w-mx, (h/2)+(area_h/2), outline=COLOR_LINEAS, width=2)

    def _dibujar_fichas(self, coords, nombres, color):
        r = RADIO_JUGADOR
        for i, (x, y) in enumerate(coords):
            nombre = nombres[i] if i < len(nombres) else f"J{i+1}"
            
            # Ficha
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=2)
            # Número
            self.canvas.create_text(x, y, text=str(i+1), fill="white", font=("Arial", 10, "bold"))
            # Nombre
            self.canvas.create_text(x, y+r+12, text=nombre, fill="white", font=("Arial", 9, "bold"))

    # --- MÉTODOS PÚBLICOS (Llamados desde main.py) ---
    def actualizar_equipo(self, tipo, formacion, nombres):
        """Guarda la configuración y fuerza un redibujado"""
        if tipo == "local":
            self.formacion_local = formacion
            self.nombres_jugadores_local = nombres
        else:
            self.formacion_visita = formacion
            self.nombres_jugadores_visita = nombres
            
        # Forzamos redibujar con el tamaño actual
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # Pequeño hack: si w es 1 (al iniciar), esperamos
        if w > 1: self.dibujar_todo(w, h)

    def actualizar_nombres_equipos(self, n_local, n_visita):
        self.nombre_equipo_local = n_local
        self.nombre_equipo_visita = n_visita
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1: self.dibujar_todo(w, h)