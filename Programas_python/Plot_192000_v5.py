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

Frames = 1024 * 32
Format = pa.paInt16
Channels = 1
Fs = 192000
Vmax_PA = 10

p = pa.PyAudio()

stream = p.open(format=Format,
                channels=Channels,
                rate=Fs,
                input=True,
                output=True,
                frames_per_buffer=Frames)

fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 6))

x_audio = np.arange(0, Frames, 1)
x_fft = np.linspace(0, Fs / 2, Frames // 2)

line, = ax1.plot(x_audio, np.random.rand(Frames), 'r')
line_fft, = ax2.plot(x_fft, np.random.rand(Frames // 2), 'b')
line_fund, = ax2.plot([0, 0], [-120, 0], 'g--', label='f₀')

ax1.set_ylim(-1200, 1200)
ax1.set_xlim(0, Frames)

Fmin = 1
Fmax = 40000
text_freq = ax2.text(
    0.99 * Fmax, -30, '', fontsize=10, color='black',
    ha='right', va='top',
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)
ax2.set_xlim(Fmin, Fmax)
fig.suptitle('Entrada de datos en tiempo real', fontsize=12)
ax1.set_xlabel('Muestras por trama')
ax1.set_ylabel('Amplitud (mV)')
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Amplitud (dB)')
ax1.grid()
ax2.grid()
ax2.legend(loc='upper right')
fig.show()

F = (Fs / Frames) * np.arange(0, Frames // 2)
data_queue = queue.Queue()
buffer = collections.deque(maxlen=10)
running = True

def save_to_txt(frequency):
    with open('frecuencias.txt', 'a') as file:
        file.write(f"{frequency}\n")

def process_audio():
    while running:
        try:
            data = stream.read(Frames, exception_on_overflow=False)
            dataInt = np.array(struct.unpack(str(Frames) + 'h', data), dtype=np.int16)
            dataVolt = (dataInt / 32768.0) * Vmax_PA
            datamVolt = dataVolt * 1000
            M_gk = np.abs(fourier.fft(dataVolt)) / (Frames / 2)
            M_gk = M_gk[0:Frames // 2]
            M_gk_db = 20 * np.log10(M_gk + 1e-12)
            Posm = np.argmax(M_gk)
            F_fund = (Fs / Frames) * Posm
            buffer.append((datamVolt, M_gk_db, int(F_fund)))
        except IOError as e:
            if running:
                print("Error reading stream: ", e)
            continue

def update_plot():
    while running:
        try:
            if len(buffer) > 0:
                datamVolt, M_gk_db, F_fund = buffer.popleft()
                line.set_ydata(datamVolt)
                ax2.set_ylim(-120, 0)
                line_fft.set_ydata(M_gk_db)
                line_fund.set_xdata([F_fund, F_fund])
                text_freq.set_text(f"f₀ = {F_fund:.0f} Hz")
                save_to_txt(F_fund)
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

audio_thread = threading.Thread(target=process_audio)
audio_thread.start()

fig.canvas.mpl_connect('close_event', on_close)

update_plot()
