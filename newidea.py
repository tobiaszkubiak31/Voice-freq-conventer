import os
import sys
import winsound

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout
from PyQt5.QtGui import QIcon
from playsound import playsound
# from Tkinter import Tk
from tkinter.filedialog import askopenfilename, Tk
import PyQt5
import simpleaudio
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



class VoiceConventer(QDialog):

    def __init__(self):
        super().__init__()

        #initializtion the window properties
        self.title = 'Voice conventer'
        self.left = 700
        self.top = 400
        self.width = 320
        self.height = 200
        self.move(50,100)
        #path to voice sound set to default
        self.pathToFile = "man_voice.wav"


        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createHorizontalLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createHorizontalLayout(self):

        self.horizontalGroupBox = QGroupBox("Converting")
        layout = QHBoxLayout()
        buttonAdd = QPushButton('Select sound', self)
        buttonAdd.clicked.connect(self.openSound)
        layout.addWidget(buttonAdd)

        buttonPlay = QPushButton('Play sound', self)
        buttonPlay.clicked.connect(self.playSound)
        layout.addWidget(buttonPlay)

        buttonChild = QPushButton('Convert to Child Voice', self)
        buttonChild.clicked.connect(self.convertChild)
        layout.addWidget(buttonChild)

        buttonMan = QPushButton('Convert to Man Voice', self)
        buttonMan.clicked.connect(self.convertMan)
        layout.addWidget(buttonMan)

        buttonNoise = QPushButton('Add Noise', self)
        buttonNoise.clicked.connect(self.addNoise)
        layout.addWidget(buttonNoise)

        buttonDeleteNoise = QPushButton('Delete Noise', self)
        buttonDeleteNoise.clicked.connect(self.deleteNoise)
        layout.addWidget(buttonDeleteNoise)

        self.horizontalGroupBox.setLayout(layout)

    def openSound(self):
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.pathToFile = filename
    def playSound(self):
        try:
            playsound(self.pathToFile)
        except:
            print("Sound file doesnt exists, check your sound file path")

    def convertChild(self):
        y, sr = librosa.load("man_voice.wav")
        self.y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=24, bins_per_octave=24, res_type='fft')
        write("child.wav", sr, self.y_shifted)

        winsound.PlaySound("child.wav", winsound.SND_FILENAME)

    def convertMan(self):
        y, sr = librosa.load("child.wav")
        self.y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=-24, bins_per_octave=24, res_type='fft')
        write("man_voice_reversed.wav", sr, self.y_shifted)

        winsound.PlaySound("man_voice_reversed.wav", winsound.SND_FILENAME)
    def addNoise(self):
        fnames = ["man_voice.wav", "szum.wav"]
        wavs = [wave.open(fn) for fn in fnames]
        frames = [w.readframes(w.getnframes()) for w in wavs]
        self.samples = [np.frombuffer(f, dtype='<i2') for f in frames]
        self.samples = [samp.astype(np.float64) for samp in self.samples]
        print(self.samples[1])
        self.delete = self.samples[1]
        n = min(map(len, self.samples))
        mix = self.samples[0][:n] + self.samples[1][:n]
        mix_wav = wave.open("withnoise.wav", 'w')
        mix_wav.setparams(wavs[0].getparams())
        mix_wav.writeframes(mix.astype('<i2').tobytes())
        mix_wav.close()
        winsound.PlaySound("withnoise.wav", winsound.SND_FILENAME)
    def deleteNoise(self):
        fnames = ["withnoise.wav", "szum.wav"]
        wavs = [wave.open(fn) for fn in fnames]
        frames = [w.readframes(w.getnframes()) for w in wavs]
        self.samples = [np.frombuffer(f, dtype='<i2') for f in frames]
        self.samples = [samp.astype(np.float64) for samp in self.samples]
        print(self.samples[1])
        self.delete = self.samples[1]
        n = min(map(len, self.samples))
        mix = self.samples[0][:n] - self.samples[1][:n]
        mix_wav = wave.open("withoutnoise.wav", 'w')
        mix_wav.setparams(wavs[0].getparams())
        mix_wav.writeframes(mix.astype('<i2').tobytes())
        mix_wav.close()
        winsound.PlaySound("withoutnoise.wav", winsound.SND_FILENAME)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceConventer()
    sys.exit(app.exec_())



#pole bitewne dodawanie szumu
 # y, sr = librosa.load("man_voice.wav")
 #        #losowanie
 #        sampl = np.random.uniform(low=0.0, high=0.10, size=(len(y)))
 #        a = np.float32(sampl)
 #        data = np.float32(y)
 #
 #        j = min(len(a), len(data))
 #        z = [a[i] + data[i] for i in range(j)]
 #        write("example.wav", sr, z)
 #        playsound('example.wav')





