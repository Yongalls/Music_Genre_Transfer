import librosa
import librosa.display
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def wav2spectro(filename):
    audio, sr = librosa.load(filename)
    D = np.abs(librosa.stft(audio))**2
    spectro = librosa.feature.melspectrogram(y=audio, sr=sr, S=D)
    return spectro, audio, sr

def spectro2wav(spectro, sr, filename):
    audio = librosa.feature.inverse.mel_to_audio(spectro)
    sf.write(filename, audio, sr)

if __name__ == '__main__':
    filename = './dataset/ballad_1.wav'
    spectro, audio, sr = wav2spectro(filename)
    # y_trimmed, _ = librosa.effects.trim(audio)
    # librosa.display.waveplot(y_trimmed, sr=sr)
    # plt.show()
    spectro2wav(spectro, sr, './dataset/ballad_1_converted.wav')
