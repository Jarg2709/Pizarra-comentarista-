import os
import ctypes 
import tkinter as tk 
import customtkinter as ctk
from src.componentes.cancha_widget import CanchaWidget
from src.utils.constantes import *

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppNarrador(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Narrador Pro - Pizarra Táctica")
        self.geometry("1100x750") 
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_icono = os.path.join(directorio_actual, "assets", "icono.ico")
        
        try:
            myappid = 'narrador.pro.pizarra.v7'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
            
        if os.path.exists(ruta_icono):
            self.iconbitmap(ruta_icono)

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.mi_cancha = CanchaWidget(master=self)
        self.mi_cancha.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.panel = ctk.CTkFrame(master=self, width=300)
        self.panel.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)
        
        self.nombres_local = ["Dibu", "Molina", "Cuti", "Otamendi", "Taglia", "De Paul", "Enzo", "Mac A", "Messi", "Julian", "Di Maria"]
        self.nombres_visitante = ["Courtois", "Carvajal", "Militao", "Rudiger", "Mendy", "Cama", "Kroos", "Valverde", "Bellingham", "Vini", "Rodrygo"]

        self.construir_panel()

    def construir_panel(self):
        self.scroll_panel = ctk.CTkScrollableFrame(self.panel, width=280)
        self.scroll_panel.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.scroll_panel, text="Control Total", font=("Arial", 20, "bold")).pack(pady=10)

        # --- DATOS GENERALES ---
        ctk.CTkLabel(self.scroll_panel, text="🏟️ Nombre del Estadio:").pack(pady=(5,0))
        self.entry_estadio = ctk.CTkEntry(self.scroll_panel, placeholder_text="Ej: Wembley")
        self.entry_estadio.insert(0, "WEMBLEY STADIUM")
        self.entry_estadio.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.scroll_panel, text="Estilo de Pizarra:").pack(pady=(15,0))
        self.combo_estilo = ctk.CTkComboBox(self.scroll_panel, values=list(ESTILOS_CANCHA.keys()), command=self.cambiar_tema_cancha, state="readonly")
        self.combo_estilo.set("Pasto Clásico (Verde)")
        self.combo_estilo.pack(pady=5, padx=15, fill="x")
        
        ctk.CTkFrame(self.scroll_panel, height=2, fg_color="gray").pack(fill="x", pady=10, padx=15)

        # --- EQUIPO IZQUIERDA ---
        ctk.CTkLabel(self.scroll_panel, text="⬅️ EQUIPO IZQUIERDA ⬅️", font=("Arial", 12, "bold")).pack()
        self.entry_local = ctk.CTkEntry(self.scroll_panel, placeholder_text="Nombre Izquierda")
        self.entry_local.insert(0, "ARGENTINA")
        self.entry_local.pack(pady=5, padx=15, fill="x")
        
        self.combo_color_local = ctk.CTkComboBox(self.scroll_panel, values=list(COLORES_EQUIPOS.keys()), command=self.actualizar_todo, state="readonly")
        self.combo_color_local.set("Celeste / Blanco (Arg)")
        self.combo_color_local.pack(pady=5, padx=15, fill="x")

        self.combo_formacion_local = ctk.CTkComboBox(self.scroll_panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], command=self.actualizar_todo, state="readonly")
        self.combo_formacion_local.set("4-2-3-1")
        self.combo_formacion_local.pack(pady=5, padx=15, fill="x")

        # --- BOTÓN SEGUNDO TIEMPO ---
        ctk.CTkButton(self.scroll_panel, text="⚽ Segundo Tiempo (Cambiar Lados)", fg_color="#FBC02D", hover_color="#F9A825", text_color="black", font=("Arial", 12, "bold"), command=self.intercambiar_lados).pack(pady=15, padx=15, fill="x")

        # --- EQUIPO DERECHA ---
        ctk.CTkLabel(self.scroll_panel, text="➡️ EQUIPO DERECHA ➡️", font=("Arial", 12, "bold")).pack()
        self.entry_visita = ctk.CTkEntry(self.scroll_panel, placeholder_text="Nombre Derecha")
        self.entry_visita.insert(0, "REAL MADRID")
        self.entry_visita.pack(pady=5, padx=15, fill="x")
        
        self.combo_color_visita = ctk.CTkComboBox(self.scroll_panel, values=list(COLORES_EQUIPOS.keys()), command=self.actualizar_todo, state="readonly")
        self.combo_color_visita.set("Blanco (Madrid)")
        self.combo_color_visita.pack(pady=5, padx=15, fill="x")

        self.combo_formacion_visita = ctk.CTkComboBox(self.scroll_panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], command=self.actualizar_todo, state="readonly")
        self.combo_formacion_visita.set("4-3-3")
        self.combo_formacion_visita.pack(pady=5, padx=15, fill="x")

        ctk.CTkFrame(self.scroll_panel, height=2, fg_color="gray").pack(fill="x", pady=15, padx=15)
        ctk.CTkButton(self.scroll_panel, text="Refrescar Nombres", command=self.actualizar_todo).pack(pady=5, padx=15, fill="x")
        
        self.actualizar_todo()

    def intercambiar_lados(self):
        nom_temp = self.entry_local.get()
        color_temp = self.combo_color_local.get()
        form_temp = self.combo_formacion_local.get()
        jugadores_temp = self.nombres_local
        
        self.entry_local.delete(0, 'end')
        self.entry_local.insert(0, self.entry_visita.get())
        self.combo_color_local.set(self.combo_color_visita.get())
        self.combo_formacion_local.set(self.combo_formacion_visita.get())
        self.nombres_local = self.nombres_visitante
        
        self.entry_visita.delete(0, 'end')
        self.entry_visita.insert(0, nom_temp)
        self.combo_color_visita.set(color_temp)
        self.combo_formacion_visita.set(form_temp)
        self.nombres_visitante = jugadores_temp
        
        self.actualizar_todo()

    def cambiar_tema_cancha(self, seleccion):
        tema = ESTILOS_CANCHA[seleccion]
        self.mi_cancha.cambiar_estilo_cancha(tema["fondo"], tema["lineas"])

    def actualizar_todo(self, *args):
        l_name = self.entry_local.get().upper()
        v_name = self.entry_visita.get().upper()
        e_name = self.entry_estadio.get().upper()
        
        self.mi_cancha.actualizar_nombres_equipos(l_name, v_name, e_name)
        
        form_l = self.combo_formacion_local.get()
        col_l = self.combo_color_local.get()
        if form_l != "Seleccionar":
            self.mi_cancha.actualizar_equipo("local", form_l, self.nombres_local, col_l)
            
        form_v = self.combo_formacion_visita.get()
        col_v = self.combo_color_visita.get()
        if form_v != "Seleccionar":
            self.mi_cancha.actualizar_equipo("visita", form_v, self.nombres_visitante, col_v)

if __name__ == "__main__":
    app = AppNarrador()
    app.mainloop()