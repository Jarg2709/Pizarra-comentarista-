import json
import os

class GestorEquipos:
    def __init__(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Ruta donde se guardará el archivo de base de datos
        self.ruta_archivo = os.path.join(directorio_actual, "..", "..", "assets", "equipos.json")
        self.equipos = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    # Migración por si hay datos viejos
                    for eq, info in datos.items():
                        if "tecnico" not in info: info["tecnico"] = "Por Definir"
                        if "suplentes" not in info: info["suplentes"] = []
                        if "jugadores" in info and len(info["jugadores"]) > 0:
                            if isinstance(info["jugadores"][0], str):
                                info["jugadores"] = [{"numero": str(i+1), "nombre": n} for i, n in enumerate(info["jugadores"])]
                    return datos
            except Exception:
                pass
        return self._datos_por_defecto()

    def guardar_datos(self, datos_nuevos):
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_nuevos, f, indent=4, ensure_ascii=False)
        self.equipos = datos_nuevos

    def _datos_por_defecto(self):
        # BASE DE DATOS FPC ACTUALIZADA
        return {
            "LLANEROS FC": {
                "color": "Blanco y Dorado (Llaneros)", "estadio": "BELLO HORIZONTE - REY PELÉ", "tecnico": "Pedro Depablos",
                "jugadores": [
                    {"numero": "1", "nombre": "Armesto"}, {"numero": "2", "nombre": "Bogotá"}, {"numero": "3", "nombre": "Montes"},
                    {"numero": "4", "nombre": "Palacios"}, {"numero": "5", "nombre": "Guevara"}, {"numero": "6", "nombre": "Muñoz"},
                    {"numero": "7", "nombre": "Urueña"}, {"numero": "8", "nombre": "Gómez"}, {"numero": "9", "nombre": "Lazo"},
                    {"numero": "10", "nombre": "Ospina"}, {"numero": "11", "nombre": "Vergara"}
                ],
                "suplentes": [
                    {"numero": "12", "nombre": "Roa"}, {"numero": "14", "nombre": "Mendoza"}, {"numero": "15", "nombre": "Sierra"},
                    {"numero": "18", "nombre": "Pérez"}, {"numero": "20", "nombre": "García"}, {"numero": "21", "nombre": "López"}, {"numero": "25", "nombre": "Díaz"}
                ]
            },
            "MILLONARIOS FC": {
                "color": "Azul (Millonarios)", "estadio": "NEMESIO CAMACHO EL CAMPÍN", "tecnico": "Alberto Gamero",
                "jugadores": [
                    {"numero": "31", "nombre": "Montero"}, {"numero": "22", "nombre": "Del Valle"}, {"numero": "4", "nombre": "Vargas"},
                    {"numero": "26", "nombre": "Llinás"}, {"numero": "3", "nombre": "Arias"}, {"numero": "28", "nombre": "Stiven V."},
                    {"numero": "8", "nombre": "Giraldo"}, {"numero": "14", "nombre": "Silva"}, {"numero": "10", "nombre": "Cataño"},
                    {"numero": "23", "nombre": "L. Castro"}, {"numero": "9", "nombre": "Falcao"}
                ],
                "suplentes": [
                    {"numero": "1", "nombre": "Novoa"}, {"numero": "17", "nombre": "Ruiz"}, {"numero": "5", "nombre": "Paz"},
                    {"numero": "11", "nombre": "Mantilla"}, {"numero": "15", "nombre": "Córdoba"}, {"numero": "24", "nombre": "Ramírez"}, {"numero": "32", "nombre": "Giordana"}
                ]
            },
            "ATLÉTICO NACIONAL": {
                "color": "Verde (Nacional)", "estadio": "ATANASIO GIRARDOT", "tecnico": "Efraín Juárez",
                "jugadores": [
                    {"numero": "1", "nombre": "Marquinez"}, {"numero": "6", "nombre": "Aguirre"}, {"numero": "3", "nombre": "Tesillo"},
                    {"numero": "4", "nombre": "Campuzano"}, {"numero": "2", "nombre": "Angulo"}, {"numero": "20", "nombre": "Cepellini"},
                    {"numero": "8", "nombre": "Cardona"}, {"numero": "21", "nombre": "Sarmiento"}, {"numero": "10", "nombre": "Hinestroza"},
                    {"numero": "9", "nombre": "Morelos"}, {"numero": "11", "nombre": "Asprilla"}
                ],
                "suplentes": [
                    {"numero": "25", "nombre": "Castillo"}, {"numero": "14", "nombre": "Velásquez"}, {"numero": "19", "nombre": "Aristizábal"},
                    {"numero": "5", "nombre": "Guzmán"}, {"numero": "16", "nombre": "Castro"}, {"numero": "22", "nombre": "Mejía"}, {"numero": "29", "nombre": "Pabón"}
                ]
            },
            "AMÉRICA DE CALI": {
                "color": "Rojo Escarlata (América)", "estadio": "PASCUAL GUERRERO", "tecnico": "Polilla Da Silva",
                "jugadores": [
                    {"numero": "1", "nombre": "Soto"}, {"numero": "3", "nombre": "Mina"}, {"numero": "5", "nombre": "Bocanegra"},
                    {"numero": "2", "nombre": "Castrillón"}, {"numero": "22", "nombre": "Candelo"}, {"numero": "14", "nombre": "Leys"},
                    {"numero": "8", "nombre": "Rivera"}, {"numero": "10", "nombre": "Zapata"}, {"numero": "7", "nombre": "Vergara"},
                    {"numero": "11", "nombre": "Holgado"}, {"numero": "9", "nombre": "Ramos"}
                ],
                "suplentes": [
                    {"numero": "12", "nombre": "Graterol"}, {"numero": "4", "nombre": "Gómez"}, {"numero": "19", "nombre": "Barrios"},
                    {"numero": "15", "nombre": "Quiñones"}, {"numero": "21", "nombre": "Garcés"}, {"numero": "25", "nombre": "Escobar"}, {"numero": "30", "nombre": "Mena"}
                ]
            },
            "INDEPENDIENTE SANTA FE": {
                "color": "Rojo y Blanco (Santa Fe)", "estadio": "NEMESIO CAMACHO EL CAMPÍN", "tecnico": "Pablo Peirano",
                "jugadores": [
                    {"numero": "1", "nombre": "Mosquera M."}, {"numero": "3", "nombre": "Millán"}, {"numero": "4", "nombre": "Ortiz"},
                    {"numero": "29", "nombre": "Scarpeta"}, {"numero": "22", "nombre": "Perlaza"}, {"numero": "17", "nombre": "Meléndez"},
                    {"numero": "14", "nombre": "Torres"}, {"numero": "16", "nombre": "Zuluaga"}, {"numero": "10", "nombre": "Velásquez"},
                    {"numero": "11", "nombre": "Rodallega"}, {"numero": "9", "nombre": "Rodríguez"}
                ],
                "suplentes": [
                    {"numero": "12", "nombre": "Espitia"}, {"numero": "5", "nombre": "Agüero"}, {"numero": "8", "nombre": "Cuperman"},
                    {"numero": "20", "nombre": "Ovalle"}, {"numero": "23", "nombre": "López"}, {"numero": "28", "nombre": "Aristizábal"}, {"numero": "30", "nombre": "Correa"}
                ]
            },
            "JUNIOR DE BARRANQUILLA": {
                "color": "Rojiblanco (Junior)", "estadio": "METROPOLITANO ROBERTO MELÉNDEZ", "tecnico": "César Farías",
                "jugadores": [
                    {"numero": "77", "nombre": "Mele"}, {"numero": "18", "nombre": "Olivera"}, {"numero": "28", "nombre": "Peña"},
                    {"numero": "12", "nombre": "Fuentes"}, {"numero": "21", "nombre": "Pacheco"}, {"numero": "6", "nombre": "Moreno"},
                    {"numero": "24", "nombre": "Cantillo"}, {"numero": "99", "nombre": "Enamorado"}, {"numero": "8", "nombre": "Chará"},
                    {"numero": "70", "nombre": "Bacca"}, {"numero": "20", "nombre": "Pérez"}
                ],
                "suplentes": [
                    {"numero": "31", "nombre": "Martínez"}, {"numero": "3", "nombre": "Ceballos"}, {"numero": "10", "nombre": "Quintero"},
                    {"numero": "14", "nombre": "Hinojosa"}, {"numero": "16", "nombre": "Castrillón"}, {"numero": "23", "nombre": "Berrío"}, {"numero": "9", "nombre": "Lencina"}
                ]
            },
            "DEPORTES TOLIMA": {
                "color": "Vinotinto y Oro (Tolima)", "estadio": "MANUEL MURILLO TORO", "tecnico": "David González",
                "jugadores": [
                    {"numero": "1", "nombre": "Volpi"}, {"numero": "2", "nombre": "Angulo"}, {"numero": "3", "nombre": "Mera"},
                    {"numero": "4", "nombre": "Torres"}, {"numero": "20", "nombre": "Hurtado"}, {"numero": "14", "nombre": "Rovira"},
                    {"numero": "6", "nombre": "Nieto"}, {"numero": "10", "nombre": "Guzmán"}, {"numero": "11", "nombre": "Lucumí"},
                    {"numero": "7", "nombre": "Pérez"}, {"numero": "9", "nombre": "Gil"}
                ],
                "suplentes": [
                    {"numero": "12", "nombre": "Chaverra"}, {"numero": "5", "nombre": "Quiñones"}, {"numero": "15", "nombre": "Trujillo"},
                    {"numero": "17", "nombre": "Sosa"}, {"numero": "23", "nombre": "Hernández"}, {"numero": "27", "nombre": "Boné"}, {"numero": "30", "nombre": "Herazo"}
                ]
            },
            "ATLÉTICO BUCARAMANGA": {
                "color": "Amarillo (Bucaramanga)", "estadio": "AMÉRICO MONTANINI", "tecnico": "Rafael Dudamel",
                "jugadores": [
                    {"numero": "1", "nombre": "Quintana"}, {"numero": "2", "nombre": "Mena"}, {"numero": "3", "nombre": "Henao"},
                    {"numero": "4", "nombre": "Romaña"}, {"numero": "6", "nombre": "Gutiérrez"}, {"numero": "8", "nombre": "Flores"},
                    {"numero": "14", "nombre": "Castro"}, {"numero": "10", "nombre": "Sambueza"}, {"numero": "11", "nombre": "Mosquera"},
                    {"numero": "9", "nombre": "Córdoba"}, {"numero": "20", "nombre": "Ponce"}
                ],
                "suplentes": [
                    {"numero": "12", "nombre": "Varela"}, {"numero": "5", "nombre": "Zárate"}, {"numero": "15", "nombre": "Jiménez"},
                    {"numero": "17", "nombre": "Maza"}, {"numero": "21", "nombre": "Pérez"}, {"numero": "23", "nombre": "Torres"}, {"numero": "29", "nombre": "Valencia"}
                ]
            },
            "ONCE CALDAS": {
                "color": "Blanco (Blanco Blanco)", "estadio": "PALOGRANDE", "tecnico": "Hernán Darío Herrera",
                "jugadores": [
                    {"numero": "12", "nombre": "Aguirre"}, {"numero": "22", "nombre": "Palacios"}, {"numero": "3", "nombre": "Riquett"},
                    {"numero": "4", "nombre": "Cuesta"}, {"numero": "14", "nombre": "Patiño"}, {"numero": "6", "nombre": "Rojas"},
                    {"numero": "8", "nombre": "García"}, {"numero": "10", "nombre": "Torres"}, {"numero": "11", "nombre": "Arce"},
                    {"numero": "9", "nombre": "Moreno L."}, {"numero": "17", "nombre": "D. Moreno"}
                ],
                "suplentes": [
                    {"numero": "1", "nombre": "Mastrolía"}, {"numero": "5", "nombre": "Morán"}, {"numero": "15", "nombre": "García"},
                    {"numero": "19", "nombre": "Beltrán"}, {"numero": "20", "nombre": "Mejía"}, {"numero": "24", "nombre": "Araujo"}, {"numero": "27", "nombre": "Castaño"}
                ]
            }
        }