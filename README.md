# Figuras de Lissajous 
Este programa recrea las figuras de Lissajous por medio de gráficas y animaciones en 2D
## Descripción

  - Se definen las amplitudes de las ondas.
  - Se definen sus frecuencias y fases.
  - Se hace una superposición de las dos ondas.
  - Se grafica la  forma que deberia tener la superposición.
  - Se hace un archivo .gif para mostrar la animación de la superposición de las dos ondas.
## Requisitos
- Python 3.8+
- numpy
- matplotlib

## Instalación
```bash
git clone https://github.com/DanielVillarraga/Proyecto1_figuras_de_Lissajous.git
pip install -r requirements.txt
```
## Funcionamiento
`FiguraLissajous` (Clase abstracta):
- Define la estructura base con atributos encapsulados (_a, _b, _delta).
- Usa @property para validar valores (ej: frecuencias > 0).
- Método abstracto calculate_points() para obligar a su implementación en subclases.

`BasicLissajous ` (Subclase):
- Implementa la figura clásica con las ecuaciones estándar.

`AmplitudeModulatedLissajous` (Subclase)
- Añade modulación de amplitud para crear variantes dinámicas.
  
`LissajousVisualizer`:
- Maneja la visualización usando Matplotlib.
- Genera:
- Gráficos estáticos: Para análisis rápido.
- Animaciones: Muestra la evolución de la figura al variar δ.

## Autor 
Daniel Felipe Villarraga González
