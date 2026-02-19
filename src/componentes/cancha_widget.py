import customtkinter as ctk
import tkinter as tk
from src.utils.constantes import *
from src.logica.formaciones import GestorFormaciones

class CanchaWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        estilo_inicial = ESTILOS_CANCHA["Pasto Clásico (Verde)"]
        self.color_fondo = estilo_inicial["fondo"]
        self.color_lineas = estilo_inicial["lineas"]
        
        # El canvas ahora tiene el color oscuro de la app, el pasto lo dibujaremos adentro
        self.canvas = tk.Canvas(self, bg=COLOR_FONDO_APP, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.formacion_local = None
        self.formacion_visita = None
        self.nombres_jugadores_local = []
        self.nombres_jugadores_visita = []
        
        self.color_local = COLORES_EQUIPOS["Celeste / Blanco (Arg)"]
        self.color_visita = COLORES_EQUIPOS["Blanco (Madrid)"]
        
        self.nombre_equipo_local = "EQUIPO IZQUIERDA"
        self.nombre_equipo_visita = "EQUIPO DERECHA"
        self.nombre_estadio = "ESTADIO MONUMENTAL"

        self.canvas.bind("<Configure>", self.al_redimensionar)

    def al_redimensionar(self, event):
        w, h = event.width, event.height
        if w > 1: self.dibujar_todo(w, h)

    def dibujar_todo(self, aw, ah):
        self.canvas.delete("all") 
        
        # --- 1. CÁLCULO DE PROPORCIÓN PERFECTA ---
        # Dejamos espacio arriba para los nombres (12%) y abajo para margen (5%)
        margen_top = ah * 0.12
        margen_bot = ah * 0.05
        espacio_w = aw * 0.95 # Dejamos 2.5% de margen a cada lado
        espacio_h = ah - margen_top - margen_bot
        
        if espacio_h <= 0 or espacio_w <= 0: return
        
        # Proporción real estándar de una cancha (ej. 105m x 68m = ~1.54)
        proporcion = 1.54 
        
        if espacio_w / espacio_h > proporcion:
            # La ventana es muy ancha: la altura manda
            ph = espacio_h
            pw = ph * proporcion
        else:
            # La ventana es muy alta/cuadrada: el ancho manda
            pw = espacio_w
            ph = pw / proporcion
            
        # Coordenadas de inicio para centrar la cancha en la pantalla
        ox = (aw - pw) / 2
        oy = margen_top + (espacio_h - ph) / 2

        # --- 2. DIBUJAR NOMBRES AFUERA DE LA CANCHA ---
        # Estadio (Centro Arriba)
        self.canvas.create_text(aw/2, margen_top * 0.35, text=self.nombre_estadio, 
                               fill="white", font=("Arial", int(ah*0.035), "bold"))
        # Equipos (Lados, alineados con los bordes de la cancha)
        self.canvas.create_text(ox, margen_top * 0.8, text=self.nombre_equipo_local, 
                               fill=self.color_local["bg"], font=("Arial", int(ah*0.045), "bold"), anchor="w")
        self.canvas.create_text(ox + pw, margen_top * 0.8, text=self.nombre_equipo_visita, 
                               fill=self.color_visita["bg"], font=("Arial", int(ah*0.045), "bold"), anchor="e")

        # --- 3. DIBUJAR CANCHA Y JUGADORES ---
        self.dibujar_campo_base(pw, ph, ox, oy)
        
        if self.formacion_local:
            coords = GestorFormaciones.obtener_coordenadas_local(self.formacion_local, pw, ph)
            self._dibujar_fichas(coords, self.nombres_jugadores_local, self.color_local, ox, oy)
            
        if self.formacion_visita:
            coords = GestorFormaciones.obtener_coordenadas_visitante(self.formacion_visita, pw, ph)
            self._dibujar_fichas(coords, self.nombres_jugadores_visita, self.color_visita, ox, oy)

    def dibujar_campo_base(self, pw, ph, ox, oy):
        cl = self.color_lineas
        
        # Rectángulo Verde (Pasto)
        self.canvas.create_rectangle(ox, oy, ox+pw, oy+ph, fill=self.color_fondo, outline=cl, width=3)
        
        # Línea Central y Círculo
        cx = ox + (pw/2)
        self.canvas.create_line(cx, oy, cx, oy+ph, fill=cl, width=2)
        radio_centro = ph * 0.15
        cy = oy + (ph/2)
        self.canvas.create_oval(cx-radio_centro, cy-radio_centro, cx+radio_centro, cy+radio_centro, outline=cl, width=2)
        self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=cl)
        
        # Medidas estándar de áreas
        area_grande_h = ph * 0.55
        area_grande_w = pw * 0.16
        area_chica_h = ph * 0.25
        area_chica_w = pw * 0.055
        arco_h = ph * 0.12
        prof = pw * 0.02
        dist_penal = pw * 0.11
        r_medialuna = ph * 0.13

        # Lado Izquierdo
        self.canvas.create_rectangle(ox, cy-(area_grande_h/2), ox+area_grande_w, cy+(area_grande_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox, cy-(area_chica_h/2), ox+area_chica_w, cy+(area_chica_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox-prof, cy-(arco_h/2), ox, cy+(arco_h/2), outline="#DDDDDD", width=2)
        self.canvas.create_oval(ox+dist_penal-3, cy-3, ox+dist_penal+3, cy+3, fill=cl)
        bbox_izq = (ox+dist_penal-r_medialuna, cy-r_medialuna, ox+dist_penal+r_medialuna, cy+r_medialuna)
        self.canvas.create_arc(bbox_izq, start=-55, extent=110, style="arc", outline=cl, width=2)

        # Lado Derecho
        ox2 = ox + pw
        self.canvas.create_rectangle(ox2-area_grande_w, cy-(area_grande_h/2), ox2, cy+(area_grande_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox2-area_chica_w, cy-(area_chica_h/2), ox2, cy+(area_chica_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox2, cy-(arco_h/2), ox2+prof, cy+(arco_h/2), outline="#DDDDDD", width=2)
        self.canvas.create_oval(ox2-dist_penal-3, cy-3, ox2-dist_penal+3, cy+3, fill=cl)
        bbox_der = (ox2-dist_penal-r_medialuna, cy-r_medialuna, ox2-dist_penal+r_medialuna, cy+r_medialuna)
        self.canvas.create_arc(bbox_der, start=125, extent=110, style="arc", outline=cl, width=2)

        # Córners
        r_corner = pw * 0.02
        self.canvas.create_arc(ox-r_corner, oy-r_corner, ox+r_corner, oy+r_corner, start=270, extent=90, style="arc", outline=cl, width=2)
        self.canvas.create_arc(ox2-r_corner, oy-r_corner, ox2+r_corner, oy+r_corner, start=180, extent=90, style="arc", outline=cl, width=2)
        self.canvas.create_arc(ox-r_corner, oy+ph-r_corner, ox+r_corner, oy+ph+r_corner, start=0, extent=90, style="arc", outline=cl, width=2)
        self.canvas.create_arc(ox2-r_corner, oy+ph-r_corner, ox2+r_corner, oy+ph+r_corner, start=90, extent=90, style="arc", outline=cl, width=2)

    def _dibujar_fichas(self, coords, nombres, config_color, ox, oy):
        r = RADIO_JUGADOR
        bg = config_color["bg"]
        fg = config_color["fg"]
        for i, (x, y) in enumerate(coords):
            abs_x = x + ox
            abs_y = y + oy
            nombre = nombres[i] if i < len(nombres) else f"J{i+1}"
            
            self.canvas.create_oval(abs_x-r+2, abs_y-r+2, abs_x+r+2, abs_y+r+2, fill="#111111", outline="") 
            self.canvas.create_oval(abs_x-r, abs_y-r, abs_x+r, abs_y+r, fill=bg, outline=fg, width=2)
            self.canvas.create_text(abs_x, abs_y, text=str(i+1), fill=fg, font=("Arial", 10, "bold")) 
            self.canvas.create_rectangle(abs_x-20, abs_y+r+5, abs_x+20, abs_y+r+20, fill="#222222", outline="")
            self.canvas.create_text(abs_x, abs_y+r+13, text=nombre, fill="white", font=("Arial", 8, "bold"))

    def cambiar_estilo_cancha(self, color_fondo, color_lineas):
        self.color_fondo = color_fondo
        self.color_lineas = color_lineas
        self._forzar_redibujo()

    def actualizar_equipo(self, tipo, formacion, nombres, color_clave):
        color_data = COLORES_EQUIPOS[color_clave]
        if tipo == "local":
            self.formacion_local = formacion
            self.nombres_jugadores_local = nombres
            self.color_local = color_data
        else:
            self.formacion_visita = formacion
            self.nombres_jugadores_visita = nombres
            self.color_visita = color_data
        self._forzar_redibujo()

    def actualizar_nombres_equipos(self, n_local, n_visita, n_estadio):
        self.nombre_equipo_local = n_local
        self.nombre_equipo_visita = n_visita
        self.nombre_estadio = n_estadio
        self._forzar_redibujo()

    def _forzar_redibujo(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1: self.dibujar_todo(w, h)