import customtkinter as ctk
import tkinter as tk
from src.utils.constantes import *
from src.logica.formaciones import GestorFormaciones

class CanchaWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLOR_FONDO_APP, **kwargs)
        
        estilo = ESTILOS_CANCHA["Pasto Clásico (Verde)"]
        self.color_fondo = estilo["fondo"]
        self.color_lineas = estilo["lineas"]
        
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=(10, 0), padx=20)
        
        self.lbl_competicion = ctk.CTkLabel(self.header, text="LIGA BETPLAY DIMAYOR", font=("Arial", 16, "bold"), text_color="#FFD54F")
        self.lbl_competicion.pack()
        self.lbl_estadio = ctk.CTkLabel(self.header, text="ESTADIO BELLO HORIZONTE", font=("Arial", 12), text_color="white")
        self.lbl_estadio.pack()
        
        self.frame_nombres = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_nombres.pack(fill="x", padx=20, pady=5)
        self.lbl_local = ctk.CTkLabel(self.frame_nombres, text="LOCAL", font=("Arial", 18, "bold"))
        self.lbl_local.pack(side="left")
        self.lbl_visita = ctk.CTkLabel(self.frame_nombres, text="VISITA", font=("Arial", 18, "bold"))
        self.lbl_visita.pack(side="right")

        self.canvas = tk.Canvas(self, bg=COLOR_FONDO_APP, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", pady=(0, 10), padx=20)
        
        self.frame_dt = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.frame_dt.pack(fill="x")
        self.lbl_dt_local = ctk.CTkLabel(self.frame_dt, text="DT Local", font=("Arial", 12, "bold"), text_color="white")
        self.lbl_dt_local.pack(side="left")
        self.lbl_dt_visita = ctk.CTkLabel(self.frame_dt, text="DT Visita", font=("Arial", 12, "bold"), text_color="white")
        self.lbl_dt_visita.pack(side="right")
        
        self.frame_sup = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.frame_sup.pack(fill="x")
        self.lbl_sup_local = ctk.CTkLabel(self.frame_sup, text="Suplentes...", font=("Arial", 9), text_color="gray")
        self.lbl_sup_local.pack(side="left")
        self.lbl_sup_visita = ctk.CTkLabel(self.frame_sup, text="Suplentes...", font=("Arial", 9), text_color="gray")
        self.lbl_sup_visita.pack(side="right")

        self.formacion_local, self.formacion_visita = None, None
        self.jugadores_local, self.jugadores_visita = [], []
        self.color_local = COLORES_EQUIPOS["Blanco y Dorado (Llaneros)"]
        self.color_visita = COLORES_EQUIPOS["Azul (Millonarios)"]

        self.on_click_jugador = None
        self.canvas.bind("<Configure>", self.al_redimensionar)
        
        self.canvas.tag_bind("jugador", "<Button-1>", self._on_clic_jugador)
        self.canvas.tag_bind("jugador", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("jugador", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def al_redimensionar(self, event):
        w, h = event.width, event.height
        if w > 1: self.dibujar_cancha(w, h)

    def dibujar_cancha(self, aw, ah):
        self.canvas.delete("all") 
        if aw <= 10 or ah <= 10: return
        
        proporcion = 1.54 
        if aw / ah > proporcion:
            ph = ah; pw = ph * proporcion
        else:
            pw = aw; ph = pw / proporcion
            
        ox = (aw - pw) / 2
        oy = (ah - ph) / 2

        self.dibujar_campo_base(pw, ph, ox, oy)
        
        if self.formacion_local:
            coords = GestorFormaciones.obtener_coordenadas_local(self.formacion_local, pw, ph)
            self._dibujar_fichas(coords, self.jugadores_local, self.color_local, ox, oy, "local")
            
        if self.formacion_visita:
            coords = GestorFormaciones.obtener_coordenadas_visitante(self.formacion_visita, pw, ph)
            self._dibujar_fichas(coords, self.jugadores_visita, self.color_visita, ox, oy, "visita")

    def dibujar_campo_base(self, pw, ph, ox, oy):
        cl = self.color_lineas
        self.canvas.create_rectangle(ox, oy, ox+pw, oy+ph, fill=self.color_fondo, outline=cl, width=3)
        cx, cy = ox + (pw/2), oy + (ph/2)
        self.canvas.create_line(cx, oy, cx, oy+ph, fill=cl, width=2)
        radio_centro = ph * 0.15
        self.canvas.create_oval(cx-radio_centro, cy-radio_centro, cx+radio_centro, cy+radio_centro, outline=cl, width=2)
        self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=cl)
        
        area_grande_h, area_grande_w = ph * 0.55, pw * 0.16
        area_chica_h, area_chica_w = ph * 0.25, pw * 0.055
        arco_h, prof, dist_penal, r_medialuna = ph * 0.12, pw * 0.02, pw * 0.11, ph * 0.13

        self.canvas.create_rectangle(ox, cy-(area_grande_h/2), ox+area_grande_w, cy+(area_grande_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox, cy-(area_chica_h/2), ox+area_chica_w, cy+(area_chica_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox-prof, cy-(arco_h/2), ox, cy+(arco_h/2), outline="#DDDDDD", width=2)
        self.canvas.create_oval(ox+dist_penal-3, cy-3, ox+dist_penal+3, cy+3, fill=cl)
        self.canvas.create_arc((ox+dist_penal-r_medialuna, cy-r_medialuna, ox+dist_penal+r_medialuna, cy+r_medialuna), start=-55, extent=110, style="arc", outline=cl, width=2)

        ox2 = ox + pw
        self.canvas.create_rectangle(ox2-area_grande_w, cy-(area_grande_h/2), ox2, cy+(area_grande_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox2-area_chica_w, cy-(area_chica_h/2), ox2, cy+(area_chica_h/2), outline=cl, width=2)
        self.canvas.create_rectangle(ox2, cy-(arco_h/2), ox2+prof, cy+(arco_h/2), outline="#DDDDDD", width=2)
        self.canvas.create_oval(ox2-dist_penal-3, cy-3, ox2-dist_penal+3, cy+3, fill=cl)
        self.canvas.create_arc((ox2-dist_penal-r_medialuna, cy-r_medialuna, ox2-dist_penal+r_medialuna, cy+r_medialuna), start=125, extent=110, style="arc", outline=cl, width=2)

    def _dibujar_fichas(self, coords, jugadores, config_color, ox, oy, tipo_equipo):
        r = RADIO_JUGADOR
        bg, fg = config_color["bg"], config_color["fg"]
        for i, info in enumerate(coords):
            x, y, pos = info if len(info) == 3 else (info[0], info[1], "")
            abs_x, abs_y = x + ox, y + oy
            
            if i < len(jugadores):
                nombre, numero = jugadores[i].get("nombre",""), jugadores[i].get("numero","")
            else:
                nombre, numero = f"J{i+1}", str(i+1)
            
            tag_ficha = f"ficha_{tipo_equipo}_{i}"
            todas_tags = (tag_ficha, "jugador")
            
            # --- NUEVO: GEOMETRÍA DE LA CAMISETA ---
            pts_camiseta = [
                (abs_x - r*0.35, abs_y - r*0.9), # cuello izq
                (abs_x + r*0.35, abs_y - r*0.9), # cuello der
                (abs_x + r*0.8,  abs_y - r*0.6), # hombro der
                (abs_x + r*1.2,  abs_y - r*0.1), # manga der ext
                (abs_x + r*0.8,  abs_y + r*0.2), # axila der
                (abs_x + r*0.7,  abs_y + r*1.0), # cintura der
                (abs_x - r*0.7,  abs_y + r*1.0), # cintura izq
                (abs_x - r*0.8,  abs_y + r*0.2), # axila izq
                (abs_x - r*1.2,  abs_y - r*0.1), # manga izq ext
                (abs_x - r*0.8,  abs_y - r*0.6), # hombro izq
            ]
            
            # Sombra y forma de camiseta
            sombra_pts = [(px+2, py+2) for px, py in pts_camiseta]
            self.canvas.create_polygon(sombra_pts, fill="#111111", outline="", tags=todas_tags) 
            self.canvas.create_polygon(pts_camiseta, fill=bg, outline=fg, width=2, tags=todas_tags)
            
            # Número un poco más arriba para que cuadre en el "pecho"
            self.canvas.create_text(abs_x, abs_y + r*0.1, text=str(numero), fill=fg, font=("Arial", int(r*0.6), "bold"), tags=todas_tags) 
            
            if pos: self.canvas.create_text(abs_x, abs_y-r-10, text=pos, fill="#FFD54F", font=("Arial", 9, "bold"), tags=todas_tags)
            self.canvas.create_rectangle(abs_x-20, abs_y+r+5, abs_x+20, abs_y+r+20, fill="#222222", outline="", tags=todas_tags)
            self.canvas.create_text(abs_x, abs_y+r+13, text=nombre, fill="white", font=("Arial", 8, "bold"), tags=todas_tags)

    def _on_clic_jugador(self, event):
        if not self.on_click_jugador: return
        items = self.canvas.find_withtag("current")
        if not items: return
        tags = self.canvas.gettags(items[0])
        for t in tags:
            if t.startswith("ficha_"):
                _, tipo, indice = t.split("_")
                self.on_click_jugador(tipo, int(indice))
                break

    def cambiar_estilo_cancha(self, color_fondo, color_lineas):
        self.color_fondo, self.color_lineas = color_fondo, color_lineas
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def actualizar_datos(self, tipo, formacion, data_equipo, color_clave):
        color_data = COLORES_EQUIPOS[color_clave]
        str_sup = " | ".join([f"{s.get('numero','')} {s.get('nombre','')}" for s in data_equipo.get("suplentes",[]) if s.get('nombre')])
        
        if tipo == "local":
            self.formacion_local, self.jugadores_local = formacion, data_equipo["jugadores"]
            self.color_local = color_data
            self.lbl_local.configure(text=self.nombre_local, text_color=color_data["bg"])
            self.lbl_dt_local.configure(text=f"DT: {data_equipo['tecnico'].upper()}")
            self.lbl_sup_local.configure(text=f"Suplentes: {str_sup}" if str_sup else "Sin suplentes")
        else:
            self.formacion_visita, self.jugadores_visita = formacion, data_equipo["jugadores"]
            self.color_visita = color_data
            self.lbl_visita.configure(text=self.nombre_visita, text_color=color_data["bg"])
            self.lbl_dt_visita.configure(text=f"DT: {data_equipo['tecnico'].upper()}")
            self.lbl_sup_visita.configure(text=f"Suplentes: {str_sup}" if str_sup else "Sin suplentes")
            
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def actualizar_entorno(self, competicion, n_estadio, n_local, n_visita):
        self.nombre_local, self.nombre_visita = n_local, n_visita
        self.lbl_competicion.configure(text=competicion)
        self.lbl_estadio.configure(text=n_estadio)