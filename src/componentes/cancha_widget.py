import customtkinter as ctk
import tkinter as tk
from PIL import ImageGrab 
from src.utils.constantes import COLOR_FONDO_APP, COLOR_PANEL, COLOR_TEXTO_SEC, COLOR_ACENTO_AZUL, ESTILOS_CANCHA, RADIO_JUGADOR
from src.logica.formaciones import GestorFormaciones

class CanchaWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        ctk.CTkFrame.__init__(self, master=master, fg_color="transparent", **kwargs)
        
        estilo = ESTILOS_CANCHA["Pasto Clásico (Verde)"]
        self.color_fondo = estilo["fondo"]
        self.color_lineas = estilo["lineas"]
        
        self.header = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=12)
        self.header.pack(fill="x", pady=(0, 10))
        self.header.grid_columnconfigure((0, 2), weight=1)
        self.header.grid_columnconfigure(1, weight=2)
        
        self.lbl_local = ctk.CTkLabel(self.header, text="LOCAL", font=("Arial", 22, "bold"))
        self.lbl_local.grid(row=0, column=0, rowspan=2, sticky="e", padx=20, pady=10)
        
        self.lbl_competicion = ctk.CTkLabel(self.header, text="LIGA BETPLAY", font=("Arial", 12, "bold"), text_color=COLOR_ACENTO_AZUL)
        self.lbl_competicion.grid(row=0, column=1, pady=(10, 0))
        self.lbl_estadio = ctk.CTkLabel(self.header, text="ESTADIO", font=("Arial", 10), text_color=COLOR_TEXTO_SEC)
        self.lbl_estadio.grid(row=1, column=1, pady=(0, 10))
        
        self.lbl_visita = ctk.CTkLabel(self.header, text="VISITA", font=("Arial", 22, "bold"))
        self.lbl_visita.grid(row=0, column=2, rowspan=2, sticky="w", padx=20, pady=10)

        self.frame_canvas = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=12)
        self.frame_canvas.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_canvas, bg=COLOR_FONDO_APP, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", pady=(10, 0))
        
        self.frame_dt = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.frame_dt.pack(fill="x")
        self.lbl_dt_local = ctk.CTkLabel(self.frame_dt, text="DT Local", font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC)
        self.lbl_dt_local.pack(side="left")
        self.lbl_dt_visita = ctk.CTkLabel(self.frame_dt, text="DT Visita", font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC)
        self.lbl_dt_visita.pack(side="right")
        
        self.frame_sup = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.frame_sup.pack(fill="x")
        self.lbl_sup_local = ctk.CTkLabel(self.frame_sup, text="Suplentes...", font=("Arial", 9), text_color=COLOR_TEXTO_SEC)
        self.lbl_sup_local.pack(side="left")
        self.lbl_sup_visita = ctk.CTkLabel(self.frame_sup, text="Suplentes...", font=("Arial", 9), text_color=COLOR_TEXTO_SEC)
        self.lbl_sup_visita.pack(side="right")

        self.formacion_local, self.formacion_visita = None, None
        self.jugadores_local, self.jugadores_visita = [], []
        self.color_local = {"bg": "#FFFFFF", "fg": "#000000"}
        self.color_visita = {"bg": "#111111", "fg": "#FFFFFF"}
        
        # --- VARIABLES INDEPENDIENTES DE ESCALA ---
        self.escala_jugadores = 1.0  # Para la camiseta
        self.escala_textos = 1.0     # Para las letras
        self.historial_trazos = []

        self.modo_interaccion = "mover" 
        self.item_arrastrado = ""
        self.linea_actual = 0
        self.start_x = self.start_y = 0
        self.last_x = self.last_y = 0
        self.on_click_jugador = lambda tipo, indice: None
        
        self.canvas.bind("<Configure>", self.al_redimensionar)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.tag_bind("jugador", "<Enter>", lambda e: self.canvas.config(cursor="hand2") if self.modo_interaccion == "mover" else None)
        self.canvas.tag_bind("jugador", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def cambiar_modo(self, modo):
        self.modo_interaccion = modo
        if modo == "dibujar": self.canvas.config(cursor="pencil")
        else: self.canvas.config(cursor="")

    def limpiar_trazos(self):
        self.canvas.delete("trazo")
        self.historial_trazos.clear()

    def deshacer_trazo(self):
        if self.historial_trazos:
            ultimo = self.historial_trazos.pop()
            self.canvas.delete(ultimo)
            return True
        return False

    def _on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.last_x, self.last_y = event.x, event.y
        if self.modo_interaccion == "dibujar":
            self.linea_actual = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="#FFEA00", width=4, arrow=tk.LAST, arrowshape=(16,20,6), tags="trazo")
        elif self.modo_interaccion == "mover":
            items = self.canvas.find_withtag("current")
            if items and "jugador" in self.canvas.gettags(items[0]):
                tags = self.canvas.gettags(items[0])
                for t in tags:
                    if t.startswith("ficha_"):
                        self.item_arrastrado = t
                        self.canvas.tag_raise(t) 
                        break

    def _on_drag(self, event):
        if self.modo_interaccion == "dibujar" and self.linea_actual:
            self.canvas.coords(self.linea_actual, self.start_x, self.start_y, event.x, event.y)
        elif self.modo_interaccion == "mover" and self.item_arrastrado:
            dx, dy = event.x - self.last_x, event.y - self.last_y
            self.canvas.move(self.item_arrastrado, dx, dy)
            self.last_x, self.last_y = event.x, event.y

    def _on_release(self, event):
        if self.modo_interaccion == "mover" and self.item_arrastrado:
            distancia = abs(event.x - self.start_x) + abs(event.y - self.start_y)
            if distancia < 5 and self.on_click_jugador:
                try:
                    _, tipo, indice = self.item_arrastrado.split("_")
                    self.on_click_jugador(tipo, int(indice))
                except ValueError:
                    pass
            self.item_arrastrado = ""
        elif self.modo_interaccion == "dibujar":
            if self.linea_actual:
                self.historial_trazos.append(self.linea_actual)
            self.linea_actual = 0

    def exportar_imagen(self, ruta_archivo):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        x1 = x + self.winfo_width()
        y1 = y + self.winfo_height()
        try:
            imagen = ImageGrab.grab(bbox=(x, y, x1, y1))
            imagen.save(ruta_archivo)
            return True
        except Exception as e: return False

    def al_redimensionar(self, event):
        w, h = event.width, event.height
        if w > 1: self.dibujar_cancha(w, h)

    def dibujar_cancha(self, aw, ah):
        self.canvas.delete("all") 
        if aw <= 10 or ah <= 10: return
        proporcion = 1.54 
        if aw / ah > proporcion: ph = ah; pw = ph * proporcion
        else: pw = aw; ph = pw / proporcion
        ox, oy = (aw - pw) / 2, (ah - ph) / 2
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

    def _dibujar_fichas(self, coords, jugadores, color_dict, ox, oy, tipo_equipo):
        # RADIO CAMISETA (Controlado por slider de herramientas)
        r = RADIO_JUGADOR * self.escala_jugadores 
        
        # TAMAÑO FUENTE (Controlado por Ajustes)
        t_num = max(6, int(11 * self.escala_textos))
        t_nom = max(6, int(9 * self.escala_textos))
        t_pos = max(6, int(10 * self.escala_textos))

        bg, fg = color_dict.get("bg", "#FFF"), color_dict.get("fg", "#000")
        for i, info in enumerate(coords):
            x, y, pos = info if len(info) == 3 else (info[0], info[1], "")
            abs_x, abs_y = x + ox, y + oy
            
            if i < len(jugadores): nombre, numero = jugadores[i].get("nombre",""), jugadores[i].get("numero","")
            else: nombre, numero = f"J{i+1}", str(i+1)
            
            tag_ficha = f"ficha_{tipo_equipo}_{i}"
            todas_tags = (tag_ficha, "jugador")
            
            pts_camiseta = [
                (abs_x - r*0.35, abs_y - r*0.9), (abs_x + r*0.35, abs_y - r*0.9), 
                (abs_x + r*0.8,  abs_y - r*0.6), (abs_x + r*1.2,  abs_y - r*0.1), 
                (abs_x + r*0.8,  abs_y + r*0.2), (abs_x + r*0.7,  abs_y + r*1.0), 
                (abs_x - r*0.7,  abs_y + r*1.0), (abs_x - r*0.8,  abs_y + r*0.2), 
                (abs_x - r*1.2,  abs_y - r*0.1), (abs_x - r*0.8,  abs_y - r*0.6)
            ]
            sombra_pts = [(px+(2*self.escala_jugadores), py+(2*self.escala_jugadores)) for px, py in pts_camiseta]
            self.canvas.create_polygon(sombra_pts, fill="#111111", outline="", tags=todas_tags) 
            self.canvas.create_polygon(pts_camiseta, fill=bg, outline=fg, width=max(1, int(2*self.escala_jugadores)), tags=todas_tags)
            
            # Textos no crecen con la camiseta, solo bajan para no ser tapados
            self.canvas.create_text(abs_x, abs_y + r*0.1, text=str(numero), fill=fg, font=("Arial", t_num, "bold"), tags=todas_tags) 
            if pos: self.canvas.create_text(abs_x, abs_y-r-10, text=pos, fill="#FFD54F", font=("Arial", t_pos, "bold"), tags=todas_tags)
            
            # Etiqueta de nombre dinámica según el tamaño de la letra
            ancho_caja = 25 * self.escala_textos
            alto_caja = 18 * self.escala_textos
            offset_y = abs_y + r + 5
            
            self.canvas.create_rectangle(abs_x - ancho_caja, offset_y, abs_x + ancho_caja, offset_y + alto_caja, fill="#1A1D27", outline="", tags=todas_tags)
            self.canvas.create_text(abs_x, offset_y + (alto_caja/2), text=nombre, fill="white", font=("Arial", t_nom, "bold"), tags=todas_tags)

    def cambiar_escala_jugadores(self, nueva_escala):
        self.escala_jugadores = nueva_escala
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def cambiar_escala_textos(self, nueva_escala):
        self.escala_textos = nueva_escala
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def cambiar_estilo_cancha(self, color_fondo, color_lineas):
        self.color_fondo, self.color_lineas = color_fondo, color_lineas
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def actualizar_datos(self, tipo, formacion, data_equipo, color_dict):
        str_sup = " | ".join([f"{s.get('numero','')} {s.get('nombre','')}" for s in data_equipo.get("suplentes",[]) if s.get('nombre')])
        
        if tipo == "local":
            self.formacion_local, self.jugadores_local, self.color_local = formacion, data_equipo["jugadores"], color_dict
            self.lbl_local.configure(text=self.nombre_local, text_color=color_dict.get("bg", "#FFF"))
            self.lbl_dt_local.configure(text=f"DT: {data_equipo['tecnico'].upper()}")
            self.lbl_sup_local.configure(text=f"Suplentes: {str_sup}" if str_sup else "Sin suplentes")
        else:
            self.formacion_visita, self.jugadores_visita, self.color_visita = formacion, data_equipo["jugadores"], color_dict
            self.lbl_visita.configure(text=self.nombre_visita, text_color=color_dict.get("bg", "#FFF"))
            self.lbl_dt_visita.configure(text=f"DT: {data_equipo['tecnico'].upper()}")
            self.lbl_sup_visita.configure(text=f"Suplentes: {str_sup}" if str_sup else "Sin suplentes")
            
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1: self.dibujar_cancha(w, h)

    def actualizar_entorno(self, competicion, n_estadio, n_local, n_visita):
        self.nombre_local, self.nombre_visita = n_local, n_visita
        self.lbl_competicion.configure(text=competicion)
        self.lbl_estadio.configure(text=n_estadio)