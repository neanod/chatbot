import time
from jarvis import Bot
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard
import queue
from faster_whisper import WhisperModel
import os


MIN_LANGUAGE_PROBABILITY = 0.5

model_size = "large-v3"
fs = 44100       
channels = 2     
q = queue.Queue()
model = WhisperModel(model_size, device="cuda", compute_type="float16")


def callback(indata, frames, time, status):
	if status:
		print(status)
	q.put(indata.copy())


def transcribe_sound(min_propability: float = MIN_LANGUAGE_PROBABILITY):
	segments, info = model.transcribe("voice.wav", beam_size=5)

	if info.language_probability < min_propability:
		return "", info.language_probability
	print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

	res = ""
	print("usr>>>", end="")
	for segment in segments:
		# print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
		print(segment.text, end="", flush=True)
		res += segment.text
	print()
	return res, info.language_probability


def record_sound():
	recorded_frames = []
	with sd.InputStream(samplerate=fs, channels=channels, callback=callback):
		while keyboard.is_pressed('f13'):
			try:
				data = q.get(timeout=0.1)
				recorded_frames.append(data)
			except queue.Empty:
				pass
	write("voice.wav", fs, np.concatenate(recorded_frames, axis=0))


if __name__ == "__main__":
	bot = Bot()
	print("Initialized successfully")
	while True:
		try:
			time.sleep(0.1)
			if keyboard.is_pressed("ctrl+f13"):
				text = input("usr>>>")
			elif keyboard.is_pressed("f13"):
				record_sound()
				text, propability = transcribe_sound()
				if propability < MIN_LANGUAGE_PROBABILITY:
					continue
				os.remove("voice.wav")
			else:
				continue
			if not text.strip():
				continue
			bot.print_response(text)
		except KeyboardInterrupt:
			print("Quiting because of ^C")
			break
print("Ended up successfully")
