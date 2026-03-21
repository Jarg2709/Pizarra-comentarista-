import os
import ctypes 
from datetime import datetime
from tkinter import filedialog 
import customtkinter as ctk
from src.componentes.cancha_widget import CanchaWidget
from src.utils.constantes import *
from src.logica.gestor_equipos import GestorEquipos

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppNarrador(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Narrador Pro - FPC 2026")
        self.configure(fg_color=COLOR_FONDO_APP)
        self.centrar_y_poner_logo(self, 1350, 850) 
        self.db = GestorEquipos()

        self.segundos = 0
        self.cronometro_activo = False
        
        self.data_local = {"jugadores": [], "suplentes": [], "tecnico": ""}
        self.data_visita = {"jugadores": [], "suplentes": [], "tecnico": ""}

        # --- ESTRUCTURA DE COLUMNAS ---
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 
        self.grid_rowconfigure(0, weight=1)

        # 1. ZONA IZQUIERDA (Exclusiva para la Cancha)
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(15, 10), pady=15)
        self.frame_izquierdo.grid_columnconfigure(0, weight=1) 
        self.frame_izquierdo.grid_rowconfigure(0, weight=1) 

        self.mi_cancha = CanchaWidget(master=self.frame_izquierdo)
        self.mi_cancha.grid(row=0, column=0, sticky="nsew")
        self.mi_cancha.on_click_jugador = self.abrir_menu_sustitucion

        # 2. PANEL DERECHO (Controles y Eventos fijos) - Ancho aumentado para la Scrollbar
        self.panel_derecho = ctk.CTkFrame(self, fg_color="transparent", width=360)
        self.panel_derecho.grid(row=0, column=1, sticky="ns", padx=(5, 15), pady=15)
        self.panel_derecho.grid_propagate(False)

        # --- CAJA DE EVENTOS (Fija abajo) ---
        self.frame_log = ctk.CTkFrame(self.panel_derecho, fg_color=COLOR_PANEL, corner_radius=12, height=140)
        self.frame_log.pack(side="bottom", fill="x", pady=(10, 0))
        self.frame_log.pack_propagate(False) 
        
        ctk.CTkLabel(self.frame_log, text="📝 LIVE TICKETS / EVENTOS", font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC).pack(anchor="w", padx=15, pady=(10, 0))
        self.caja_eventos = ctk.CTkTextbox(self.frame_log, font=("Consolas", 11), fg_color=COLOR_FONDO_APP, text_color="#A9A9B5")
        self.caja_eventos.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.caja_eventos.configure(state="disabled")

        self.construir_panel()

    def centrar_y_poner_logo(self, ventana, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho / 2) - (ancho / 2))
        y = int((pantalla_alto / 2) - (alto / 2))
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        ruta_icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icono.ico")
        try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('narrador.pro.v26')
        except: pass
        if os.path.exists(ruta_icono):
            try: ventana.iconbitmap(ruta_icono)
            except: pass
            ventana.after(50, lambda: ventana.iconbitmap(ruta_icono))

    def registrar_evento(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        texto = f"[{hora}] {mensaje}\n"
        self.caja_eventos.configure(state="normal")
        self.caja_eventos.insert("end", texto)
        self.caja_eventos.see("end")
        self.caja_eventos.configure(state="disabled")

    def crear_tarjeta(self, parent, titulo):
        tarjeta = ctk.CTkFrame(parent, fg_color=COLOR_PANEL, corner_radius=12)
        tarjeta.pack(fill="x", pady=(0, 15))
        if titulo:
            ctk.CTkLabel(tarjeta, text=titulo, font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC).pack(anchor="w", padx=15, pady=(10, 5))
        return tarjeta

    def construir_panel(self):
        scroll_panel = ctk.CTkScrollableFrame(self.panel_derecho, fg_color="transparent")
        scroll_panel.pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(scroll_panel, text="Control Táctico FPC", font=("Arial", 20, "bold")).pack(pady=(5, 15))

        # --- 1. CRONÓMETRO ---
        card_crono = self.crear_tarjeta(scroll_panel, "⏱️ TIEMPO EN VIVO")
        self.lbl_crono = ctk.CTkLabel(card_crono, text="00:00", font=("Consolas", 36, "bold"), text_color=COLOR_ACENTO_VERDE)
        self.lbl_crono.pack(pady=(0, 5))
        frame_btn_crono = ctk.CTkFrame(card_crono, fg_color="transparent")
        frame_btn_crono.pack(pady=(0, 15))
        self.btn_play = ctk.CTkButton(frame_btn_crono, text="▶️", width=50, fg_color="#2E7D32", hover_color="#1B5E20", command=self.toggle_cronometro)
        self.btn_play.pack(side="left", padx=5)
        ctk.CTkButton(frame_btn_crono, text="🔄", width=50, fg_color=COLOR_ACENTO_ROJO, hover_color="#C62828", command=self.reset_cronometro).pack(side="left", padx=5)

        # --- 2. ENTORNO DEL PARTIDO ---
        card_entorno = self.crear_tarjeta(scroll_panel, "🏟️ ENTORNO DEL PARTIDO")
        self.combo_competicion = ctk.CTkComboBox(card_entorno, values=["LIGA BETPLAY DIMAYOR", "COPA BETPLAY DIMAYOR"], command=self.actualizar_todo, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_competicion.set("LIGA BETPLAY DIMAYOR")
        self.combo_competicion.pack(pady=5, padx=15, fill="x")

        self.entry_estadio = ctk.CTkEntry(card_entorno, placeholder_text="Nombre del Estadio", border_color=COLOR_FONDO_APP)
        self.entry_estadio.pack(pady=5, padx=15, fill="x")

        self.combo_estilo = ctk.CTkComboBox(card_entorno, values=list(ESTILOS_CANCHA.keys()), command=self.cambiar_tema_cancha, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_estilo.set("Pasto Clásico (Verde)")
        self.combo_estilo.pack(pady=(5, 15), padx=15, fill="x")

        # --- PREPARACIÓN DE EQUIPOS ---
        lista_equipos = list(self.db.equipos.keys())

        # --- 3. EQUIPO LOCAL ---
        card_local = self.crear_tarjeta(scroll_panel, "⬅️ EQUIPO LOCAL")
        self.combo_equipo_local = ctk.CTkComboBox(card_local, values=lista_equipos, command=self.cargar_equipo_local, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_equipo_local.set("LLANEROS FC" if "LLANEROS FC" in lista_equipos else lista_equipos[0])
        self.combo_equipo_local.pack(pady=5, padx=15, fill="x")
        self.combo_color_local = ctk.CTkComboBox(card_local, values=[], command=self.actualizar_todo, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_color_local.pack(pady=5, padx=15, fill="x")
        self.combo_formacion_local = ctk.CTkComboBox(card_local, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1"], command=self.actualizar_todo, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_formacion_local.set("4-2-3-1")
        self.combo_formacion_local.pack(pady=(5,15), padx=15, fill="x")

        # --- 4. EQUIPO VISITA ---
        card_visita = self.crear_tarjeta(scroll_panel, "➡️ EQUIPO VISITA")
        self.combo_equipo_visita = ctk.CTkComboBox(card_visita, values=lista_equipos, command=self.cargar_equipo_visita, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_equipo_visita.set("MILLONARIOS FC" if "MILLONARIOS FC" in lista_equipos else lista_equipos[-1])
        self.combo_equipo_visita.pack(pady=5, padx=15, fill="x")
        self.combo_color_visita = ctk.CTkComboBox(card_visita, values=[], command=self.actualizar_todo, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_color_visita.pack(pady=5, padx=15, fill="x")
        self.combo_formacion_visita = ctk.CTkComboBox(card_visita, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2", "5-3-2", "4-1-4-1"], command=self.actualizar_todo, state="readonly", border_color=COLOR_FONDO_APP)
        self.combo_formacion_visita.set("4-3-3")
        self.combo_formacion_visita.pack(pady=(5,15), padx=15, fill="x")

        # --- 5. CAMBIAR LADOS ---
        ctk.CTkButton(scroll_panel, text="⇅ CAMBIAR LADOS ⇅", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", font=("Arial", 12, "bold"), command=self.intercambiar_lados).pack(pady=(0, 15), padx=15, fill="x")

        # --- 6. HERRAMIENTAS Y CAMISETAS ---
        card_herramientas = self.crear_tarjeta(scroll_panel, "🛠️ HERRAMIENTAS Y CAMISETAS")
        self.modo_var = ctk.StringVar(value="mover")
        ctk.CTkRadioButton(card_herramientas, text="🤚 Mover/Sustituir", variable=self.modo_var, value="mover", command=self.cambiar_modo_cancha).pack(pady=5, anchor="w", padx=20)
        ctk.CTkRadioButton(card_herramientas, text="🖍️ Dibujar Flechas", variable=self.modo_var, value="dibujar", command=self.cambiar_modo_cancha).pack(pady=5, anchor="w", padx=20)
        
        ctk.CTkLabel(card_herramientas, text="Talla de Camisetas:", font=("Arial", 11)).pack(pady=(10, 0))
        self.slider_tamano = ctk.CTkSlider(card_herramientas, from_=0.5, to=1.8, command=self.actualizar_tamano_jugadores, button_color=COLOR_ACENTO_AZUL)
        self.slider_tamano.set(1.0)
        self.slider_tamano.pack(pady=(0, 10), padx=20, fill="x")

        # Corrección del empaquetado (Grid 50/50) para evitar que se corten a la derecha
        btn_frame_herr = ctk.CTkFrame(card_herramientas, fg_color="transparent")
        btn_frame_herr.pack(fill="x", pady=(0, 15), padx=10)
        btn_frame_herr.grid_columnconfigure(0, weight=1)
        btn_frame_herr.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(btn_frame_herr, text="🗑️ Limpiar", fg_color="#4F5268", hover_color="#3A3C4D", command=self.mi_cancha.limpiar_trazos).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame_herr, text="📸 Exportar", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=self.guardar_imagen).grid(row=0, column=1, padx=5, sticky="ew")

        # --- 7. AJUSTES (GLOBAL) ---
        card_main = self.crear_tarjeta(scroll_panel, "⚙️ CONFIGURACIÓN GLOBAL")
        frame_top_btns = ctk.CTkFrame(card_main, fg_color="transparent")
        frame_top_btns.pack(fill="x", padx=10, pady=(5, 15))
        
        # Corrección del empaquetado (Grid 50/50) para evitar que se corten a la derecha
        frame_top_btns.grid_columnconfigure(0, weight=1)
        frame_top_btns.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(frame_top_btns, text="⚙️ Equipos", fg_color=COLOR_ACENTO_AZUL, hover_color="#1074D0", font=("Arial", 12, "bold"), command=self.abrir_editor_equipos).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(frame_top_btns, text="🛠️ Ajustes", fg_color="#4F5268", hover_color="#3A3C4D", font=("Arial", 12, "bold"), command=self.abrir_configuracion).grid(row=0, column=1, padx=5, sticky="ew")

        # Cargar inicial
        self.cargar_equipo_local(self.combo_equipo_local.get())
        self.cargar_equipo_visita(self.combo_equipo_visita.get())
        self.registrar_evento("✓ Interfaz reorganizada y botones ajustados.")

    # ================= FUNCIONES ================= 
    def actualizar_tamano_jugadores(self, valor):
        self.mi_cancha.cambiar_escala_jugadores(valor)

    def cambiar_modo_cancha(self):
        self.mi_cancha.cambiar_modo(self.modo_var.get())
        if self.modo_var.get() == "dibujar": self.registrar_evento("🖍️ Herramienta de dibujo activada")
            
    def guardar_imagen(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], title="Guardar Pizarra")
        if ruta:
            self.update_idletasks()
            exito = self.mi_cancha.exportar_imagen(ruta)
            if exito: self.registrar_evento(f"📸 Exportación gráfica completada exitosamente")
            else: self.registrar_evento(f"❌ Error interno al exportar")

    def toggle_cronometro(self):
        if self.cronometro_activo:
            self.cronometro_activo = False
            self.btn_play.configure(text="▶️")
            self.registrar_evento(f"⏱️ Tiempo detenido en {self._formatear_tiempo()}")
        else:
            self.cronometro_activo = True
            self.btn_play.configure(text="⏸️")
            self.registrar_evento("⏱️ Tiempo iniciado")
            self.actualizar_tiempo()

    def actualizar_tiempo(self):
        if self.cronometro_activo:
            self.segundos += 1
            self.lbl_crono.configure(text=self._formatear_tiempo())
            self.after(1000, self.actualizar_tiempo)

    def reset_cronometro(self):
        self.cronometro_activo = False
        self.segundos = 0
        self.lbl_crono.configure(text="00:00")
        self.btn_play.configure(text="▶️")
        self.registrar_evento("⏱️ Tiempo reiniciado a 0")

    def _formatear_tiempo(self):
        m, s = self.segundos // 60, self.segundos % 60
        return f"{m:02d}:{s:02d}"

    def abrir_configuracion(self):
        ventana_cfg = ctk.CTkToplevel(self)
        ventana_cfg.title("Ajustes del Sistema")
        self.centrar_y_poner_logo(ventana_cfg, 350, 320)
        ventana_cfg.transient(self)
        ventana_cfg.grab_set()
        ventana_cfg.configure(fg_color=COLOR_FONDO_APP)

        ctk.CTkLabel(ventana_cfg, text="Configuración Visual", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(ventana_cfg, text="Escala General de la Interfaz:").pack(pady=(10, 5))
        opciones_escala = {"Pequeño (80%)": "0.8", "Normal (100%)": "1.0", "Grande (110%)": "1.1", "Extra Grande (120%)": "1.2"}
        combo_escala = ctk.CTkComboBox(ventana_cfg, values=list(opciones_escala.keys()), state="readonly", border_color=COLOR_PANEL)
        combo_escala.set("Normal (100%)")
        combo_escala.pack(pady=5, padx=40, fill="x")

        ctk.CTkLabel(ventana_cfg, text="Tamaño de Letras en Cancha:").pack(pady=(15, 5))
        slider_texto = ctk.CTkSlider(ventana_cfg, from_=0.5, to=2.0, button_color=COLOR_ACENTO_AZUL)
        slider_texto.set(self.mi_cancha.escala_textos)
        slider_texto.pack(pady=5, padx=40, fill="x")

        def aplicar_ajustes():
            seleccion = combo_escala.get()
            ctk.set_widget_scaling(float(opciones_escala[seleccion]))
            self.mi_cancha.cambiar_escala_textos(slider_texto.get())
            self.registrar_evento(f"⚙️ Configuración visual actualizada.")
            ventana_cfg.destroy()

        ctk.CTkButton(ventana_cfg, text="Aplicar Cambios", fg_color=COLOR_ACENTO_AZUL, hover_color="#1074D0", command=aplicar_ajustes).pack(pady=25)

    def abrir_menu_sustitucion(self, tipo_equipo, indice_titular):
        equipo_data = self.data_local if tipo_equipo == "local" else self.data_visita
        if indice_titular >= len(equipo_data["jugadores"]): return
        
        titular = equipo_data["jugadores"][indice_titular]
        suplentes = [s for s in equipo_data.get("suplentes", []) if s.get("nombre")]
        if not suplentes: return 
            
        ventana_sub = ctk.CTkToplevel(self)
        ventana_sub.title("Sustitución de Jugador")
        self.centrar_y_poner_logo(ventana_sub, 300, 420)
        ventana_sub.transient(self)
        ventana_sub.grab_set()
        ventana_sub.configure(fg_color=COLOR_FONDO_APP)
        
        ctk.CTkLabel(ventana_sub, text="SALE DEL CAMPO:", font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC).pack(pady=(15,0))
        ctk.CTkLabel(ventana_sub, text=f"{titular.get('numero')} - {titular.get('nombre')}", font=("Arial", 18, "bold"), text_color=COLOR_ACENTO_ROJO).pack(pady=(0,15))
        ctk.CTkFrame(ventana_sub, height=2, fg_color=COLOR_PANEL).pack(fill="x", padx=20)
        ctk.CTkLabel(ventana_sub, text="INGRESAR A:", font=("Arial", 11, "bold"), text_color=COLOR_TEXTO_SEC).pack(pady=(15,5))
        
        scroll_subs = ctk.CTkScrollableFrame(ventana_sub, fg_color="transparent")
        scroll_subs.pack(fill="both", expand=True, padx=15, pady=5)
        
        for i, sup in enumerate(suplentes):
            texto_boton = f"{sup.get('numero')} - {sup.get('nombre')}"
            cmd = lambda idx_sup=i: self.ejecutar_sustitucion(tipo_equipo, indice_titular, idx_sup, ventana_sub)
            ctk.CTkButton(scroll_subs, text=texto_boton, fg_color=COLOR_PANEL, hover_color="#3A3C4D", border_width=1, border_color=COLOR_ACENTO_AZUL, font=("Arial", 14), command=cmd).pack(pady=5, fill="x")

    def ejecutar_sustitucion(self, tipo_equipo, idx_titular, idx_suplente, ventana):
        equipo_data = self.data_local if tipo_equipo == "local" else self.data_visita
        nombre_equipo = self.combo_equipo_local.get() if tipo_equipo == "local" else self.combo_equipo_visita.get()
        titular_sale = equipo_data["jugadores"][idx_titular]
        suplente_entra = equipo_data["suplentes"][idx_suplente]
        
        equipo_data["jugadores"][idx_titular] = suplente_entra
        equipo_data["suplentes"][idx_suplente] = titular_sale
        
        self.registrar_evento(f"🔄 CAMBIO ({nombre_equipo}): Sale {titular_sale['nombre']} | Entra {suplente_entra['nombre']}")
        ventana.destroy()
        self.actualizar_todo() 

    def cargar_equipo_local(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.data_local = {"jugadores": list(datos.get("jugadores", [])), "suplentes": list(datos.get("suplentes", [])), "tecnico": datos.get("tecnico", "Por definir")}
        uniformes_disponibles = list(datos.get("uniformes", {"Base": {"bg": "#FFF", "fg": "#000"}}).keys())
        self.combo_color_local.configure(values=uniformes_disponibles)
        self.combo_color_local.set(uniformes_disponibles[0])
        self.entry_estadio.delete(0, 'end')
        self.entry_estadio.insert(0, datos.get("estadio", "ESTADIO DESCONOCIDO"))
        self.actualizar_todo()

    def cargar_equipo_visita(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.data_visita = {"jugadores": list(datos.get("jugadores", [])), "suplentes": list(datos.get("suplentes", [])), "tecnico": datos.get("tecnico", "Por definir")}
        uniformes_disponibles = list(datos.get("uniformes", {"Base": {"bg": "#111", "fg": "#FFF"}}).keys())
        self.combo_color_visita.configure(values=uniformes_disponibles)
        if len(uniformes_disponibles) > 1: self.combo_color_visita.set(uniformes_disponibles[1])
        else: self.combo_color_visita.set(uniformes_disponibles[0])
        self.actualizar_todo()

    def abrir_editor_equipos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Editor de Base de Datos")
        self.centrar_y_poner_logo(ventana, 500, 800) 
        ventana.transient(self)
        ventana.grab_set()
        ventana.configure(fg_color=COLOR_FONDO_APP)
        
        frame_top = ctk.CTkFrame(ventana, fg_color="transparent")
        frame_top.pack(fill="x", padx=20, pady=5)
        combo_editar = ctk.CTkComboBox(frame_top, values=list(self.db.equipos.keys()), border_color=COLOR_PANEL)
        combo_editar.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL, corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        entry_nombre = ctk.CTkEntry(scroll, placeholder_text="Nombre del Equipo"); entry_nombre.pack(fill="x", pady=2)
        entry_estadio_ed = ctk.CTkEntry(scroll, placeholder_text="Estadio Local"); entry_estadio_ed.pack(fill="x", pady=2)
        entry_dt = ctk.CTkEntry(scroll, placeholder_text="Director Técnico"); entry_dt.pack(fill="x", pady=2)
        combo_color = ctk.CTkComboBox(scroll, values=list(COLORES_EQUIPOS.keys()), state="readonly")
        combo_color.set("Blanco Base")
        combo_color.pack(fill="x", pady=5)
        
        ctk.CTkLabel(scroll, text="11 Titulares:", font=("Arial", 12, "bold")).pack(pady=(10,0))
        entradas_jugadores = []
        for i in range(11):
            row = ctk.CTkFrame(scroll, fg_color="transparent"); row.pack(fill="x", pady=1)
            nu = ctk.CTkEntry(row, width=40, placeholder_text="#"); nu.pack(side="left", padx=(0, 5))
            no = ctk.CTkEntry(row, placeholder_text=f"Titular {i+1}"); no.pack(side="left", fill="x", expand=True)
            entradas_jugadores.append((nu, no))
            
        ctk.CTkLabel(scroll, text="7 Suplentes:", font=("Arial", 12, "bold")).pack(pady=(10,0))
        entradas_suplentes = []
        for i in range(7):
            row = ctk.CTkFrame(scroll, fg_color="transparent"); row.pack(fill="x", pady=1)
            nu = ctk.CTkEntry(row, width=40, placeholder_text="#"); nu.pack(side="left", padx=(0, 5))
            no = ctk.CTkEntry(row, placeholder_text=f"Suplente {i+1}"); no.pack(side="left", fill="x", expand=True)
            entradas_suplentes.append((nu, no))
            
        def cargar_datos_al_formulario(sel):
            if sel in self.db.equipos:
                d = self.db.equipos[sel]
                entry_nombre.delete(0, 'end'); entry_nombre.insert(0, sel)
                entry_estadio_ed.delete(0, 'end'); entry_estadio_ed.insert(0, d.get("estadio", ""))
                entry_dt.delete(0, 'end'); entry_dt.insert(0, d.get("tecnico", ""))
                for i, j_data in enumerate(d.get("jugadores", [])):
                    if i < 11: entradas_jugadores[i][0].delete(0, 'end'); entradas_jugadores[i][0].insert(0, str(j_data.get("numero", ""))); entradas_jugadores[i][1].delete(0, 'end'); entradas_jugadores[i][1].insert(0, str(j_data.get("nombre", "")))
                for nu, no in entradas_suplentes: nu.delete(0, 'end'); no.delete(0, 'end')
                for i, j_data in enumerate(d.get("suplentes", [])):
                    if i < 7: entradas_suplentes[i][0].insert(0, str(j_data.get("numero", ""))); entradas_suplentes[i][1].insert(0, str(j_data.get("nombre", "")))
                    
        def limpiar_formulario():
            entry_nombre.delete(0, 'end'); entry_estadio_ed.delete(0, 'end'); entry_dt.delete(0, 'end')
            for nu, no in entradas_jugadores + entradas_suplentes: nu.delete(0, 'end'); no.delete(0, 'end')
            entry_nombre.focus()
            
        ctk.CTkButton(frame_top, text="✨ Nuevo", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=limpiar_formulario).pack(side="right", padx=10)
        combo_editar.configure(command=cargar_datos_al_formulario); cargar_datos_al_formulario(combo_editar.get())
        
        def guardar_equipo():
            nom = entry_nombre.get().upper().strip()
            if not nom: return
            j_nuevos = [{"numero": nu.get().strip() or "-", "nombre": no.get().strip() or "Jugador"} for nu, no in entradas_jugadores]
            s_nuevos = [{"numero": nu.get().strip(), "nombre": no.get().strip()} for nu, no in entradas_suplentes if no.get().strip()]
            color_base = COLORES_EQUIPOS.get(combo_color.get(), {"bg": "#FFFFFF", "fg": "#000000"})
            color_invertido = {"bg": color_base["fg"], "fg": color_base["bg"]}
            if nom in self.db.equipos: dict_uniformes = self.db.equipos[nom].get("uniformes", {"Local": color_base, "Visita": color_invertido})
            else: dict_uniformes = {"Local": color_base, "Visita": color_invertido}
            self.db.equipos[nom] = {"estadio": entry_estadio_ed.get().upper().strip(), "tecnico": entry_dt.get().strip(), "uniformes": dict_uniformes, "jugadores": j_nuevos, "suplentes": s_nuevos}
            self.db.guardar_datos(self.db.equipos)
            ln = list(self.db.equipos.keys())
            self.combo_equipo_local.configure(values=ln); self.combo_equipo_visita.configure(values=ln)
            self.combo_equipo_local.set(nom); self.cargar_equipo_local(nom)
            self.registrar_evento(f"DB Actualizada con éxito: {nom}")
            ventana.destroy()
            
        ctk.CTkButton(ventana, text="💾 Guardar en DB", fg_color=COLOR_ACENTO_AZUL, hover_color="#1074D0", command=guardar_equipo).pack(pady=15, padx=20, fill="x")

    def intercambiar_lados(self):
        eq_t, col_t, form_t, dt_t = self.combo_equipo_local.get(), self.combo_color_local.get(), self.combo_formacion_local.get(), self.data_local
        self.combo_equipo_local.set(self.combo_equipo_visita.get())
        self.cargar_equipo_local(self.combo_equipo_visita.get())
        self.combo_color_local.set(self.combo_color_visita.get())
        self.combo_formacion_local.set(self.combo_formacion_visita.get())
        self.data_local = self.data_visita
        
        self.combo_equipo_visita.set(eq_t)
        self.cargar_equipo_visita(eq_t)
        self.combo_color_visita.set(col_t)
        self.combo_formacion_visita.set(form_t)
        self.data_visita = dt_t
        self.registrar_evento("⇅ Lados de la cancha intercambiados")
        self.actualizar_todo()

    def cambiar_tema_cancha(self, seleccion):
        self.mi_cancha.cambiar_estilo_cancha(ESTILOS_CANCHA[seleccion]["fondo"], ESTILOS_CANCHA[seleccion]["lineas"])

    def actualizar_todo(self, *args):
        self.mi_cancha.actualizar_entorno(self.combo_competicion.get(), self.entry_estadio.get().upper(), self.combo_equipo_local.get(), self.combo_equipo_visita.get())
        nombre_l = self.combo_equipo_local.get()
        uniforme_l = self.combo_color_local.get()
        dict_color_l = self.db.equipos.get(nombre_l, {}).get("uniformes", {}).get(uniforme_l, {"bg": "#FFF", "fg": "#000"})
        if self.combo_formacion_local.get() != "Seleccionar": self.mi_cancha.actualizar_datos("local", self.combo_formacion_local.get(), self.data_local, dict_color_l)
        nombre_v = self.combo_equipo_visita.get()
        uniforme_v = self.combo_color_visita.get()
        dict_color_v = self.db.equipos.get(nombre_v, {}).get("uniformes", {}).get(uniforme_v, {"bg": "#111", "fg": "#FFF"})
        if self.combo_formacion_visita.get() != "Seleccionar": self.mi_cancha.actualizar_datos("visita", self.combo_formacion_visita.get(), self.data_visita, dict_color_v)

if __name__ == "__main__":
    app = AppNarrador()
    app.mainloop()