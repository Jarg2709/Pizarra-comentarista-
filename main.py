import customtkinter as ctk
from src.componentes.cancha_widget import CanchaWidget
from src.utils.constantes import *

ctk.set_appearance_mode("Dark")

class AppNarrador(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Narrador Pro - Responsive")
        self.geometry("1100x600")
        
        # IMPORTANTE: Permitir que la fila/columna se estire
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # 1. Cancha (Responsive)
        self.mi_cancha = CanchaWidget(master=self)
        self.mi_cancha.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 2. Panel
        self.panel = ctk.CTkFrame(master=self, width=250)
        self.panel.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)
        
        # Datos
        self.nombres_local = ["Dibu", "Molina", "Cuti", "Otamendi", "Taglia", "De Paul", "Enzo", "Mac A", "Messi", "Julian", "Di Maria"]
        self.nombres_visitante = ["Courtois", "Carvajal", "Militao", "Rudiger", "Mendy", "Cama", "Kroos", "Valverde", "Bellingham", "Vini", "Rodrygo"]

        self.construir_panel()

    def construir_panel(self):
        ctk.CTkLabel(self.panel, text="Panel Táctico", font=("Arial", 20, "bold")).pack(pady=10)

        # -- Inputs Nombres --
        self.entry_local = ctk.CTkEntry(self.panel, placeholder_text="Local")
        self.entry_local.insert(0, "LOCAL")
        self.entry_local.pack(pady=5, padx=10)
        
        self.entry_visita = ctk.CTkEntry(self.panel, placeholder_text="Visita")
        self.entry_visita.insert(0, "VISITA")
        self.entry_visita.pack(pady=5, padx=10)
        
        ctk.CTkButton(self.panel, text="Actualizar Nombres", command=self.actualizar_titulos).pack(pady=5)

        # -- Selectores --
        ctk.CTkLabel(self.panel, text="Formación Local:").pack(pady=(15,0))
        self.combo_local = ctk.CTkComboBox(self.panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], 
                                           command=self.cambio_local, state="readonly")
        self.combo_local.set("Seleccionar")
        self.combo_local.pack(pady=5)

        ctk.CTkLabel(self.panel, text="Formación Visita:").pack(pady=(15,0))
        self.combo_visita = ctk.CTkComboBox(self.panel, values=["4-4-2", "4-3-3", "4-2-3-1", "3-5-2"], 
                                            command=self.cambio_visita, state="readonly")
        self.combo_visita.set("Seleccionar")
        self.combo_visita.pack(pady=5)

    def actualizar_titulos(self):
        l = self.entry_local.get().upper()
        v = self.entry_visita.get().upper()
        self.mi_cancha.actualizar_nombres_equipos(l, v)

    def cambio_local(self, formacion):
        self.mi_cancha.actualizar_equipo("local", formacion, self.nombres_local)

    def cambio_visita(self, formacion):
        self.mi_cancha.actualizar_equipo("visita", formacion, self.nombres_visitante)

if __name__ == "__main__":
    app = AppNarrador()
    app.mainloop()