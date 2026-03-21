import json
import os

class GestorEquipos:
    def __init__(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_archivo = os.path.join(directorio_actual, "..", "..", "assets", "equipos.json")
        self.equipos = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    for eq, info in datos.items():
                        if "tecnico" not in info: info["tecnico"] = "Por Definir"
                        if "suplentes" not in info: info["suplentes"] = []
                        # Migración de colores viejos a estructura de uniformes
                        if "uniformes" not in info: 
                            info["uniformes"] = {"Local": {"bg": "#FFFFFF", "fg": "#000000"}, "Visita": {"bg": "#111111", "fg": "#FFFFFF"}}
                        if "jugadores" in info and len(info["jugadores"]) > 0:
                            if isinstance(info["jugadores"][0], str):
                                info["jugadores"] = [{"numero": str(i+1), "nombre": n} for i, n in enumerate(info["jugadores"])]
                    return datos
            except Exception: pass
        return self._datos_por_defecto()

    def guardar_datos(self, datos_nuevos):
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_nuevos, f, indent=4, ensure_ascii=False)
        self.equipos = datos_nuevos

    def _datos_por_defecto(self):
        return {
            "LLANEROS FC": {
                "estadio": "BELLO HORIZONTE", "tecnico": "Pedro Depablos",
                "uniformes": {"Local (Blanco)": {"bg": "#FFFFFF", "fg": "#D4AF37"}, "Visita (Negro)": {"bg": "#111111", "fg": "#D4AF37"}},
                "jugadores": [{"numero": "1", "nombre": "Armesto"}, {"numero": "2", "nombre": "Bogotá"}, {"numero": "3", "nombre": "Montes"}, {"numero": "4", "nombre": "Palacios"}, {"numero": "5", "nombre": "Guevara"}, {"numero": "6", "nombre": "Muñoz"}, {"numero": "7", "nombre": "Urueña"}, {"numero": "8", "nombre": "Gómez"}, {"numero": "9", "nombre": "Lazo"}, {"numero": "10", "nombre": "Ospina"}, {"numero": "11", "nombre": "Vergara"}],
                "suplentes": [{"numero": "12", "nombre": "Roa"}, {"numero": "14", "nombre": "Mendoza"}, {"numero": "15", "nombre": "Sierra"}, {"numero": "18", "nombre": "Pérez"}, {"numero": "20", "nombre": "García"}, {"numero": "21", "nombre": "López"}, {"numero": "25", "nombre": "Díaz"}]
            },
            "MILLONARIOS FC": {
                "estadio": "NEMESIO CAMACHO EL CAMPÍN", "tecnico": "Alberto Gamero",
                "uniformes": {"Local (Azul)": {"bg": "#0D47A1", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#0D47A1"}},
                "jugadores": [{"numero": "31", "nombre": "Montero"}, {"numero": "22", "nombre": "Del Valle"}, {"numero": "4", "nombre": "Vargas"}, {"numero": "26", "nombre": "Llinás"}, {"numero": "3", "nombre": "Arias"}, {"numero": "28", "nombre": "Stiven V."}, {"numero": "8", "nombre": "Giraldo"}, {"numero": "14", "nombre": "Silva"}, {"numero": "10", "nombre": "Cataño"}, {"numero": "23", "nombre": "L. Castro"}, {"numero": "9", "nombre": "Falcao"}],
                "suplentes": [{"numero": "1", "nombre": "Novoa"}, {"numero": "17", "nombre": "Ruiz"}, {"numero": "5", "nombre": "Paz"}, {"numero": "11", "nombre": "Mantilla"}, {"numero": "15", "nombre": "Córdoba"}, {"numero": "24", "nombre": "Ramírez"}, {"numero": "32", "nombre": "Giordana"}]
            },
            "ATLÉTICO NACIONAL": {
                "estadio": "ATANASIO GIRARDOT", "tecnico": "Efraín Juárez",
                "uniformes": {"Local (Verde)": {"bg": "#2E7D32", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#2E7D32"}},
                "jugadores": [{"numero": "1", "nombre": "Marquinez"}, {"numero": "6", "nombre": "Aguirre"}, {"numero": "3", "nombre": "Tesillo"}, {"numero": "4", "nombre": "Campuzano"}, {"numero": "2", "nombre": "Angulo"}, {"numero": "20", "nombre": "Cepellini"}, {"numero": "8", "nombre": "Cardona"}, {"numero": "21", "nombre": "Sarmiento"}, {"numero": "10", "nombre": "Hinestroza"}, {"numero": "9", "nombre": "Morelos"}, {"numero": "11", "nombre": "Asprilla"}],
                "suplentes": [{"numero": "25", "nombre": "Castillo"}, {"numero": "14", "nombre": "Velásquez"}, {"numero": "19", "nombre": "Aristizábal"}, {"numero": "5", "nombre": "Guzmán"}, {"numero": "16", "nombre": "Castro"}, {"numero": "22", "nombre": "Mejía"}, {"numero": "29", "nombre": "Pabón"}]
            },
            "AMÉRICA DE CALI": {
                "estadio": "PASCUAL GUERRERO", "tecnico": "Polilla Da Silva",
                "uniformes": {"Local (Rojo)": {"bg": "#C62828", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#C62828"}},
                "jugadores": [{"numero": "1", "nombre": "Soto"}, {"numero": "3", "nombre": "Mina"}, {"numero": "5", "nombre": "Bocanegra"}, {"numero": "2", "nombre": "Castrillón"}, {"numero": "22", "nombre": "Candelo"}, {"numero": "14", "nombre": "Leys"}, {"numero": "8", "nombre": "Rivera"}, {"numero": "10", "nombre": "Zapata"}, {"numero": "7", "nombre": "Vergara"}, {"numero": "11", "nombre": "Holgado"}, {"numero": "9", "nombre": "Ramos"}],
                "suplentes": [{"numero": "12", "nombre": "Graterol"}, {"numero": "4", "nombre": "Gómez"}, {"numero": "19", "nombre": "Barrios"}, {"numero": "15", "nombre": "Quiñones"}, {"numero": "21", "nombre": "Garcés"}, {"numero": "25", "nombre": "Escobar"}, {"numero": "30", "nombre": "Mena"}]
            },
            "INDEPENDIENTE SANTA FE": {
                "estadio": "EL CAMPÍN", "tecnico": "Pablo Peirano",
                "uniformes": {"Local (Rojiblanco)": {"bg": "#E53935", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#E53935"}},
                "jugadores": [{"numero": "1", "nombre": "Mosquera M."}, {"numero": "3", "nombre": "Millán"}, {"numero": "4", "nombre": "Ortiz"}, {"numero": "29", "nombre": "Scarpeta"}, {"numero": "22", "nombre": "Perlaza"}, {"numero": "17", "nombre": "Meléndez"}, {"numero": "14", "nombre": "Torres"}, {"numero": "16", "nombre": "Zuluaga"}, {"numero": "10", "nombre": "Velásquez"}, {"numero": "11", "nombre": "Rodallega"}, {"numero": "9", "nombre": "Rodríguez"}],
                "suplentes": [{"numero": "12", "nombre": "Espitia"}, {"numero": "5", "nombre": "Agüero"}, {"numero": "8", "nombre": "Cuperman"}, {"numero": "20", "nombre": "Ovalle"}, {"numero": "23", "nombre": "López"}, {"numero": "28", "nombre": "Aristizábal"}, {"numero": "30", "nombre": "Correa"}]
            },
            "JUNIOR DE BARRANQUILLA": {
                "estadio": "METROPOLITANO", "tecnico": "César Farías",
                "uniformes": {"Local (Rojiblanco)": {"bg": "#FFFFFF", "fg": "#C62828"}, "Visita (Azul Oscuro)": {"bg": "#1A237E", "fg": "white"}},
                "jugadores": [{"numero": "77", "nombre": "Mele"}, {"numero": "18", "nombre": "Olivera"}, {"numero": "28", "nombre": "Peña"}, {"numero": "12", "nombre": "Fuentes"}, {"numero": "21", "nombre": "Pacheco"}, {"numero": "6", "nombre": "Moreno"}, {"numero": "24", "nombre": "Cantillo"}, {"numero": "99", "nombre": "Enamorado"}, {"numero": "8", "nombre": "Chará"}, {"numero": "70", "nombre": "Bacca"}, {"numero": "20", "nombre": "Pérez"}],
                "suplentes": [{"numero": "31", "nombre": "Martínez"}, {"numero": "3", "nombre": "Ceballos"}, {"numero": "10", "nombre": "Quintero"}, {"numero": "14", "nombre": "Hinojosa"}, {"numero": "16", "nombre": "Castrillón"}, {"numero": "23", "nombre": "Berrío"}, {"numero": "9", "nombre": "Lencina"}]
            },
            "DEPORTES TOLIMA": {
                "estadio": "MANUEL MURILLO TORO", "tecnico": "David González",
                "uniformes": {"Local (Vinotinto)": {"bg": "#5D4037", "fg": "#FBC02D"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#5D4037"}},
                "jugadores": [{"numero": "1", "nombre": "Volpi"}, {"numero": "2", "nombre": "Angulo"}, {"numero": "3", "nombre": "Mera"}, {"numero": "4", "nombre": "Torres"}, {"numero": "20", "nombre": "Hurtado"}, {"numero": "14", "nombre": "Rovira"}, {"numero": "6", "nombre": "Nieto"}, {"numero": "10", "nombre": "Guzmán"}, {"numero": "11", "nombre": "Lucumí"}, {"numero": "7", "nombre": "Pérez"}, {"numero": "9", "nombre": "Gil"}],
                "suplentes": [{"numero": "12", "nombre": "Chaverra"}, {"numero": "5", "nombre": "Quiñones"}, {"numero": "15", "nombre": "Trujillo"}, {"numero": "17", "nombre": "Sosa"}, {"numero": "23", "nombre": "Hernández"}, {"numero": "27", "nombre": "Boné"}, {"numero": "30", "nombre": "Herazo"}]
            },
            "ATLÉTICO BUCARAMANGA": {
                "estadio": "AMÉRICO MONTANINI", "tecnico": "Rafael Dudamel",
                "uniformes": {"Local (Amarillo)": {"bg": "#FDD835", "fg": "black"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#FDD835"}},
                "jugadores": [{"numero": "1", "nombre": "Quintana"}, {"numero": "2", "nombre": "Mena"}, {"numero": "3", "nombre": "Henao"}, {"numero": "4", "nombre": "Romaña"}, {"numero": "6", "nombre": "Gutiérrez"}, {"numero": "8", "nombre": "Flores"}, {"numero": "14", "nombre": "Castro"}, {"numero": "10", "nombre": "Sambueza"}, {"numero": "11", "nombre": "Mosquera"}, {"numero": "9", "nombre": "Córdoba"}, {"numero": "20", "nombre": "Ponce"}],
                "suplentes": [{"numero": "12", "nombre": "Varela"}, {"numero": "5", "nombre": "Zárate"}, {"numero": "15", "nombre": "Jiménez"}, {"numero": "17", "nombre": "Maza"}, {"numero": "21", "nombre": "Pérez"}, {"numero": "23", "nombre": "Torres"}, {"numero": "29", "nombre": "Valencia"}]
            },
            "ONCE CALDAS": {
                "estadio": "PALOGRANDE", "tecnico": "Hernán Darío Herrera",
                "uniformes": {"Local (Blanco)": {"bg": "#FFFFFF", "fg": "black"}, "Visita (Negro)": {"bg": "#111111", "fg": "white"}},
                "jugadores": [{"numero": "12", "nombre": "Aguirre"}, {"numero": "22", "nombre": "Palacios"}, {"numero": "3", "nombre": "Riquett"}, {"numero": "4", "nombre": "Cuesta"}, {"numero": "14", "nombre": "Patiño"}, {"numero": "6", "nombre": "Rojas"}, {"numero": "8", "nombre": "García"}, {"numero": "10", "nombre": "Torres"}, {"numero": "11", "nombre": "Arce"}, {"numero": "9", "nombre": "Moreno L."}, {"numero": "17", "nombre": "D. Moreno"}],
                "suplentes": [{"numero": "1", "nombre": "Mastrolía"}, {"numero": "5", "nombre": "Morán"}, {"numero": "15", "nombre": "García"}, {"numero": "19", "nombre": "Beltrán"}, {"numero": "20", "nombre": "Mejía"}, {"numero": "24", "nombre": "Araujo"}, {"numero": "27", "nombre": "Castaño"}]
            },
            "INDEPENDIENTE MEDELLÍN": {
                "estadio": "ATANASIO GIRARDOT", "tecnico": "Alejandro Restrepo",
                "uniformes": {"Local (Rojo/Azul)": {"bg": "#C62828", "fg": "#0D47A1"}, "Visita (Azul)": {"bg": "#0D47A1", "fg": "white"}},
                "jugadores": [{"numero": "1", "nombre": "Chaux"}, {"numero": "2", "nombre": "Ortiz"}, {"numero": "3", "nombre": "Torijano"}, {"numero": "24", "nombre": "Fory"}, {"numero": "29", "nombre": "Chaverra"}, {"numero": "5", "nombre": "Alvarado"}, {"numero": "6", "nombre": "Lima"}, {"numero": "10", "nombre": "Monsalve"}, {"numero": "11", "nombre": "Sandoval"}, {"numero": "9", "nombre": "León"}, {"numero": "27", "nombre": "Arizala"}],
                "suplentes": [{"numero": "12", "nombre": "Gómez"}, {"numero": "4", "nombre": "Palacios"}, {"numero": "15", "nombre": "Escobar"}, {"numero": "17", "nombre": "García"}, {"numero": "20", "nombre": "Martínez"}, {"numero": "22", "nombre": "Peralta"}, {"numero": "30", "nombre": "Muñiz"}]
            },
            "DEPORTIVO CALI": {
                "estadio": "ESTADIO DEPORTIVO CALI", "tecnico": "Sergio Herrera",
                "uniformes": {"Local (Verde)": {"bg": "#1B5E20", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#1B5E20"}},
                "jugadores": [{"numero": "1", "nombre": "Guruceaga"}, {"numero": "22", "nombre": "Marulanda"}, {"numero": "3", "nombre": "Meza"}, {"numero": "4", "nombre": "Caldera"}, {"numero": "20", "nombre": "Gómez"}, {"numero": "5", "nombre": "Mejía"}, {"numero": "8", "nombre": "Osorio"}, {"numero": "10", "nombre": "Barrera"}, {"numero": "11", "nombre": "Estupiñán"}, {"numero": "17", "nombre": "Andrade"}, {"numero": "9", "nombre": "Montero"}],
                "suplentes": [{"numero": "12", "nombre": "Rodríguez"}, {"numero": "2", "nombre": "Franco"}, {"numero": "15", "nombre": "Cabezas"}, {"numero": "19", "nombre": "Bustos"}, {"numero": "21", "nombre": "Castillo"}, {"numero": "24", "nombre": "Córdoba"}, {"numero": "29", "nombre": "Villegas"}]
            },
            "DEPORTIVO PEREIRA": {
                "estadio": "HERNÁN RAMÍREZ VILLEGAS", "tecnico": "Luis Fernando Suárez",
                "uniformes": {"Local (Amarillo/Rojo)": {"bg": "#FDD835", "fg": "#C62828"}, "Visita (Negro)": {"bg": "#111111", "fg": "#FDD835"}},
                "jugadores": [{"numero": "1", "nombre": "Ichazo"}, {"numero": "3", "nombre": "Moya"}, {"numero": "4", "nombre": "Pestaña"}, {"numero": "2", "nombre": "Garcés"}, {"numero": "13", "nombre": "Aguilar"}, {"numero": "20", "nombre": "Ríos"}, {"numero": "25", "nombre": "Murillo"}, {"numero": "10", "nombre": "Darwin Q."}, {"numero": "11", "nombre": "Ibargüen"}, {"numero": "9", "nombre": "Lencina"}, {"numero": "7", "nombre": "Piedrahita"}],
                "suplentes": [{"numero": "22", "nombre": "Mosquera"}, {"numero": "5", "nombre": "Giraldo"}, {"numero": "8", "nombre": "Rojas"}, {"numero": "14", "nombre": "Berrío"}, {"numero": "17", "nombre": "Pacheco"}, {"numero": "21", "nombre": "Cabrera"}, {"numero": "29", "nombre": "Valencia"}]
            },
            "LA EQUIDAD": {
                "estadio": "METROPOLITANO DE TECHO", "tecnico": "Alexis García",
                "uniformes": {"Local (Verde)": {"bg": "#2E7D32", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#2E7D32"}},
                "jugadores": [{"numero": "1", "nombre": "Ortega"}, {"numero": "20", "nombre": "Polanco"}, {"numero": "3", "nombre": "Payares"}, {"numero": "4", "nombre": "Mina"}, {"numero": "5", "nombre": "Correa"}, {"numero": "6", "nombre": "Ricardo"}, {"numero": "8", "nombre": "Acosta"}, {"numero": "10", "nombre": "Chaverra"}, {"numero": "7", "nombre": "Rojas"}, {"numero": "9", "nombre": "Viveros"}, {"numero": "11", "nombre": "Castillo"}],
                "suplentes": [{"numero": "12", "nombre": "Pérez"}, {"numero": "2", "nombre": "Lloreda"}, {"numero": "14", "nombre": "Ceballos"}, {"numero": "17", "nombre": "Salazar"}, {"numero": "21", "nombre": "Banguero"}, {"numero": "23", "nombre": "Escobar"}, {"numero": "28", "nombre": "Gómez"}]
            },
            "ÁGUILAS DORADAS": {
                "estadio": "ARTURO CUMPLIDO", "tecnico": "José Luis García",
                "uniformes": {"Local (Dorado)": {"bg": "#D4AF37", "fg": "black"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#D4AF37"}},
                "jugadores": [{"numero": "1", "nombre": "Contreras"}, {"numero": "4", "nombre": "Quiñónes"}, {"numero": "3", "nombre": "Pestaña"}, {"numero": "2", "nombre": "Varela"}, {"numero": "17", "nombre": "Celis"}, {"numero": "8", "nombre": "Rivas"}, {"numero": "5", "nombre": "Pineda"}, {"numero": "10", "nombre": "Caballero"}, {"numero": "7", "nombre": "Salazar"}, {"numero": "9", "nombre": "Pérez"}, {"numero": "11", "nombre": "Estacio"}],
                "suplentes": [{"numero": "12", "nombre": "Martínez"}, {"numero": "6", "nombre": "Lara"}, {"numero": "14", "nombre": "Gómez"}, {"numero": "19", "nombre": "Ramos"}, {"numero": "22", "nombre": "Díaz"}, {"numero": "25", "nombre": "Moreno"}, {"numero": "30", "nombre": "Vuletich"}]
            },
            "DEPORTIVO PASTO": {
                "estadio": "DEPARTAMENTAL LIBERTAD", "tecnico": "Gustavo Florentín",
                "uniformes": {"Local (Tricolor)": {"bg": "#0D47A1", "fg": "#E53935"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#0D47A1"}},
                "jugadores": [{"numero": "1", "nombre": "Martínez"}, {"numero": "20", "nombre": "Alba"}, {"numero": "3", "nombre": "Malagón"}, {"numero": "4", "nombre": "Figueroa"}, {"numero": "2", "nombre": "Mafla"}, {"numero": "5", "nombre": "Ayala"}, {"numero": "8", "nombre": "Roa"}, {"numero": "10", "nombre": "Londoño"}, {"numero": "7", "nombre": "Tréllez"}, {"numero": "9", "nombre": "Escobar"}, {"numero": "11", "nombre": "Campuzano"}],
                "suplentes": [{"numero": "12", "nombre": "Espínola"}, {"numero": "6", "nombre": "Pino"}, {"numero": "14", "nombre": "Rendón"}, {"numero": "17", "nombre": "Chávez"}, {"numero": "21", "nombre": "Castilla"}, {"numero": "25", "nombre": "Campaña"}, {"numero": "29", "nombre": "Ramos"}]
            },
            "ENVIGADO FC": {
                "estadio": "POLIDEPORTIVO SUR", "tecnico": "Andrés Orozco",
                "uniformes": {"Local (Naranja)": {"bg": "#FF9800", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#FF9800"}},
                "jugadores": [{"numero": "1", "nombre": "Parra"}, {"numero": "2", "nombre": "Cuervo"}, {"numero": "3", "nombre": "Palacios"}, {"numero": "4", "nombre": "Noreña"}, {"numero": "17", "nombre": "Rodallega"}, {"numero": "6", "nombre": "Jaramillo"}, {"numero": "8", "nombre": "Villa"}, {"numero": "10", "nombre": "Moreno"}, {"numero": "7", "nombre": "Díaz"}, {"numero": "9", "nombre": "Garcés"}, {"numero": "11", "nombre": "Hurtado"}],
                "suplentes": [{"numero": "12", "nombre": "Soto"}, {"numero": "5", "nombre": "Gómez"}, {"numero": "14", "nombre": "Banguera"}, {"numero": "19", "nombre": "Carcabal"}, {"numero": "21", "nombre": "García"}, {"numero": "25", "nombre": "Zapata"}, {"numero": "30", "nombre": "Pérez"}]
            },
            "BOYACÁ CHICÓ": {
                "estadio": "LA INDEPENDENCIA", "tecnico": "Jhon Jairo Gómez",
                "uniformes": {"Local (Ajedrezado)": {"bg": "#000000", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#000000"}},
                "jugadores": [{"numero": "1", "nombre": "Caicedo"}, {"numero": "2", "nombre": "Alfonzo"}, {"numero": "3", "nombre": "Plazas"}, {"numero": "4", "nombre": "Banguero"}, {"numero": "17", "nombre": "Pérez"}, {"numero": "6", "nombre": "Lozano"}, {"numero": "8", "nombre": "Támara"}, {"numero": "10", "nombre": "Cruz"}, {"numero": "7", "nombre": "Aleo"}, {"numero": "9", "nombre": "Gómez"}, {"numero": "11", "nombre": "Balanta"}],
                "suplentes": [{"numero": "12", "nombre": "Ortega"}, {"numero": "5", "nombre": "Mosquera"}, {"numero": "14", "nombre": "Soto"}, {"numero": "19", "nombre": "Londoño"}, {"numero": "22", "nombre": "Moreno"}, {"numero": "27", "nombre": "Peña"}, {"numero": "30", "nombre": "Castaño"}]
            },
            "JAGUARES DE CÓRDOBA": {
                "estadio": "JARAGUAY", "tecnico": "Edgar Carvajal",
                "uniformes": {"Local (Celeste)": {"bg": "#4FC3F7", "fg": "black"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#4FC3F7"}},
                "jugadores": [{"numero": "1", "nombre": "Figueroa"}, {"numero": "20", "nombre": "Meléndez"}, {"numero": "3", "nombre": "Páez"}, {"numero": "4", "nombre": "Escorcia"}, {"numero": "2", "nombre": "Castaño"}, {"numero": "5", "nombre": "Serje"}, {"numero": "8", "nombre": "Roa"}, {"numero": "10", "nombre": "Rojas"}, {"numero": "7", "nombre": "Díaz"}, {"numero": "9", "nombre": "Morelo"}, {"numero": "11", "nombre": "Mosquera"}],
                "suplentes": [{"numero": "12", "nombre": "Banguera"}, {"numero": "6", "nombre": "García"}, {"numero": "14", "nombre": "Medrano"}, {"numero": "17", "nombre": "Villalobos"}, {"numero": "21", "nombre": "Padilla"}, {"numero": "25", "nombre": "Gómez"}, {"numero": "29", "nombre": "Anaya"}]
            },
            "PATRIOTAS BOYACÁ": {
                "estadio": "LA INDEPENDENCIA", "tecnico": "Dayron Pérez",
                "uniformes": {"Local (Rojo)": {"bg": "#B71C1C", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#B71C1C"}},
                "jugadores": [{"numero": "1", "nombre": "Valencia"}, {"numero": "2", "nombre": "Roa"}, {"numero": "3", "nombre": "García"}, {"numero": "4", "nombre": "Alarcón"}, {"numero": "17", "nombre": "De las Salas"}, {"numero": "6", "nombre": "Díaz"}, {"numero": "8", "nombre": "Pérez"}, {"numero": "10", "nombre": "Aristizábal"}, {"numero": "7", "nombre": "Ruiz"}, {"numero": "9", "nombre": "Córdoba"}, {"numero": "11", "nombre": "Martínez"}],
                "suplentes": [{"numero": "12", "nombre": "Román"}, {"numero": "5", "nombre": "Banguero"}, {"numero": "14", "nombre": "Salas"}, {"numero": "19", "nombre": "Victoria"}, {"numero": "21", "nombre": "Peña"}, {"numero": "25", "nombre": "Ramos"}, {"numero": "30", "nombre": "Viveros"}]
            },
            "FORTALEZA CEIF": {
                "estadio": "METROPOLITANO DE TECHO", "tecnico": "Sebastián Oliveros",
                "uniformes": {"Local (Azul)": {"bg": "#0277BD", "fg": "white"}, "Visita (Blanco)": {"bg": "#FFFFFF", "fg": "#0277BD"}},
                "jugadores": [{"numero": "1", "nombre": "Castillo"}, {"numero": "20", "nombre": "Hinestroza"}, {"numero": "3", "nombre": "Rivera"}, {"numero": "4", "nombre": "Morález"}, {"numero": "2", "nombre": "Díaz"}, {"numero": "5", "nombre": "Pico"}, {"numero": "8", "nombre": "Pájaro"}, {"numero": "10", "nombre": "Lucumí"}, {"numero": "7", "nombre": "Arrieta"}, {"numero": "9", "nombre": "Parra"}, {"numero": "11", "nombre": "Alarcón"}],
                "suplentes": [{"numero": "12", "nombre": "Gómez"}, {"numero": "6", "nombre": "Cortés"}, {"numero": "14", "nombre": "Navarro"}, {"numero": "17", "nombre": "Garcés"}, {"numero": "21", "nombre": "Rodríguez"}, {"numero": "25", "nombre": "Castañeda"}, {"numero": "29", "nombre": "Pérez"}]
            },
            "ALIANZA FC": {
                "estadio": "ARMANDO MAESTRE", "tecnico": "Hubert Bodhert",
                "uniformes": {"Local (Tricolor)": {"bg": "#FFFFFF", "fg": "black"}, "Visita (Negro)": {"bg": "#111111", "fg": "white"}},
                "jugadores": [{"numero": "1", "nombre": "Grazziani"}, {"numero": "2", "nombre": "Navarro"}, {"numero": "3", "nombre": "Ospina"}, {"numero": "4", "nombre": "Franco"}, {"numero": "17", "nombre": "Saldaña"}, {"numero": "6", "nombre": "Manjarrés"}, {"numero": "8", "nombre": "Castillo"}, {"numero": "10", "nombre": "Acosta"}, {"numero": "7", "nombre": "Batalla"}, {"numero": "9", "nombre": "Rentería"}, {"numero": "11", "nombre": "Garcés"}],
                "suplentes": [{"numero": "12", "nombre": "Mosquera"}, {"numero": "5", "nombre": "Simanca"}, {"numero": "14", "nombre": "Torres"}, {"numero": "19", "nombre": "Cárdenas"}, {"numero": "21", "nombre": "García"}, {"numero": "25", "nombre": "Valdés"}, {"numero": "30", "nombre": "Gómez"}]
            }
        }