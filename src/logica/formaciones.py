class GestorFormaciones:
    @staticmethod
    def obtener_coordenadas_local(formacion, w, h):
        """
        Calcula posiciones relativas al ancho (w) y alto (h).
        Equipo Local: Juega de 0 a 50% del ancho.
        """
        cy = h / 2          # Centro Vertical
        # Posiciones X relativas (porcentajes del ancho total)
        x_arq = w * 0.05    # Arquero al 5%
        x_def = w * 0.15    # Defensas al 15%
        x_med = w * 0.30    # Medios al 30%
        x_del = w * 0.42    # Delanteros al 42%

        # Separación vertical relativa (spread)
        dy_def = h * 0.18   # Separación entre defensas
        dy_med = h * 0.18
        dy_del = h * 0.20

        # Tácticas
        if formacion == "4-4-2":
            return [
                (x_arq, cy),
                (x_def, cy - 1.5*dy_def), (x_def, cy - 0.5*dy_def), (x_def, cy + 0.5*dy_def), (x_def, cy + 1.5*dy_def),
                (x_med, cy - 1.5*dy_med), (x_med, cy - 0.5*dy_med), (x_med, cy + 0.5*dy_med), (x_med, cy + 1.5*dy_med),
                (x_del, cy - 0.5*dy_del), (x_del, cy + 0.5*dy_del)
            ]
        elif formacion == "4-3-3":
            return [
                (x_arq, cy),
                (x_def, cy - 1.5*dy_def), (x_def, cy - 0.5*dy_def), (x_def, cy + 0.5*dy_def), (x_def, cy + 1.5*dy_def),
                (x_med - (w*0.02), cy), (x_med + (w*0.02), cy - dy_med), (x_med + (w*0.02), cy + dy_med), # Triángulo medios
                (x_del, cy), (x_del, cy - 1.2*dy_del), (x_del, cy + 1.2*dy_del)
            ]
        elif formacion == "4-2-3-1":
            return [
                (x_arq, cy),
                (x_def, cy - 1.5*dy_def), (x_def, cy - 0.5*dy_def), (x_def, cy + 0.5*dy_def), (x_def, cy + 1.5*dy_def),
                (x_med - (w*0.05), cy - 0.5*dy_med), (x_med - (w*0.05), cy + 0.5*dy_med), # Pivotes
                (x_med + (w*0.05), cy), (x_med + (w*0.05), cy - 1.2*dy_med), (x_med + (w*0.05), cy + 1.2*dy_med), # Mediapuntas
                (x_del + (w*0.02), cy)
            ]
        elif formacion == "3-5-2":
            return [
                (x_arq, cy),
                (x_def, cy), (x_def, cy - dy_def), (x_def, cy + dy_def), # 3 Centrales
                (x_med, cy), (x_med, cy - dy_med), (x_med, cy + dy_med), (x_med + (w*0.05), cy - 2*dy_med), (x_med + (w*0.05), cy + 2*dy_med), # 5 Medios
                (x_del, cy - 0.5*dy_del), (x_del, cy + 0.5*dy_del)
            ]
        return []

    @staticmethod
    def obtener_coordenadas_visitante(formacion, w, h):
        """
        Espejo matemático: Nuevo X = AnchoTotal - X
        """
        coords_local = GestorFormaciones.obtener_coordenadas_local(formacion, w, h)
        coords_visitante = []
        for (x, y) in coords_local:
            coords_visitante.append((w - x, y))
        return coords_visitante