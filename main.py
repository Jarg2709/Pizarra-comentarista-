import os
import ctypes 
import customtkinter as ctk
from src.componentes.cancha_widget import CanchaWidget
from src.utils.constantes import *
from src.logica.gestor_equipos import GestorEquipos

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppNarrador(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Narrador Pro - Pizarra Táctica")
        self.geometry("1100x750") 
        
        self.db = GestorEquipos()
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_icono = os.path.join(directorio_actual, "assets", "icono.ico")
        try:
            myappid = 'narrador.pro.pizarra.v10'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception: pass
        if os.path.exists(ruta_icono): self.iconbitmap(ruta_icono)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.mi_cancha = CanchaWidget(master=self)
        self.mi_cancha.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.panel = ctk.CTkFrame(master=self, width=300)
        self.panel.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)
        
        self.jugadores_local = []
        self.jugadores_visitante = []

        self.construir_panel()

    def construir_panel(self):
        self.scroll_panel = ctk.CTkScrollableFrame(self.panel, width=280)
        self.scroll_panel.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.scroll_panel, text="Control Total", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkButton(self.scroll_panel, text="⚙️ Gestor de Equipos", fg_color="#1976D2", hover_color="#1565C0", 
                      font=("Arial", 12, "bold"), command=self.abrir_editor_equipos).pack(pady=5, padx=15, fill="x")

        # --- ESTADIO ---
        ctk.CTkLabel(self.scroll_panel, text="🏟️ Nombre del Estadio:").pack(pady=(15,0))
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
        self.combo_equipo_visita.set("REAL MADRID" if "REAL MADRID" in lista_equipos else lista_equipos[-1])
        self.combo_equipo_visita.pack(pady=5, padx=15, fill="x")
        
        self.combo_color_visita = ctk.CTkComboBox(self.scroll_panel, values=list(COLORES_EQUIPOS.keys()), command=self.actualizar_todo, state="readonly")
        self.combo_color_visita.set("Blanco (Madrid)")
        self.combo_color_visita.pack(pady=5, padx=15, fill="x")

        self.combo_formacion_visita = ctk.CTkComboBox(self.scroll_panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], command=self.actualizar_todo, state="readonly")
        self.combo_formacion_visita.set("4-3-3")
        self.combo_formacion_visita.pack(pady=5, padx=15, fill="x")

        ctk.CTkFrame(self.scroll_panel, height=2, fg_color="gray").pack(fill="x", pady=15, padx=15)
        ctk.CTkButton(self.scroll_panel, text="Refrescar Pizarra", command=self.actualizar_todo).pack(pady=5, padx=15, fill="x")
        
        self.cargar_equipo_local(self.combo_equipo_local.get())
        self.cargar_equipo_visita(self.combo_equipo_visita.get())

    def cargar_equipo_local(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.jugadores_local = datos.get("jugadores", [])
        self.combo_color_local.set(datos.get("color", "Blanco y Dorado (Llaneros)"))
        
        self.entry_estadio.delete(0, 'end')
        self.entry_estadio.insert(0, datos.get("estadio", "ESTADIO DESCONOCIDO"))
        self.actualizar_todo()

    def cargar_equipo_visita(self, nombre_equipo):
        datos = self.db.equipos.get(nombre_equipo, {})
        self.jugadores_visitante = datos.get("jugadores", [])
        self.combo_color_visita.set(datos.get("color", "Blanco (Madrid)"))
        self.actualizar_todo()

    # --- NUEVO EDITOR VISUAL CON DORSALES Y POSICIONES ---
    def abrir_editor_equipos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Gestor de Base de Datos")
        ventana.geometry("480x750")
        ventana.transient(self)
        ventana.grab_set()
        
        ctk.CTkLabel(ventana, text="Base de Datos de Equipos", font=("Arial", 18, "bold")).pack(pady=10)
        
        frame_top = ctk.CTkFrame(ventana)
        frame_top.pack(fill="x", padx=20, pady=5)
        
        combo_editar = ctk.CTkComboBox(frame_top, values=list(self.db.equipos.keys()))
        combo_editar.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        scroll = ctk.CTkScrollableFrame(ventana)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        entry_nombre = ctk.CTkEntry(scroll, placeholder_text="Nombre del Equipo (NUEVO o EDITADO)")
        entry_nombre.pack(fill="x", pady=(0, 10))
        
        entry_estadio_editor = ctk.CTkEntry(scroll, placeholder_text="Nombre del Estadio")
        entry_estadio_editor.pack(fill="x", pady=5)
        
        combo_color = ctk.CTkComboBox(scroll, values=list(COLORES_EQUIPOS.keys()), state="readonly")
        combo_color.pack(fill="x", pady=5)
        
        ctk.CTkLabel(scroll, text="Plantilla Titular:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Generar filas con (Posición + Dorsal + Nombre)
        entradas_jugadores = []
        posiciones_base = ["POR", "DEF", "DEF", "DEF", "DEF", "MED", "MED", "MED", "DEL", "DEL", "DEL"]
        
        for i in range(11):
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Etiqueta de posición base para guiar al usuario
            lbl = ctk.CTkLabel(row, text=posiciones_base[i], width=35, anchor="e", text_color="grey")
            lbl.pack(side="left", padx=(0, 5))
            
            # Caja para el número de camiseta
            num_entry = ctk.CTkEntry(row, width=40, placeholder_text="#")
            num_entry.pack(side="left", padx=(0, 5))
            
            # Caja para el nombre
            nom_entry = ctk.CTkEntry(row, placeholder_text="Nombre del Jugador")
            nom_entry.pack(side="left", fill="x", expand=True)
            
            entradas_jugadores.append((num_entry, nom_entry))
            
        def cargar_datos_al_formulario(seleccion):
            if seleccion in self.db.equipos:
                datos = self.db.equipos[seleccion]
                entry_nombre.delete(0, 'end')
                entry_nombre.insert(0, seleccion)
                
                entry_estadio_editor.delete(0, 'end')
                entry_estadio_editor.insert(0, datos.get("estadio", ""))
                
                combo_color.set(datos.get("color", "Blanco y Dorado (Llaneros)"))
                
                # Llenar cajas de número y nombre
                for i, j_data in enumerate(datos.get("jugadores", [])):
                    if i < len(entradas_jugadores):
                        num_e, nom_e = entradas_jugadores[i]
                        num_e.delete(0, 'end')
                        num_e.insert(0, str(j_data.get("numero", "")))
                        nom_e.delete(0, 'end')
                        nom_e.insert(0, str(j_data.get("nombre", "")))
                    
        def limpiar_formulario():
            entry_nombre.delete(0, 'end')
            entry_estadio_editor.delete(0, 'end')
            combo_color.set("Blanco y Dorado (Llaneros)")
            for num_e, nom_e in entradas_jugadores:
                num_e.delete(0, 'end')
                nom_e.delete(0, 'end')
            entry_nombre.focus()
            
        ctk.CTkButton(frame_top, text="✨ Crear de Cero", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=limpiar_formulario).pack(side="right", padx=10)

        combo_editar.configure(command=cargar_datos_al_formulario)
        cargar_datos_al_formulario(combo_editar.get())
        
        def guardar_equipo():
            nombre = entry_nombre.get().upper().strip()
            if not nombre: return
            
            estadio = entry_estadio_editor.get().upper().strip()
            
            # Recopilar lista de diccionarios {numero, nombre}
            jugadores_nuevos = []
            for num_e, nom_e in entradas_jugadores:
                n = nom_e.get().strip() or "Jugador"
                num = num_e.get().strip() or "-"
                jugadores_nuevos.append({"numero": num, "nombre": n})
            
            self.db.equipos[nombre] = {
                "color": combo_color.get(),
                "estadio": estadio,
                "jugadores": jugadores_nuevos
            }
            self.db.guardar_datos(self.db.equipos)
            
            lista_nueva = list(self.db.equipos.keys())
            self.combo_equipo_local.configure(values=lista_nueva)
            self.combo_equipo_visita.configure(values=lista_nueva)
            
            self.combo_equipo_local.set(nombre)
            self.cargar_equipo_local(nombre)
            
            ventana.destroy()
            
        ctk.CTkButton(ventana, text="💾 Guardar y Actualizar", fg_color="#43A047", hover_color="#2E7D32", command=guardar_equipo).pack(pady=15, padx=20, fill="x")

    def intercambiar_lados(self):
        eq_temp = self.combo_equipo_local.get()
        color_temp = self.combo_color_local.get()
        form_temp = self.combo_formacion_local.get()
        jugadores_temp = self.jugadores_local
        
        self.combo_equipo_local.set(self.combo_equipo_visita.get())
        self.combo_color_local.set(self.combo_color_visita.get())
        self.combo_formacion_local.set(self.combo_formacion_visita.get())
        self.jugadores_local = self.jugadores_visitante
        
        self.combo_equipo_visita.set(eq_temp)
        self.combo_color_visita.set(color_temp)
        self.combo_formacion_visita.set(form_temp)
        self.jugadores_visitante = jugadores_temp
        
        self.actualizar_todo()

    def cambiar_tema_cancha(self, seleccion):
        tema = ESTILOS_CANCHA[seleccion]
        self.mi_cancha.cambiar_estilo_cancha(tema["fondo"], tema["lineas"])

    def actualizar_todo(self, *args):
        l_name = self.combo_equipo_local.get()
        v_name = self.combo_equipo_visita.get()
        e_name = self.entry_estadio.get().upper()
        
        self.mi_cancha.actualizar_nombres_equipos(l_name, v_name, e_name)
        
        form_l = self.combo_formacion_local.get()
        col_l = self.combo_color_local.get()
        if form_l != "Seleccionar":
            self.mi_cancha.actualizar_equipo("local", form_l, self.jugadores_local, col_l)
            
        form_v = self.combo_formacion_visita.get()
        col_v = self.combo_color_visita.get()
        if form_v != "Seleccionar":
            self.mi_cancha.actualizar_equipo("visita", form_v, self.jugadores_visitante, col_v)

if __name__ == "__main__":
    app = AppNarrador()
    app.mainloop()