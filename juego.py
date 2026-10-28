"""Misión meteorito: ejecuta python juego.py con Python 3 y Tkinter."""
import random
import time
import tkinter as tk

ANCHO, ALTO = 600, 700


class Juego:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title('Misión meteorito')
        ventana.resizable(False, False)
        self.canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO,
                                bg='#080e24', highlightthickness=0)
        self.canvas.pack()
        self.teclas = set()
        self.record = 0
        ventana.bind('<KeyPress>', self.pulsar)
        ventana.bind('<KeyRelease>', lambda e: self.teclas.discard(e.keysym.lower()))
        ventana.bind('<FocusOut>', lambda e: self.teclas.clear())
        self.reiniciar()
        self.actualizar()

    def reiniciar(self):
        self.x = ANCHO / 2
        self.meteoritos = []
        self.estrellas = [[random.randrange(ANCHO), random.randrange(ALTO)]
                           for _ in range(65)]
        self.tiempo = self.puntos = 0
        self.espera = 0.7
        self.terminado = False
        self.teclas.clear()
        self.ultimo = time.monotonic()

    def pulsar(self, evento):
        tecla = evento.keysym.lower()
        self.teclas.add(tecla)
        if tecla == 'space' and self.terminado:
            self.reiniciar()
        elif tecla == 'escape':
            self.ventana.destroy()

    def avanzar(self, dt):
        if self.terminado:
            return
        self.tiempo += dt
        direccion = int(bool(self.teclas & {'right', 'd'})) - int(
            bool(self.teclas & {'left', 'a'}))
        self.x = max(22, min(ANCHO - 22, self.x + direccion * 380 * dt))
        for estrella in self.estrellas:
            estrella[1] = (estrella[1] + 65 * dt) % ALTO
        self.espera -= dt
        if self.espera <= 0:
            r = random.randint(15, 32)
            self.meteoritos.append([random.randint(r, ANCHO-r), -r, r,
                                    random.uniform(170, 260) + self.tiempo * 4])
            self.espera = max(0.18, 0.75 - self.tiempo * 0.009)
        restantes = []
        for meteorito in self.meteoritos:
            meteorito[1] += meteorito[3] * dt
            x, y, r, _ = meteorito
            if (x-self.x)**2 + (y-(ALTO-70))**2 < (r+13)**2:
                self.terminado = True
            if y-r > ALTO:
                self.puntos += 10
            else:
                restantes.append(meteorito)
        self.meteoritos = restantes
        self.record = max(self.record, self.puntos)

    def dibujar(self):
        c = self.canvas
        c.delete('all')
        for x, y in self.estrellas:
            c.create_oval(x, y, x+2, y+2, fill='#a6bbdf', outline='')
        for x, y, r, _ in self.meteoritos:
            c.create_oval(x-r, y-r, x+r, y+r, fill='#b36d48',
                          outline='#edab72', width=2)
            c.create_oval(x-r/2, y-r/2, x, y, fill='#794b3b', outline='')
            c.create_oval(x+r/5, y+r/5, x+r/2, y+r/2,
                          fill='#794b3b', outline='')
        x, y = self.x, ALTO-70
        c.create_polygon(x-9, y+14, x, y+random.randint(20, 33), x+9, y+14,
                         fill='#ffb347', outline='')
        c.create_polygon(x, y-25, x-20, y+18, x, y+10, x+20, y+18,
                         fill='#48d8ee', outline='#b2f5ff', width=2)
        c.create_oval(x-5, y-8, x+5, y+3, fill='#172953', outline='')
        c.create_text(20, 25, anchor='w', text=f'PUNTOS  {self.puntos}',
                      fill='white', font=('Arial', 17, 'bold'))
        c.create_text(ANCHO-20, 25, anchor='e', text=f'RÉCORD  {self.record}',
                      fill='#ffd166', font=('Arial', 14, 'bold'))
        c.create_text(ANCHO/2, ALTO-20, text='← → o A / D: mover   •   Esc: salir',
                      fill='#b0bfdc', font=('Arial', 12))
        if self.terminado:
            c.create_rectangle(50, 240, ANCHO-50, 440, fill='#14213d',
                               outline='#48d8ee', width=2)
            c.create_text(ANCHO/2, 285, text='¡MISIÓN TERMINADA!',
                          fill='#ff7777', font=('Arial', 24, 'bold'))
            c.create_text(ANCHO/2, 335, text=f'Conseguiste {self.puntos} puntos',
                          fill='white', font=('Arial', 18))
            c.create_text(ANCHO/2, 395, text='Pulsa ESPACIO para volver a jugar',
                          fill='#48d8ee', font=('Arial', 14))
        elif self.tiempo < 4:
            c.create_text(ANCHO/2, 150, text='¡ESQUIVA LOS METEORITOS!',
                          fill='#48d8ee', font=('Arial', 20, 'bold'))

    def actualizar(self):
        ahora = time.monotonic()
        dt = min(ahora-self.ultimo, 0.05)
        self.ultimo = ahora
        self.avanzar(dt)
        self.dibujar()
        self.ventana.after(16, self.actualizar)


def main():
    ventana = tk.Tk()
    Juego(ventana)
    ventana.mainloop()


if __name__ == '__main__':
    main()
