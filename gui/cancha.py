import tkinter as tk


class Cancha:
    ASPECT_RATIO = 105 / 68  # proporción real FIFA

    def __init__(self, parent, on_resize=None):
        self.parent = parent
        self.on_resize = on_resize

        self.canvas = tk.Canvas(
            parent,
            bg="#2e7d32",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.width = 1
        self.height = 1
        self.x0 = 0
        self.y0 = 0

        self.canvas.bind("<Configure>", self._redimensionar)

    # =========================
    # REDIMENSIONAMIENTO
    # =========================
    def _redimensionar(self, event):
        w, h = event.width, event.height

        if w / h > self.ASPECT_RATIO:
            self.height = h
            self.width = int(h * self.ASPECT_RATIO)
        else:
            self.width = w
            self.height = int(w / self.ASPECT_RATIO)

        self.x0 = (w - self.width) / 2
        self.y0 = (h - self.height) / 2

        self.dibujar_cancha()

        if self.on_resize:
            self.on_resize()

    # =========================
    # DIBUJO CANCHA
    # =========================
    def dibujar_cancha(self):
        self.canvas.delete("cancha")

        m = self.width * 0.04
        x0, y0, w, h = self.x0, self.y0, self.width, self.height

        self.canvas.create_rectangle(
            x0 + m, y0 + m,
            x0 + w - m, y0 + h - m,
            outline="white", width=2, tags="cancha"
        )

        self.canvas.create_line(
            x0 + w / 2, y0 + m,
            x0 + w / 2, y0 + h - m,
            fill="white", width=2, tags="cancha"
        )

        r = h * 0.15
        self.canvas.create_oval(
            x0 + w / 2 - r, y0 + h / 2 - r,
            x0 + w / 2 + r, y0 + h / 2 + r,
            outline="white", width=2, tags="cancha"
        )

    # =========================
    # COORDENADAS
    # =========================
    def normalizar(self, nx, ny):
        x = self.x0 + nx * self.width
        y = self.y0 + ny * self.height
        return x, y

    # =========================
    # JUGADORES
    # =========================
    def dibujar_jugador(self, jugador, color):
        x, y = self.normalizar(jugador.nx, jugador.ny)
        r = 12

        c = self.canvas.create_oval(
            x - r, y - r,
            x + r, y + r,
            fill=color, outline="white"
        )
        t = self.canvas.create_text(
            x, y,
            text=jugador.numero,
            fill="white",
            font=("Segoe UI", 9, "bold")
        )

        jugador._grafico = (c, t)

    def mover_jugador(self, jugador):
        c, t = jugador._grafico
        x, y = self.normalizar(jugador.nx, jugador.ny)

        x0, y0, x1, y1 = self.canvas.coords(c)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2

        dx = x - cx
        dy = y - cy

        self.canvas.move(c, dx, dy)
        self.canvas.move(t, dx, dy)
