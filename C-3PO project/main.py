from Chatbot import launchUI
from voice import load_STT
from playsound import playsound as ps
import threading

def PlayAudio(file):
    ps(file)

if __name__ == "__main__":
    # Create a thread for loading STT
    stt_thread = threading.Thread(target=load_STT)
    stt_thread.start()

    # Create a thread for launching the UI
    ui_thread = threading.Thread(target=launchUI)
    ui_thread.start()