import matplotlib
import scipy.fftpack as fourier
import matplotlib.pyplot as plt
import numpy as np
import pyaudio as pa
import struct
import threading
import queue
import collections

matplotlib.use('TKAgg')

# Seteo parámetros para el procesamiento de audio
Frames = 1024 * 32  # Tamaño del paquete a procesar reducido
Format = pa.paInt16  # Formato de lectura Int 16 bits
Channels = 1
Fs = 192000  # Frecuencia de muestreo típica de audio

p = pa.PyAudio()

# Abrir Stream de audio para lectura y escritura
stream = p.open(format=Format,
                channels=Channels,
                rate=Fs,
                input=True,
                output=True,
                frames_per_buffer=Frames)

# Crear gráfico con 2 subgráficos
fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 6))

x_audio = np.arange(0, Frames, 1)
x_fft = np.linspace(0, Fs / 2, Frames // 2)  # Asegurar que el eje x esté correctamente mapeado

line, = ax1.plot(x_audio, np.random.rand(Frames), 'r')
line_fft, = ax2.plot(x_fft, np.random.rand(Frames // 2), 'b')  # Cambio a escala lineal para la FFT

ax1.set_ylim(-3000, 3000)
ax1.set_xlim(0, Frames)

Fmin = 1
Fmax = 40000
ax2.set_xlim(Fmin, Fmax)
fig.suptitle('Entrada de datos en tiempo real', fontsize=12)
ax1.set_xlabel('Muestras por trama')
ax1.set_ylabel('Amplitud (V)')
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Amplitud (dB)')
ax1.grid()
ax2.grid()
fig.show()

# Crear vector de frecuencia para encontrar frecuencia dominante
F = (Fs / Frames) * np.arange(0, Frames // 2)

# Crear una cola para comunicar entre hilos
data_queue = queue.Queue()

# Buffer circular
buffer = collections.deque(maxlen=10)

# Variable para controlar el estado de los hilos
running = True

def save_to_txt(frequency):
    with open('frecuencias.txt', 'a') as file:
        file.write(f"{frequency}\n")

def process_audio():
    while running:
        try:
            # Leer paquetes de longitud Frames
            data = stream.read(Frames, exception_on_overflow=False)
            # Convertir datos del paquete en bytes
            dataInt = struct.unpack(str(Frames) + 'h', data)
            # Calcular FFT y magnitud de FFT para paquete
            M_gk = abs(fourier.fft(dataInt) / Frames)
            # Tomar la mitad del espectro
            M_gk = M_gk[0:Frames // 2]
            Posm = np.argmax(M_gk)  # Encuentra el índice del máximo en M_gk
            # Encontrar frecuencia correspondiente a magnitud máxima
            F_fund = (Fs / Frames) * Posm  # Convertir índice a frecuencia (Hz)

            # Añadir datos al buffer circular y a la cola de datos
            buffer.append((dataInt, M_gk, int(F_fund)))
        except IOError as e:
            if running:
                print("Error reading stream: ", e)
            continue

def update_plot():
    while running:
        try:
            # Leer datos del buffer circular
            if len(buffer) > 0:
                dataInt, M_gk, F_fund = buffer.popleft()
                line.set_ydata(dataInt)
                ax2.set_ylim(0, np.max(M_gk + 10))  # Ajustar el eje Y según el pico
                line_fft.set_ydata(M_gk)
                print(F_fund)  # Imprimir la frecuencia en Hz
                save_to_txt(F_fund)  # Guardar en el archivo
                fig.canvas.draw()
                fig.canvas.flush_events()
        except queue.Empty:
            pass
        fig.canvas.flush_events()

def on_close(event):
    global running
    running = False
    audio_thread.join()
    plt.close()

# Crear y comenzar el hilo para procesar el audio
audio_thread = threading.Thread(target=process_audio)
audio_thread.start()

# Conectar el manejador de cierre de ventana
fig.canvas.mpl_connect('close_event', on_close)

# Actualizar la gráfica en el hilo principal
update_plot()
