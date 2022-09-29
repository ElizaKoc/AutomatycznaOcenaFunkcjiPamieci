from scipy.io import wavfile
import noisereduce as nr
from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def preprocess(path_in):
    path_out = 'resources/preprocessed/' + path_in.split('\\')[-1]
    rate, data = wavfile.read(path_in)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(path_out, rate, reduced_noise)
    sound = AudioSegment.from_file(path_out)
    normalized_sound = match_target_amplitude(sound, -20.0)
    normalized_sound.export(path_out, format="wav")
    return path_out
