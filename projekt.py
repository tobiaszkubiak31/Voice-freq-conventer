

import wave
import numpy as np
# load two files you'd like to mix
fnames =["man_voice.wav", "szum.wav"]
wavs = [wave.open(fn) for fn in fnames]
frames = [w.readframes(w.getnframes()) for w in wavs]
# here's efficient numpy conversion of the raw byte buffers
# '<i2' is a little-endian two-byte integer.
samples = [np.frombuffer(f, dtype='<i2') for f in frames]
samples = [samp.astype(np.float64) for samp in samples]
# mix as much as possible
n = min(map(len, samples))
mix = samples[0][:n] + samples[1][:n]
# Save the result
mix_wav = wave.open("./mix.wav", 'w')
mix_wav.setparams(wavs[0].getparams())
# before saving, we want to convert back to '<i2' bytes:
mix_wav.writeframes(mix.astype('<i2').tobytes())
mix_wav.close()
