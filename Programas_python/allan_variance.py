import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import periodogram
from scipy.optimize import curve_fit
import pandas as pd
import allantools

# Ruta del archivo de datos
file_path = 'C:\\Users\\alanb\\OneDrive\\Documentos\\pythonProjets\\py_Projects\\mediciones\\frecuencias_analisis_estabilidad.txt'

df = pd.read_csv(file_path)

data = np.loadtxt(file_path)

data = allantools.Dataset(data)
data.compute("mdev")

data.write_results("output.dat")

# Crear un objeto Plot de allantools
b = allantools.Plot()

# Graficar los datos con barras de error y grilla
b.plot(data, errorbars=True, grid=True)

# Personalizar el eje x
b.ax.set_xlabel("Tau (s)")

# Obtener la figura actual
fig = plt.gcf()

# Personalizar el tamaño de la figura
fig.set_size_inches(10, 5)

# Personalizar el título del gráfico
plt.title('Varianza de Allan')

# Mostrar el gráfico
plt.show()