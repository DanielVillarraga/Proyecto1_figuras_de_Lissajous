import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from abc import ABC, abstractmethod
import time
import math
from functools import wraps

class FiguraLissajous(ABC):
    """Clase abstracta base para figuras de Lissajous."""
    
    def __init__(self, a=1, b=1, delta=0):
        self._a = a  # Frecuencia en x (privada)
        self._b = b  # Frecuencia en y (privada)
        self._delta = delta  # Diferencia de fase (privada)
        self._t = np.linspace(0, 2*np.pi, 1000)  # Parámetro t
        
    @property
    def a(self):
        return self._a
        
    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("La frecuencia debe ser positiva")
        self._a = value
    @property
    def b(self):
        return self._b
        
    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("La frecuencia debe ser positiva")
        self._b = value
        
    @property
    def delta(self):
        return self._delta
        
    @delta.setter
    def delta(self, value):
        self._delta = value % (2*np.pi)
        
    @abstractmethod
    def calculate_points(self):
        """Método abstracto para calcular puntos de la figura."""
        pass
    def timing_decorator(func):
        """Decorador para medir tiempo de ejecución."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} ejecutado en {end-start:.4f} segundos")
            return result
        return wrapper

class BasicLissajous(FiguraLissajous):
    """Implementación básica de figuras de Lissajous."""
    
    @FiguraLissajous.timing_decorator
    def calculate_points(self):
        """Calcula los puntos x e y para la figura."""
        x = np.sin(self._a * self._t + self._delta)
        y = np.sin(self._b * self._t)
        return x, y
    
class AmplitudeModulatedLissajous(FiguraLissajous):
    """Lissajous con amplitud modulada en el tiempo."""
    
    def __init__(self, a=1, b=1, delta=0, modulation=0.5):
        super().__init__(a, b, delta)
        self._modulation = modulation
        
    @property
    def modulation(self):
        return self._modulation
        
    @modulation.setter
    def modulation(self, value):
        if not 0 <= value <= 1:
            raise ValueError("La modulación debe estar entre 0 y 1")
        self._modulation = value
        
    @FiguraLissajous.timing_decorator
    def calculate_points(self):
        """Calcula puntos con amplitud modulada."""
        envelope = 1 - self._modulation * np.sin(self._t/2)
        x = envelope * np.sin(self._a * self._t + self._delta)
        y = envelope * np.sin(self._b * self._t)
        return x, y
    
class LissajousVisualizer:
    """Clase para visualizar y animar figuras de Lissajous."""
    
    def __init__(self, figure):
        self.figure = figure
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], lw=2)
        self.title = self.ax.set_title('')
        
    def update_plot(self, delta):
        """Actualiza la figura con nuevo delta."""
        self.figure.delta = delta
        x, y = self.figure.calculate_points()
        self.line.set_data(x, y)
        ratio = self.figure.a / self.figure.b
        self.title.set_text(f'Lissajous {self.figure.a}:{self.figure.b}\nFase: {delta:.2f} rad')
        return self.line, self.title
        
    def animate(self, frames=100):
        """Crea animación de la figura."""
        ani = FuncAnimation(
            self.fig, 
            lambda i: self.update_plot(i*2*np.pi/frames),
            frames=frames,
            interval=50,
            blit=True
        )
        plt.close()
        return ani
        
    def show_static(self, delta=0):
        """Muestra una figura estática."""
        self.update_plot(delta)
        plt.show()

if __name__ == "__main__":
    # Crear figuras
    basic = BasicLissajous(a=3, b=2)
    modulated = AmplitudeModulatedLissajous(a=4, b=3, modulation=0.7)
    
    # Visualización estática
    print("\nVisualización estática de BasicLissajous:")
    vis_basic = LissajousVisualizer(basic)
    vis_basic.show_static(np.pi/4)
    
    print("\nVisualización estática de AmplitudeModulatedLissajous:")
    vis_mod = LissajousVisualizer(modulated)
    vis_mod.show_static(np.pi/2)
    
    # Generar animaciones
    print("\nGenerando animaciones...")
    ani_basic = vis_basic.animate()
    ani_mod = vis_mod.animate()
    
    # Guardar animaciones (requiere ffmpeg o pillow)
    try:
        ani_basic.save('basic_lissajous.gif', writer='pillow', fps=20)
        ani_mod.save('modulated_lissajous.gif', writer='pillow', fps=20)
        print("Animaciones guardadas como GIF")
    except:
        print("No se pudo guardar las animaciones. Faltan dependencias.")
    
    # Demostración de encapsulación y propiedades
    print("\nProbando encapsulación:")
    try:
        basic.a = -1  # Debe fallar
    except ValueError as e:
        print(f"Error correcto: {e}")
    
    # Cambio válido
    basic.a = 3
    basic.b = 4
    print(f"Nueva relación de frecuencias: {basic.a}:{basic.b}")