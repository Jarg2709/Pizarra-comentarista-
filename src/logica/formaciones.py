class GestorFormaciones:
    @staticmethod
    def obtener_coordenadas_local(formacion, w, h):
        """
        Calcula posiciones relativas al ancho (w) y alto (h).
        Ahora devuelve (X, Y, Posición).
        El equipo local ataca de Izquierda a Derecha.
        """
        cy = h / 2          
        x_arq = w * 0.05    
        x_def = w * 0.15    
        x_med = w * 0.30    
        x_del = w * 0.42    

        dy_def = h * 0.18   
        dy_med = h * 0.18
        dy_del = h * 0.20

        # Recuerda: Menor Y (cy - algo) = Arriba en la pantalla (Lado Izquierdo del jugador)
        # Mayor Y (cy + algo) = Abajo en la pantalla (Lado Derecho del jugador)
        if formacion == "4-4-2":
            return [
                (x_arq, cy, "POR"),
                (x_def, cy - 1.5*dy_def, "LI"), (x_def, cy - 0.5*dy_def, "DFC"), (x_def, cy + 0.5*dy_def, "DFC"), (x_def, cy + 1.5*dy_def, "LD"),
                (x_med, cy - 1.5*dy_med, "MI"), (x_med, cy - 0.5*dy_med, "MC"), (x_med, cy + 0.5*dy_med, "MC"), (x_med, cy + 1.5*dy_med, "MD"),
                (x_del, cy - 0.5*dy_del, "DC"), (x_del, cy + 0.5*dy_del, "DC")
            ]
        elif formacion == "4-3-3":
            return [
                (x_arq, cy, "POR"),
                (x_def, cy - 1.5*dy_def, "LI"), (x_def, cy - 0.5*dy_def, "DFC"), (x_def, cy + 0.5*dy_def, "DFC"), (x_def, cy + 1.5*dy_def, "LD"),
                (x_med - (w*0.02), cy, "MCD"), (x_med + (w*0.02), cy - dy_med, "MC"), (x_med + (w*0.02), cy + dy_med, "MC"), 
                (x_del, cy, "DC"), (x_del, cy - 1.2*dy_del, "EI"), (x_del, cy + 1.2*dy_del, "ED")
            ]
        elif formacion == "4-2-3-1":
            return [
                (x_arq, cy, "POR"),
                (x_def, cy - 1.5*dy_def, "LI"), (x_def, cy - 0.5*dy_def, "DFC"), (x_def, cy + 0.5*dy_def, "DFC"), (x_def, cy + 1.5*dy_def, "LD"),
                (x_med - (w*0.05), cy - 0.5*dy_med, "MCD"), (x_med - (w*0.05), cy + 0.5*dy_med, "MCD"), 
                (x_med + (w*0.05), cy, "MCO"), (x_med + (w*0.05), cy - 1.2*dy_med, "MI"), (x_med + (w*0.05), cy + 1.2*dy_med, "MD"), 
                (x_del + (w*0.02), cy, "DC")
            ]
        elif formacion == "3-5-2":
            return [
                (x_arq, cy, "POR"),
                (x_def, cy, "DFC"), (x_def, cy - dy_def, "DFC"), (x_def, cy + dy_def, "DFC"), 
                (x_med, cy, "MCD"), (x_med, cy - dy_med, "MC"), (x_med, cy + dy_med, "MC"), (x_med + (w*0.05), cy - 2*dy_med, "MI"), (x_med + (w*0.05), cy + 2*dy_med, "MD"), 
                (x_del, cy - 0.5*dy_del, "DC"), (x_del, cy + 0.5*dy_del, "DC")
            ]
        return []

    @staticmethod
    def obtener_coordenadas_visitante(formacion, w, h):
        """
        Rotación de 180 grados: Invertimos X e Y.
        Esto garantiza que un Lateral Izquierdo (LI) siga estando a la izquierda
        anatómica del equipo visitante que ahora ataca hacia la izquierda.
        """
        coords_local = GestorFormaciones.obtener_coordenadas_local(formacion, w, h)
        coords_visitante = []
        for info in coords_local:
            x, y, pos = info
            # Invertir X y Y respeta la geometría del campo
            coords_visitante.append((w - x, h - y, pos))
        return coords_visitante