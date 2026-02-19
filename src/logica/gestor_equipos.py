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
                    # --- MIGRACIÓN AUTOMÁTICA ---
                    # Si el archivo antiguo solo tenía strings, lo actualiza al nuevo formato con números
                    for eq, info in datos.items():
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
        return {
            "LLANEROS FC": {
                "color": "Blanco y Dorado (Llaneros)",
                "estadio": "ESTADIO BELLO HORIZONTE - REY PELÉ",
                "jugadores": [
                    {"numero": "1", "nombre": "Armesto"}, {"numero": "2", "nombre": "Bogotá"},
                    {"numero": "3", "nombre": "Montes"}, {"numero": "4", "nombre": "Palacios"},
                    {"numero": "5", "nombre": "Guevara"}, {"numero": "6", "nombre": "Muñoz"},
                    {"numero": "7", "nombre": "Urueña"}, {"numero": "8", "nombre": "Gómez"},
                    {"numero": "9", "nombre": "Lazo"}, {"numero": "10", "nombre": "Ospina"},
                    {"numero": "11", "nombre": "Vergara"}
                ]
            },
            "ARGENTINA": {
                "color": "Celeste / Blanco (Arg)",
                "estadio": "ESTADIO MAS MONUMENTAL",
                "jugadores": [
                    {"numero": "23", "nombre": "Dibu"}, {"numero": "26", "nombre": "Molina"},
                    {"numero": "13", "nombre": "Cuti"}, {"numero": "19", "nombre": "Otamendi"},
                    {"numero": "3", "nombre": "Taglia"}, {"numero": "7", "nombre": "De Paul"},
                    {"numero": "24", "nombre": "Enzo"}, {"numero": "20", "nombre": "Mac A"},
                    {"numero": "10", "nombre": "Messi"}, {"numero": "9", "nombre": "Julian"},
                    {"numero": "11", "nombre": "Di Maria"}
                ]
            },
            "REAL MADRID": {
                "color": "Blanco (Madrid)",
                "estadio": "SANTIAGO BERNABÉU",
                "jugadores": [
                    {"numero": "1", "nombre": "Courtois"}, {"numero": "2", "nombre": "Carvajal"},
                    {"numero": "3", "nombre": "Militao"}, {"numero": "22", "nombre": "Rudiger"},
                    {"numero": "23", "nombre": "Mendy"}, {"numero": "12", "nombre": "Cama"},
                    {"numero": "8", "nombre": "Kroos"}, {"numero": "15", "nombre": "Valverde"},
                    {"numero": "5", "nombre": "Bellingham"}, {"numero": "7", "nombre": "Vini"},
                    {"numero": "11", "nombre": "Rodrygo"}
                ]
            }
        }