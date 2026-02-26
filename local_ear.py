import whisper
import sounddevice as sd
import numpy as np
import wave

# Load the smallest, fastest model
model = whisper.load_model("base")

def record_and_transcribe(duration=5):
    fs = 16000
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    
    # Save temp file
    import scipy.io.wavfile as wav
    wav.write("temp.wav", fs, audio)
    
    result = model.transcribe("temp.wav")
    return result["text"]
