from vosk import Model, KaldiRecognizer
from functools import lru_cache
import pyaudio

def STT():
    for i in range(0, int(16000/8192 *6)):
        stream().start_stream()
        print('go')
        data = stream().read(8192)
        recognizer().AcceptWaveform(data)

    text = recognizer().Result()
    stream().stop_stream()
    print(text[14:-3])
    return(text[14:-3])
        
def load_STT():
    model()
    recognizer()
    mic()
    stream()
    return()

@lru_cache
def model():
    model = Model(r"E:\3PO assets\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
    return(model)

@lru_cache
def recognizer():
    recognizer = KaldiRecognizer(model(), 16000)
    return(recognizer)

@lru_cache
def mic():
    mic = pyaudio.PyAudio()
    return(mic)

@lru_cache
def stream():
    stream = mic().open(rate=16000, channels = 1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
    return(stream)