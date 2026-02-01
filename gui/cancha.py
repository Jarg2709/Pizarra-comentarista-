import tkinter as tk


class Cancha:
    def __init__(self, parent, width=500, height=300):
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="#2e7d32",   # verde cancha
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.width = width
        self.height = height

        self.dibujar_cancha()

    def dibujar_cancha(self):
        w, h = self.width, self.height

        # Bordes
        self.canvas.create_rectangle(10, 10, w-10, h-10, outline="white", width=2)

        # Línea central
        self.canvas.create_line(w/2, 10, w/2, h-10, fill="white", width=2)

        # Círculo central
        self.canvas.create_oval(
            w/2-40, h/2-40,
            w/2+40, h/2+40,
            outline="white", width=2
        )

        # Áreas
        self.canvas.create_rectangle(10, h/2-60, 80, h/2+60, outline="white", width=2)
        self.canvas.create_rectangle(w-80, h/2-60, w-10, h/2+60, outline="white", width=2)

    def dibujar_jugador(self, jugador, color="blue"):
        r = 12
        x, y = jugador.x, jugador.y

        self.canvas.create_oval(
            x-r, y-r,
            x+r, y+r,
            fill=color, outline="white"
        )

        self.canvas.create_text(
            x, y,
            text=str(jugador.numero),
            fill="white",
            font=("Segoe UI", 9, "bold")
        )
