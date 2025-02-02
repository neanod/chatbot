import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard
import queue

fs = 44100        # частота дискретизации
channels = 2      # количество каналов
q = queue.Queue() # очередь для передачи аудио-данных из callback

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())

print("Нажмите и удерживайте F13 для записи. Отпустите F13, чтобы остановить запись.")

# Ожидаем, когда пользователь нажмёт F13
while not keyboard.is_pressed('f13'):
    pass

recorded_frames = []

# Запускаем поток записи
with sd.InputStream(samplerate=fs, channels=channels, callback=callback):
    while keyboard.is_pressed('f13'):
        try:
            data = q.get(timeout=0.1)  # получаем данные из очереди
            recorded_frames.append(data)
        except queue.Empty:
            # если данных в очереди нет, продолжаем цикл
            pass

# Объединяем записанные части в один массив
recording = np.concatenate(recorded_frames, axis=0)

# Сохраняем запись в файл
write("temp.wav", fs, recording)
print("Запись завершена и сохранена в файл temp.wav")
