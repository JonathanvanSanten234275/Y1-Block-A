import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import argparse
import time

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

if torch.cuda.is_available():
    print("Cuda is available")
else:
    print("Cuda is not available")

print(torch.version.cuda)

def TTS(textin):
# This will download all the models used by Tortoise from the HF hub.
# If you want to use deepspeed the pass use_deepspeed=True nearly 2x faster than normal
    startTTS = time.perf_counter()
    tts = TextToSpeech(use_deepspeed=False, kv_cache=True)
    print(textin)
    text = textin
    preset = "fast"
    voice = "chatbot"
    voice_samples, conditioning_latents = load_voice(voice)
    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, 
                              preset=preset)
    torchaudio.save('generated.wav', gen.squeeze(0).cpu(), 24000)
    endTTS = time.perf_counter()
    return(endTTS - startTTS, 'succes')

def main():
    parser = argparse.ArgumentParser(description="TTSpart script")
    parser.add_argument('--textin', required=True, help='Input text for TTS')
    # Add other arguments as needed

    args = parser.parse_args()

    # Now you can access the 'textin' argument as args.textin
    textin = args.textin

    # Call your function with the textin argument or do whatever processing you need
    result = TTS(textin)
    return result
    

if __name__ == '__main__':
    main()
