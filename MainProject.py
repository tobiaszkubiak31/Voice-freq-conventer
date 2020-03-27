from __future__ import print_function
import wave
from gettext import install
import IPython.display
import librosa.display
import matplotlib
import numpy
import numpy as np
import pylab
from matplotlib.cm import get_cmap
from matplotlib.pyplot import show, plot, title, figure, xlabel, ylabel, specgram, colorbar, stem
from matplotlib.pyplot import subplot, tight_layout
from scipy.fftpack import fft
from scipy.io.wavfile import read as read_wav
from scipy.io.wavfile import write
install(numpy)
install(matplotlib)
install(librosa)


if __name__ == "__main__":
    sampling_rate, data = read_wav("man_voice.wav")

    fft_out = fft(data)

    fnames = ["man_voice.wav", "szum.wav"]
    wavs = [wave.open(fn) for fn in fnames]
    frames = [w.readframes(w.getnframes()) for w in wavs]
    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
    n = min(map(len, samples))
    mix = samples[0][:n] + samples[1][:n]
    mix_wav = wave.open("./mix.wav", 'w')
    mix_wav.setparams(wavs[0].getparams())
    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()

    y, sr = librosa.load("man_voice.wav")
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=24, bins_per_octave=24, res_type='fft')
    write("example.wav", sr, y_shifted)

    y, sr = librosa.load("example.wav")  # y is a numpy array of the wav file, sr = sample rate
    y_shifted2 = librosa.effects.pitch_shift(y, sr, n_steps=-20, bins_per_octave=24)
    write("man_voice_again.wav", sr, y_shifted2)

    y, sr = librosa.load("child_voice.wav")
    y_shifted3 = librosa.effects.pitch_shift(y, sr, n_steps=-15, bins_per_octave=24)
    write("from_zero_to_hero.wav", sr, y_shifted3)


    fnames = ["child_voice.wav", "szum.wav"]
    wavs = [wave.open(fn) for fn in fnames]
    frames = [w.readframes(w.getnframes()) for w in wavs]
    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
    n = min(map(len, samples))
    mix = samples[0][:n] + samples[1][:n]
    mix_wav = wave.open("./mix1.wav", 'w')
    mix_wav.setparams(wavs[0].getparams())
    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()
