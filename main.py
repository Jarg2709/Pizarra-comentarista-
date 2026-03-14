import os
import ctypes 
from datetime import datetime
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
        self.centrar_y_poner_logo(self, 1100, 750)
        
        self.db = GestorEquipos()

        # --- Variables del Cronómetro ---
        self.segundos = 0
        self.cronometro_activo = False

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.mi_cancha = CanchaWidget(master=self)
        self.mi_cancha.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.mi_cancha.on_click_jugador = self.abrir_menu_sustitucion

        self.panel = ctk.CTkFrame(master=self, width=300)
        self.panel.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)
        
        self.data_local = {"jugadores": [], "suplentes": [], "tecnico": ""}
        self.data_visita = {"jugadores": [], "suplentes": [], "tecnico": ""}

        self.construir_panel()

    def centrar_y_poner_logo(self, ventana, ancho, alto):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho / 2) - (ancho / 2))
        y = int((pantalla_alto / 2) - (alto / 2))
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_icono = os.path.join(directorio_actual, "assets", "icono.ico")
        try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('narrador.pro.v18')
        except: pass
        if os.path.exists(ruta_icono):
            ventana.after(10, lambda: ventana.iconbitmap(ruta_icono))

    def registrar_evento(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        texto = f"[{hora}] {mensaje}\n"
        self.caja_eventos.configure(state="normal")
        self.caja_eventos.insert("end", texto)
        self.caja_eventos.see("end")
        self.caja_eventos.configure(state="disabled")

    def construir_panel(self):
        self.scroll_panel = ctk.CTkScrollableFrame(self.panel, width=280)
        self.scroll_panel.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.scroll_panel, text="Control Táctico FPC", font=("Arial", 20, "bold")).pack(pady=(10, 5))
        
        # --- NUEVO: SECCIÓN DE CRONÓMETRO ---
        frame_crono = ctk.CTkFrame(self.scroll_panel, fg_color="#1A1A1A", corner_radius=10)
        frame_crono.pack(fill="x", pady=(0, 15), padx=10)
        
        self.lbl_crono = ctk.CTkLabel(frame_crono, text="00:00", font=("Consolas", 32, "bold"), text_color="#FFD54F")
        self.lbl_crono.pack(pady=(5, 0))
        
        frame_btn_crono = ctk.CTkFrame(frame_crono, fg_color="transparent")
        frame_btn_crono.pack(pady=(0, 10))
        
        self.btn_play = ctk.CTkButton(frame_btn_crono, text="▶️", width=40, fg_color="#2E7D32", hover_color="#1B5E20", command=self.toggle_cronometro)
        self.btn_play.pack(side="left", padx=5)
        
        ctk.CTkButton(frame_btn_crono, text="🔄", width=40, fg_color="#D32F2F", hover_color="#B71C1C", command=self.reset_cronometro).pack(side="left", padx=5)
        
        # --- BOTONES DE CONFIGURACIÓN ---
        frame_top_btns = ctk.CTkFrame(self.scroll_panel, fg_color="transparent")
        frame_top_btns.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(frame_top_btns, text="⚙️ Equipos", width=120, fg_color="#1976D2", hover_color="#1565C0", font=("Arial", 12, "bold"), command=self.abrir_editor_equipos).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(frame_top_btns, text="🛠️ Ajustes", width=100, fg_color="#757575", hover_color="#616161", font=("Arial", 12, "bold"), command=self.abrir_configuracion).pack(side="right", expand=True, padx=2)

        # --- ENTORNO ---
        ctk.CTkLabel(self.scroll_panel, text="🏆 Competición:").pack(pady=(15,0))
        self.combo_competicion = ctk.CTkComboBox(self.scroll_panel, values=["LIGA BETPLAY DIMAYOR", "COPA BETPLAY DIMAYOR", "TORNEO BETPLAY DIMAYOR"], command=self.actualizar_todo, state="readonly")
        self.combo_competicion.set("LIGA BETPLAY DIMAYOR")
        self.combo_competicion.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.scroll_panel, text="🏟️ Estadio:").pack(pady=(5,0))
        self.entry_estadio = ctk.CTkEntry(self.scroll_panel)
        self.entry_estadio.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.scroll_panel, text="Estilo de Pizarra:").pack(pady=(5,0))
        self.combo_estilo = ctk.CTkComboBox(self.scroll_panel, values=list(ESTILOS_CANCHA.keys()), command=self.cambiar_tema_cancha, state="readonly")
        self.combo_estilo.set("Pasto Clásico (Verde)")
        self.combo_estilo.pack(pady=5, padx=15, fill="x")
        
        ctk.CTkFrame(self.scroll_panel, height=2, fg_color="gray").pack(fill="x", pady=10, padx=15)

        # --- EQUIPO LOCAL ---
        ctk.CTkLabel(self.scroll_panel, text="⬅️ EQUIPO LOCAL ⬅️", font=("Arial", 12, "bold")).pack()
        lista_equipos = list(self.db.equipos.keys())
        
        self.combo_equipo_local = ctk.CTkComboBox(self.scroll_panel, values=lista_equipos, command=self.cargar_equipo_local, state="readonly")
        self.combo_equipo_local.set("LLANEROS FC" if "LLANEROS FC" in lista_equipos else lista_equipos[0])
        self.combo_equipo_local.pack(pady=5, padx=15, fill="x")
        
        self.combo_color_local = ctk.CTkComboBox(self.scroll_panel, values=list(COLORES_EQUIPOS.keys()), command=self.actualizar_todo, state="readonly")
        self.combo_color_local.set("Blanco y Dorado (Llaneros)")
        self.combo_color_local.pack(pady=5, padx=15, fill="x")

        self.combo_formacion_local = ctk.CTkComboBox(self.scroll_panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], command=self.actualizar_todo, state="readonly")
        self.combo_formacion_local.set("4-2-3-1")
        self.combo_formacion_local.pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(self.scroll_panel, text="⚽ Cambiar Lados", fg_color="#FBC02D", hover_color="#F9A825", text_color="black", font=("Arial", 12, "bold"), command=self.intercambiar_lados).pack(pady=15, padx=15, fill="x")

        # --- EQUIPO VISITA ---
        ctk.CTkLabel(self.scroll_panel, text="➡️ EQUIPO VISITA ➡️", font=("Arial", 12, "bold")).pack()
        self.combo_equipo_visita = ctk.CTkComboBox(self.scroll_panel, values=lista_equipos, command=self.cargar_equipo_visita, state="readonly")
        self.combo_equipo_visita.set("MILLONARIOS FC" if "MILLONARIOS FC" in lista_equipos else lista_equipos[-1])
        self.combo_equipo_visita.pack(pady=5, padx=15, fill="x")
        
        self.combo_color_visita = ctk.CTkComboBox(self.scroll_panel, values=list(COLORES_EQUIPOS.keys()), command=self.actualizar_todo, state="readonly")
        self.combo_color_visita.set("Azul (Millonarios)")
        self.combo_color_visita.pack(pady=5, padx=15, fill="x")

        self.combo_formacion_visita = ctk.CTkComboBox(self.scroll_panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], command=self.actualizar_todo, state="readonly")
        self.combo_formacion_visita.set("4-3-3")
        self.combo_formacion_visita.pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(self.scroll_panel, text="Refrescar Pizarra", command=self.actualizar_todo).pack(pady=(15, 5), padx=15, fill="x")
        
        # --- EVENTOS ---
        ctk.CTkFrame(self.scroll_panel, height=2, fg_color="gray").pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(self.scroll_panel, text="📝 REGISTRO DE EVENTOS", font=("Arial", 12, "bold")).pack()
        
        self.caja_eventos = ctk.CTkTextbox(self.scroll_panel, height=120, font=("Consolas", 11), fg_color="#1A1A1A")
        self.caja_eventos.pack(pady=5, padx=15, fill="x")
        self.caja_eventos.configure(state="disabled")

        self.cargar_equipo_local(self.combo_equipo_local.get())
        self.cargar_equipo_visita(self.combo_equipo_visita.get())
        self.registrar_evento("¡Análisis táctico iniciado!")

    # =======================================================
    # LÓGICA DEL CRONÓMETRO
    # =======================================================
    def toggle_cronometro(self):
        if self.cronometro_activo:
            self.cronometro_activo = False
            self.btn_play.configure(text="▶️")
            self.registrar_evento(f"⏱️ Reloj pausado en {self._formatear_tiempo()}")
        else:
            self.cronometro_activo = True
            self.btn_play.configure(text="⏸️")
            self.registrar_evento("⏱️ Reloj iniciado")
            self.actualizar_tiempo()

    def actualizar_tiempo(self):
        if self.cronometro_activo:
            self.segundos += 1
            self.lbl_crono.configure(text=self._formatear_tiempo())
            self.after(1000, self.actualizar_tiempo) # Llama a esta función cada 1000ms (1 seg)

    def reset_cronometro(self):
        self.cronometro_activo = False
        self.segundos = 0
        self.lbl_crono.configure(text="00:00")
        self.btn_play.configure(text="▶️")
        self.registrar_evento("⏱️ Reloj reiniciado")

    def _formatear_tiempo(self):
        m = self.segundos // 60
        s = self.segundos % 60
        return f"{m:02d}:{s:02d}"

    # =======================================================
    # NUEVO: MODAL DE CONFIGURACIÓN / AJUSTES
    # =======================================================
    def abrir_configuracion(self):
        ventana_cfg = ctk.CTkToplevel(self)
        ventana_cfg.title("🛠️ Ajustes de Interfaz")
        self.centrar_y_poner_logo(ventana_cfg, 350, 250)
        ventana_cfg.transient(self)
        ventana_cfg.grab_set()

        ctk.CTkLabel(ventana_cfg, text="Configuración Visual", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(ventana_cfg, text="Escala (Tamaño de letras y botones):").pack(pady=(10, 5))
        
        # Opciones de escalado de CustomTkinter
        opciones_escala = {
            "Pequeño (80%)": "0.8",
            "Normal (100%)": "1.0",
            "Grande (110%)": "1.1",
            "Extra Grande (120%)": "1.2"
        }
        
        combo_escala = ctk.CTkComboBox(ventana_cfg, values=list(opciones_escala.keys()), state="readonly")
        combo_escala.set("Normal (100%)") # Valor por defecto visual
        combo_escala.pack(pady=5, padx=40, fill="x")

        def aplicar_ajustes():
            seleccion = combo_escala.get()
            escala_float = float(opciones_escala[seleccion])
            
            # Cambia dinámicamente el tamaño de TODO el programa
            ctk.set_widget_scaling(escala_float)
            
            self.registrar_evento(f"⚙️ Escala cambiada a {seleccion}")
            ventana_cfg.destroy()

        ctk.CTkButton(ventana_cfg, text="Aplicar Cambios", fg_color="#43A047", hover_color="#2E7D32", command=aplicar_ajustes).pack(pady=20)

    # =======================================================
    # SUSTITUCIONES INTERACTIVAS
    # =======================================================
    def abrir_menu_sustitucion(self, tipo_equipo, indice_titular):
        equipo_data = self.data_local if tipo_equipo == "local" else self.data_visita
        if indice_titular >= len(equipo_data["jugadores"]): return
        
        titular = equipo_data["jugadores"][indice_titular]
        suplentes = [s for s in equipo_data.get("suplentes", []) if s.get("nombre")]
        if not suplentes: return 
            
        ventana_sub = ctk.CTkToplevel(self)
        ventana_sub.title("🔄 Cambio de Jugador")
        self.centrar_y_poner_logo(ventana_sub, 300, 400)
        ventana_sub.transient(self)
        ventana_sub.grab_set()
        
        ctk.CTkLabel(ventana_sub, text="⬇️ SALE:", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(15,0))
        ctk.CTkLabel(ventana_sub, text=f"{titular.get('numero')} - {titular.get('nombre')}", font=("Arial", 18, "bold"), text_color="#E53935").pack(pady=(0,15))
        
        ctk.CTkFrame(ventana_sub, height=2, fg_color="#333333").pack(fill="x", padx=20)
        
        ctk.CTkLabel(ventana_sub, text="⬆️ SELECCIONA QUIÉN ENTRA:", font=("Arial", 12, "bold"), text_color="#43A047").pack(pady=(15,5))
        
        scroll_subs = ctk.CTkScrollableFrame(ventana_sub, fg_color="transparent")
        scroll_subs.pack(fill="both", expand=True, padx=15, pady=5)
        
        for i, sup in enumerate(suplentes):
            texto_boton = f"{sup.get('numero')} - {sup.get('nombre')}"
            cmd = lambda idx_sup=i: self.ejecutar_sustitucion(tipo_equipo, indice_titular, idx_sup, ventana_sub)
            ctk.CTkButton(scroll_subs, text=texto_boton, fg_color="#2E7D32", hover_color="#1B5E20", font=("Arial", 14), command=cmd).pack(pady=5, fill="x")

    def ejecutar_sustitucion(self, tipo_equipo, idx_titular, idx_suplente, ventana):
        equipo_data = self.data_local if tipo_equipo == "local" else self.data_visita
        nombre_equipo = self.combo_equipo_local.get() if tipo_equipo == "local" else self.combo_equipo_visita.get()
        
        titular_sale = equipo_data["jugadores"][idx_titular]
        suplente_entra = equipo_data["suplentes"][idx_suplente]
        
        equipo_data["jugadores"][idx_titular] = suplente_entra
        equipo_data["suplentes"][idx_suplente] = titular_sale
        
        minuto_juego = self._formatear_tiempo()
        self.registrar_evento(f"[{minuto_juego}] 🔄 CAMBIO {nombre_equipo}:\n  🔴 Sale: {titular_sale['nombre']}\n  🟢 Entra: {suplente_entra['nombre']}")
        
        ventana.destroy()
        self.actualizar_todo() 

    # =======================================================
    # CARGA Y ACTUALIZACIÓN
    # =======================================================
    def cargar_equipo_local(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.data_local = {
            "jugadores": list(datos.get("jugadores", [])),
            "suplentes": list(datos.get("suplentes", [])),
            "tecnico": datos.get("tecnico", "Por definir")
        }
        self.combo_color_local.set(datos.get("color", "Blanco y Dorado (Llaneros)"))
        self.entry_estadio.delete(0, 'end')
        self.entry_estadio.insert(0, datos.get("estadio", "ESTADIO DESCONOCIDO"))
        self.actualizar_todo()

    def cargar_equipo_visita(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.data_visita = {
            "jugadores": list(datos.get("jugadores", [])),
            "suplentes": list(datos.get("suplentes", [])),
            "tecnico": datos.get("tecnico", "Por definir")
        }
        self.combo_color_visita.set(datos.get("color", "Azul (Millonarios)"))
        self.actualizar_todo()

    def abrir_editor_equipos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Base de Datos FPC")
        self.centrar_y_poner_logo(ventana, 500, 800) 
        ventana.transient(self)
        ventana.grab_set()
        
        frame_top = ctk.CTkFrame(ventana)
        frame_top.pack(fill="x", padx=20, pady=5)
        combo_editar = ctk.CTkComboBox(frame_top, values=list(self.db.equipos.keys()))
        combo_editar.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        scroll = ctk.CTkScrollableFrame(ventana)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        entry_nombre = ctk.CTkEntry(scroll, placeholder_text="Nombre del Equipo")
        entry_nombre.pack(fill="x", pady=2)
        entry_estadio_ed = ctk.CTkEntry(scroll, placeholder_text="Estadio Local")
        entry_estadio_ed.pack(fill="x", pady=2)
        entry_dt = ctk.CTkEntry(scroll, placeholder_text="Director Técnico")
        entry_dt.pack(fill="x", pady=2)
        combo_color = ctk.CTkComboBox(scroll, values=list(COLORES_EQUIPOS.keys()), state="readonly")
        combo_color.pack(fill="x", pady=5)
        
        ctk.CTkLabel(scroll, text="11 Titulares:", font=("Arial", 12, "bold")).pack(pady=(10,0))
        entradas_jugadores = []
        for i in range(11):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            num_e = ctk.CTkEntry(row, width=40, placeholder_text="#")
            num_e.pack(side="left", padx=(0, 5))
            nom_e = ctk.CTkEntry(row, placeholder_text=f"Titular {i+1}")
            nom_e.pack(side="left", fill="x", expand=True)
            entradas_jugadores.append((num_e, nom_e))
            
        ctk.CTkLabel(scroll, text="7 Suplentes:", font=("Arial", 12, "bold")).pack(pady=(10,0))
        entradas_suplentes = []
        for i in range(7):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            num_e = ctk.CTkEntry(row, width=40, placeholder_text="#")
            num_e.pack(side="left", padx=(0, 5))
            nom_e = ctk.CTkEntry(row, placeholder_text=f"Suplente {i+1}")
            nom_e.pack(side="left", fill="x", expand=True)
            entradas_suplentes.append((num_e, nom_e))
            
        def cargar_datos_al_formulario(seleccion):
            if seleccion in self.db.equipos:
                d = self.db.equipos[seleccion]
                entry_nombre.delete(0, 'end'); entry_nombre.insert(0, seleccion)
                entry_estadio_ed.delete(0, 'end'); entry_estadio_ed.insert(0, d.get("estadio", ""))
                entry_dt.delete(0, 'end'); entry_dt.insert(0, d.get("tecnico", ""))
                combo_color.set(d.get("color", "Blanco y Dorado (Llaneros)"))
                
                for i, j_data in enumerate(d.get("jugadores", [])):
                    if i < len(entradas_jugadores):
                        entradas_jugadores[i][0].delete(0, 'end'); entradas_jugadores[i][0].insert(0, str(j_data.get("numero", "")))
                        entradas_jugadores[i][1].delete(0, 'end'); entradas_jugadores[i][1].insert(0, str(j_data.get("nombre", "")))
                        
                for num_e, nom_e in entradas_suplentes: num_e.delete(0, 'end'); nom_e.delete(0, 'end')
                for i, j_data in enumerate(d.get("suplentes", [])):
                    if i < len(entradas_suplentes):
                        entradas_suplentes[i][0].insert(0, str(j_data.get("numero", "")))
                        entradas_suplentes[i][1].insert(0, str(j_data.get("nombre", "")))
                    
        def limpiar_formulario():
            entry_nombre.delete(0, 'end'); entry_estadio_ed.delete(0, 'end'); entry_dt.delete(0, 'end')
            combo_color.set("Blanco y Dorado (Llaneros)")
            for num_e, nom_e in entradas_jugadores + entradas_suplentes:
                num_e.delete(0, 'end'); nom_e.delete(0, 'end')
            entry_nombre.focus()
            
        ctk.CTkButton(frame_top, text="✨ Nuevo", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=limpiar_formulario).pack(side="right", padx=10)
        combo_editar.configure(command=cargar_datos_al_formulario)
        cargar_datos_al_formulario(combo_editar.get())
        
        def guardar_equipo():
            nom = entry_nombre.get().upper().strip()
            if not nom: return
            j_nuevos = [{"numero": num_e.get().strip() or "-", "nombre": nom_e.get().strip() or "Jugador"} for num_e, nom_e in entradas_jugadores]
            s_nuevos = [{"numero": num_e.get().strip(), "nombre": nom_e.get().strip()} for num_e, nom_e in entradas_suplentes if nom_e.get().strip()]
            self.db.equipos[nom] = {
                "color": combo_color.get(), "estadio": entry_estadio_ed.get().upper().strip(),
                "tecnico": entry_dt.get().strip(), "jugadores": j_nuevos, "suplentes": s_nuevos
            }
            self.db.guardar_datos(self.db.equipos)
            lista_nueva = list(self.db.equipos.keys())
            self.combo_equipo_local.configure(values=lista_nueva); self.combo_equipo_visita.configure(values=lista_nueva)
            self.combo_equipo_local.set(nom); self.cargar_equipo_local(nom)
            self.registrar_evento(f"DB Actualizada: {nom}")
            ventana.destroy()
            
        ctk.CTkButton(ventana, text="💾 Guardar y Actualizar", fg_color="#43A047", hover_color="#2E7D32", command=guardar_equipo).pack(pady=15, padx=20, fill="x")

    def intercambiar_lados(self):
        eq_t, col_t, form_t, dt_t = self.combo_equipo_local.get(), self.combo_color_local.get(), self.combo_formacion_local.get(), self.data_local
        
        self.combo_equipo_local.set(self.combo_equipo_visita.get()); self.combo_color_local.set(self.combo_color_visita.get())
        self.combo_formacion_local.set(self.combo_formacion_visita.get()); self.data_local = self.data_visita
        
        self.combo_equipo_visita.set(eq_t); self.combo_color_visita.set(col_t)
        self.combo_formacion_visita.set(form_t); self.data_visita = dt_t
        
        self.registrar_evento("⇅ Intercambio de campos")
        self.actualizar_todo()

    def cambiar_tema_cancha(self, seleccion):
        self.mi_cancha.cambiar_estilo_cancha(ESTILOS_CANCHA[seleccion]["fondo"], ESTILOS_CANCHA[seleccion]["lineas"])

    def actualizar_todo(self, *args):
        self.mi_cancha.actualizar_entorno(self.combo_competicion.get(), self.entry_estadio.get().upper(), self.combo_equipo_local.get(), self.combo_equipo_visita.get())
        
        if self.combo_formacion_local.get() != "Seleccionar":
            self.mi_cancha.actualizar_datos("local", self.combo_formacion_local.get(), self.data_local, self.combo_color_local.get())
            
        if self.combo_formacion_visita.get() != "Seleccionar":
            self.mi_cancha.actualizar_datos("visita", self.combo_formacion_visita.get(), self.data_visita, self.combo_color_visita.get())

if __name__ == "__main__":
    app = AppNarrador()
    app.mainloop()