# -*- coding: utf-8 -*-

# Dependencies
from array import array
import pyaudio
from time import sleep
from sys import byteorder
from struct import pack
from scipy.signal import butter, lfilter
import wave
import numpy as np
from pydub import AudioSegment
from scipy.signal import resample
from os import listdir

# GLOBAL VARIABLES
VOLUME_THRESHOLD = 1000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
Fs = 16000
SILENCE_THRESHOLD = 50

def is_silent(snd_data):
    """
    This function simply check for silence by comparing the volume of the signal with a set
    threshold defined above. Noisy backgrounds may need a higher threshold.

    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    return max(snd_data) < VOLUME_THRESHOLD

# This function 
def normalize(snd_data):
    """
    Normalize the volume to a target range defined by the MAXIMUM variable
    
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    arr = array('h')
    for i in snd_data:
        arr.append(int(i*times))
    return arr

def trim(snd_data):
    """
    Trim the silence at the start and the end of the recording
    
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    # This nested function allows for a simple way to run this function twice for
    # the beginning and the end.
    def _trim(snd_data):
        snd_started = False
        arr = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > VOLUME_THRESHOLD:
                snd_started = True
                arr.append(i)

            elif snd_started:
                arr.append(i)
        return arr

    # Trim the beginning
    snd_data = _trim(snd_data)

    # Trim the end
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    
    return snd_data

def recordToFile(fname):
    """
    This function is where the mic is turned on and sound is recorded
    
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    mic = pyaudio.PyAudio()
    stream = mic.open(format = FORMAT, channels = 1, rate = Fs,
        input = True, output = True,
        frames_per_buffer = CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    data = array('h')
    
    print("Start speaking in...")
    for i in range(1,5):
        if i == 4:
            sleep(1)
            print("Go")
        else:
            sleep(1)
            print(str(4 - i))
           

    
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        data.extend(snd_data)

        # Check if you have started speaking
        silent = is_silent(snd_data)
        if not silent:
            num_silent = 0
            
        # If you started, this block tallies a count of "silent" chunks and terminates 
        # the loop when a specified count has been reached
        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > SILENCE_THRESHOLD:
            break

#    sample_width = mic.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    mic.terminate()

    data = normalize(data)
    data = trim(data)
    
    # Write the wav file
    signalToWav(data, fname)

#def loadAudio(fname):
#    """
#    ashdsjdfhs
#
#    # Arguments
#        classifier: A classifier object loaded with `keras.models.load_model`
#        or generated with `buildClassifier`
#        fname: Name of the audio file to analyze
#
#    # Returns
#        None
#
#    # Raises
#        Not handled yet
#    """
#    spf = wave.open(fname,'r')
#    signal = spf.readframes(-1)
#    signal = np.frombuffer(signal, np.int16)
#    spf.close()
#    return signal
    
def splitAudio(signal, sample_length):
    """
    Split the audio signal into several smaller samples

    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
        # Split signal into a matrix of short clips in each row
    clip = np.concatenate([signal, np.zeros(int(Fs*(np.ceil(signal.size/Fs) + np.floor(sample_length - (signal.size/Fs) % sample_length)) - signal.size), np.int16)]) #Zero pad up to multiple os our sample window
    clip_length = clip.size/Fs
    samples = np.zeros((int(clip_length/sample_length), int(sample_length*Fs)), dtype = np.int16)
    
    for i in range(int(clip_length/sample_length)):
        samples[i] = clip[int(sample_length*Fs*i):int(sample_length*Fs*(i + 1))]
    return samples

def butterLowpassFilter(data, cutoff, fs, order = 6):
    """
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y.astype(np.int16)

def downSample(data, cutoff, Fs, step):
    """
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    butterLowpassFilter(data, cutoff, Fs, 40)
    data = data[0::step]
    return data
 
def getData(fname):
    """
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
     #Extract Raw Audio from Wav File
    sound_file = wave.open(fname, 'r')
    data = sound_file.readframes(-1)
    data = np.frombuffer(data, np.int16)
    sound_file.close()
    return data

def convertToWav(filename):
    """
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    i = 0
    for filename in listdir("C://Users/Austin/Desktop/mehant/"):
        filename = "C://Users/Austin/Desktop/mehant/" + filename
        extension = filename[filename.find(".")+1:]
        if extension != "wav":
            audio = AudioSegment.from_file(file = filename, format = extension)
            audio.set_channels(1)
            audio.export(filename[0:len(filename)-4] + "wavfile" + str(i) + '.wav', format="wav")
            i += 1

def convertToMono(fname, new_fname, Fs):
    audio = getData(fname)
    audio = audio[0::2]
    signalToWav(audio, new_fname, Fs)
    
def convertToFLAC(fname, new_fname):
    extension = fname[fname.find(".")+1:]
    if extension != "flac":
        audio = AudioSegment.from_file(file = fname, format = extension)
        audio.set_channels(1)
        audio.export(new_fname, format="flac")
        
def signalToWav(signal, fname, Fs):
    data = pack('<' + ('h'*len(signal)), *signal)
    wav_file = wave.open(fname, 'wb')
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(Fs)
    wav_file.writeframes(data)
    wav_file.close()
    
def addNoise(x, SNR = 10):
#    recordToFile("demo.wav")
    SNR = 30
    x = getData("demo.wav")
    S = 10*np.log10(np.var(x))
    N = S - SNR
    noise = np.random.normal(0, np.sqrt(np.power(10, N/10)), len(x))
    noise = noise.astype(np.int16)
    x = np.sum([x, noise], axis = 0, dtype = np.int16)
    signalToWav(x, "demo_noise.wav", 16e3)
    return x
    
def freqShift(fname, new_fname, shift, Fs):
    x = getData(fname)
    x = np.asarray(resample(x, int(len(x)*(1 + shift/100))), np.int16)
    signalToWav(x, new_fname, 16e3)
    
