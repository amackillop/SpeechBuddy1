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
from os import listdir, remove, makedirs
from os import path as ospath
from random import randint
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import pylab
from librosa import stft, feature, power_to_db
import librosa.display

# Importing required libraries for training
#from keras.models import Sequential
#from keras.layers import Conv2D
#from keras.layers import MaxPooling2D
#from keras.layers import Flatten
#from keras.layers import Dense
#from keras.layers import Dropout
#from keras.preprocessing.image import ImageDataGenerator
#from keras.models import load_model
#from keras.applications import mobilenet
#from keras.callbacks import EarlyStopping

from scipy.stats import bernoulli
from shutil import copyfile


BASE_DIR = ospath.dirname(ospath.dirname(ospath.abspath(__file__))) + "/"

"""
####################################################################################################################
AUDIO MANIPULATION SECTION

This collection of functions is used for manipulating audio signal data and files
####################################################################################################################
"""
# Need to add these into the functions
# GLOBAL VARIABLES
#VOLUME_THRESHOLD = 1000
#CHUNK_SIZE = 1024
#FORMAT = pyaudio.paInt16
#Fs = 16000
#SILENCE_THRESHOLD = 50

def is_silent(audio_data, threshold = 1000):
    """
    This function simply check for silence by comparing the volume of the signal with a set
    threshold defined above. Noisy backgrounds may need a higher threshold.

    # Arguments
        audio_data: 1-D array containing the audio signal
        threshold: Volume threshold for silence detection

    # Returns
        A boolean value. True if audio is deemed silent

    """
    return max(audio_data) < threshold

# This function 
def normalize(audio_data):
    """
    Normalize the volume to a target range defined by the MAXIMUM variable
    
    # Arguments
        audio_data: 1-D array containing the audio signal

    # Returns
        audio_data: 1-D array containing the volume normalized audio signal

    # Raises
        Not handled yet
    """
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in audio_data)

    arr = array('h')
    for i in audio_data:
        arr.append(int(i*times))
    return arr

def trim(audio_data, threshold = 1000):
    """
    Trim the silence at the beginning and the end of the signal.
    
    # Arguments
        audio_data: A 1-D int16 array containing the signal\n
        threshold: A volume threshold for silence detection

    # Returns
        None

    """
    # This nested function allows for a simple way to run this function twice for
    # the beginning and the end.
    def _trim(audio_data):
        snd_started = False
        arr = array('h')

        for i in audio_data:
            if not snd_started and abs(i) > threshold:
                snd_started = True
                arr.append(i)

            elif snd_started:
                arr.append(i)
        return arr

    # Trim the beginning
    audio_data = _trim(audio_data)

    # Trim the end
    audio_data.reverse()
    audio_data = _trim(audio_data)
    audio_data.reverse()
    
    return audio_data

def recordToFile(fname, Fs, FORMAT, SILENCE_THRESHOLD = 50, CHUNK_SIZE = 1024):
    """
    This function is where the mic is turned on and sound is recorded then saved to a file
    
    # Arguments
        fname: Name of the file where the recording will be saved
        Fs: Sampling rate of the recording

    # Returns
        None

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

    sample_width = mic.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    mic.terminate()
    print("Finished.")
    data = normalize(data)
    data = trim(data)
    
    # Write the wav file
    signalToWav(data, fname, Fs)
    
def splitAudio(signal, sample_length, Fs):
    """
    Split the audio signal into several smaller samples

    # Arguments
        signal: A 1-D array containing the audio signal
        sample_length: Desired length in seconds of the samples
        Fs: Sampling rate of the signal

    # Returns
        samples: A multi-dimensional array containing a sampled clip in each row

    """
    # Split signal into a matrix of short clips in each row
    clip = np.concatenate([signal, np.zeros(int(Fs*(np.ceil(signal.size/Fs) + np.floor(sample_length - (signal.size/Fs) % sample_length)) - signal.size), np.int16)]) #Zero pad up to multiple os our sample window
    clip_length = clip.size/Fs
    samples = np.zeros((int(clip_length/sample_length), int(sample_length*Fs)), dtype = np.int16)
    
    for i in range(int(clip_length/sample_length)):
        samples[i] = clip[int(sample_length*Fs*i):int(sample_length*Fs*(i + 1))]
    return samples


def downSample(signal, cutoff, Fs, step):
    """
    Downsample the signal by a specified integer amount.
    
    # Arguments
        signal: A 1-D array containing the signal \n
        cutoff: Cutoff frequency for the lowpass filter \n
        Fs: Sampling rate of the original signal \n
        order: Order of the buttersworth lowpass filter used
        step: Integer specificying the downsample rate. a step of 2 means throwing away
        every other sample with halves the sampling rate.

    # Returns
        signal: A 1-D array containing the downsampled signal.

    # Raises
        None
    """
    def butterLowpassFilter(signal, cutoff, Fs, order = 10):
        """
        Implementing a buttersworth lowpass filter
        """
        nyq = 0.5 * Fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = lfilter(b, a, signal)
        return y.astype(np.int16)
    # Anti-aliasing filter
    butterLowpassFilter(signal, cutoff, Fs, 40)
    # Decimation
    signal = signal[0::step]
    return signal
 
def getData(fname):
    """
    Get the signal information from a wav file.
    
    # Arguments
        fname: WAV file. Name of the audio file to analyze

    # Returns
        data: A 1-D int16 numpy array containing the information
        Fs: The sampling rate of the file

    """
     #Extract Raw Audio from Wav File
    sound_file = wave.open(fname, 'r')
    Fs = sound_file.getframerate()
    data = sound_file.readframes(-1)
    data = np.frombuffer(data, np.int16)
    sound_file.close()
    return data, Fs

def convertToWav(fname, new_fname):
    """
    # Arguments
        fname: Name of the audio file to convert
        new_fname: Name of the converted audio file to be saved
        Fs: Sampling rate of the inital audio file

    # Returns
        None

    """
        
    extension = fname[fname.find(".")+1:]
    if extension != "wav":
        audio = AudioSegment.from_file(file = fname, format = extension)
        audio.set_channels(1)
        audio.export(new_fname, format="wav")

def convertToMono(fname, new_fname):
    """
    # Arguments
        fname: Name of the audio file to convert
        new_fname: Name of the converted audio file to be saved
        Fs: Sampling rate of the inital audio file

    # Returns
        None

    """
    audio, Fs = getData(fname)
    audio = audio[0::2]
    signalToWav(audio, new_fname, Fs)
    
def convertToFLAC(fname, new_fname):
    """
    # Arguments
        fname: Name of the audio file to convert
        new_fname: Name of the converted audio file to be saved

    # Returns
        None

    """
    extension = fname[fname.find(".")+1:]
    if extension != "flac":
        audio = AudioSegment.from_file(file = fname, format = extension)
        audio.set_channels(1)
        audio.export(new_fname, format="flac")
        
def signalToWav(signal, fname, Fs):
    """
    # Arguments
        signal: 1-D array containing the audio signal
        fname: Name of the audio file where the signal will be saved
        Fs: Sampling rate of the signal

    # Returns
        None

    """
    data = pack('<' + ('h'*len(signal)), *signal)
    wav_file = wave.open(fname, 'wb')
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(Fs)
    wav_file.writeframes(data)
    wav_file.close()

    """
    ###############################################################################################################
    DATASET GENERATION SECTION

    These functions are used to generate datasets to be used for training purposes. Not needed in web application
    ###############################################################################################################
    """
    
def addNoise(x, SNR = 10):
#    recordToFile("demo.wav")
    SNR = 30
    x, Fs = getData("demo.wav")
    S = 10*np.log10(np.var(x))
    N = S - SNR
    noise = np.random.normal(0, np.sqrt(np.power(10, N/10)), len(x))
    noise = noise.astype(np.int16)
    x = np.sum([x, noise], axis = 0, dtype = np.int16)
    signalToWav(x, "demo_noise.wav", 16e3)
    return x
    
def freqShift(fname, new_fname, shift):
    x, Fs = getData(fname)
    x = np.asarray(resample(x, int(len(x)*(1 + shift/100))), np.int16)
    signalToWav(x, new_fname, Fs)
    
def spliceRandWord(signal, words, clip_length, set_Fs = 8000):
    signal.flags.writeable = True
    files = listdir(words)
    rand_word = words + files[np.random.randint(0, len(files)-1)]
    audio = AudioSegment.from_file(rand_word, format = "wav")
    matchTargetAmplitude(audio, -30)
    audio.export(rand_word, format = "wav")
    splice, Fs = getData(rand_word)
    if not Fs == set_Fs:
        step = Fs//set_Fs
        splice = downSample(splice, set_Fs//2, Fs, step)
    start = np.zeros(np.random.randint(0, clip_length*set_Fs-splice.size), np.int16)
    cut = splice.size
    splice = np.append(start, splice)
    splice = np.append(splice, np.zeros(clip_length*set_Fs - splice.size, np.int16))
    signal[start.size:start.size+cut] = np.zeros(cut, np.int16)
    new_signal = np.sum([signal, splice], axis = 0, dtype = np.int16)
    return new_signal
   
def generateDataset(path, out_path, spectrograms, size = 1000, clip_length = 2, set_Fs = 16000, image_shape = (256, 256), add_noise = None, freq_shift = None, mel = False, use_negatives = False):
    """
    Generate training data by creating spectrograms from small clips taken from a dataset of spoken lines from audiobooks. 
    Positive samples have a filler word spliced into the clips.
    
    #Arguments
        size: Size of the dataset to generate
        clip_length: Length in seconds of the sampled clips
        image_shape: Size of the spectrogram images to generate
        add_noise: Add random noise to the clips up. Max power of noise will be this value
        freq_shift: Apply a random frequency shift to the clips up to this value   
        Mel: Boolean. If true, generate a mel spectrogram instead
        
    #Returns
        None
        
    """
    
    dirs = listdir(path)
    i = 0
    while len(listdir(out_path + "0/")) < size//2:
        rand_folder = path + dirs[np.random.randint(0, len(dirs)-1)] + "/"
        subs = listdir(rand_folder)
        if len(subs) == 1:
            rand_sub = rand_folder + subs[0] + "/"
        else:
            rand_sub = rand_folder + subs[np.random.randint(0, len(subs)-1)] + "/"
        files = listdir(rand_sub)
        rand_file = rand_sub + listdir(rand_sub)[np.random.randint(1,len(files)-1)]
        new_file = out_path + "sample" + str(i) + ".wav"
        convertToWav(rand_file, new_file)
        audio = AudioSegment.from_file(new_file, format = "wav")
        matchTargetAmplitude(audio, -30)
        audio.export(new_file, format = "wav")
        data, Fs = getData(new_file)
        if set_Fs != Fs:
            step = Fs//set_Fs
            data = downSample(data, int(set_Fs//2), Fs, step)
            Fs = int(set_Fs)
        samples = splitAudio(data, clip_length, Fs)
        n = len(listdir(out_path + "0/"))
        for j, sample in enumerate(samples):
            sample_file = out_path + "0/" + str(n + j) + ".wav"
            signalToWav(sample,  sample_file, Fs)
        i += 1
    
    for file in listdir(out_path)[2:]:
        remove(out_path + file)
        
    i = 0
    while len(listdir(out_path + "1/")) < size//2:
        if use_negatives == False:
            rand_folder = path + dirs[np.random.randint(0, len(dirs)-1)] + "/"
            subs = listdir(rand_folder)
            if len(subs) == 1:
                rand_sub = rand_folder + subs[0] + "/"
            else:
                rand_sub = rand_folder + subs[np.random.randint(0, len(subs)-1)] + "/"
            files = listdir(rand_sub)
            rand_file = rand_sub + listdir(rand_sub)[np.random.randint(1,len(files)-1)]
            new_file = out_path + "sample" + str(i) + ".wav"
            convertToWav(rand_file, new_file)
            audio = AudioSegment.from_file(new_file, format = "wav")
            matchTargetAmplitude(audio, -30)
            audio.export(new_file, format = "wav")
            data, Fs = getData(new_file)
            if set_Fs < Fs:
                step = Fs//set_Fs
                data = downSample(data, int(set_Fs//2), Fs, step)
                Fs = int(set_Fs)
            samples = splitAudio(data, 2, Fs)
            for i, sample in enumerate(samples):
                samples[i] = spliceRandWord(sample, "uhm's/", 2)
                
            n = len(listdir(out_path + "1/"))
            for j, sample in enumerate(samples):
                sample_file = out_path + "1/" + str(n + j) + ".wav"
                signalToWav(sample,  sample_file, Fs)
            i += 1
        else:
            for file in listdir(out_path + "0/"):
                sample_file = out_path + "1/" + file
                file = out_path + "0/" + file
                sample, Fs = getData(file)
                sample = spliceRandWord(sample, "uhm's/", 2, set_Fs = set_Fs)
                signalToWav(sample, sample_file, Fs)
    for file in listdir(out_path)[2:]:
        remove(out_path + file)

    i = 0
    recordings0 = listdir(out_path + "0/")
    n = len(listdir(spectrograms + "0/"))
    for i, file in enumerate(recordings0[n:]):
        sample, Fs = getData(out_path + "0/" + file)
        if mel == True:
            createMelSpectrogram(sample, spectrograms + "0/" + file)
        else:
            createSpectrogram(sample, spectrograms + "0/" + file, image_shape)
        
    recordings1 = listdir(out_path + "1/")
    n = len(listdir(spectrograms + "1/"))
    for i, file in enumerate(recordings1[n:]):
        sample, Fs = getData(out_path + "1/" + file)
        if mel == True:
            createMelSpectrogram(sample, spectrograms + "1/" + file)
        else:
            createSpectrogram(sample, spectrograms + "1/" + file, img_shape = (256, 256))
            
    splitDataset(BASE_DIR + "capstoneModules/", spectrograms + "0/", 0)
    splitDataset(BASE_DIR + "capstoneModules/", spectrograms + "1/", 1)

def matchTargetAmplitude(sound, target_dBFS):
    """
    Adjust volume of a clip
    
    # Arguments
        sound: An AudioSegment object, see docs for pydub
        target_dBFS: desired volume in dBs
        
    # Returns
        None

    """
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def zeroPadClip(path, filename, clip_length):
    """
    Use zero padding to a obtain desired clip_length
    
    # Arguments
        path: Path to file location
        filename: Name of the file to pad zeros
        clip_length: desired length of clip in seconds

    # Returns
        None

    """

    # Extract Raw Audio from Wav File
    signal, Fs = getData(path + filename)
    clip = np.concatenate([signal, np.zeros(int(Fs*clip_length - signal.size), np.int16)])  # Zero pad up to multiple os our sample window
    signalToWav(clip, path + filename, Fs)

def trimSamples(in_folder, out_folder, target_dir = None, target_Fs = 16e3):
    """
    This function trims an entire folder of clips and saves them somewhere else
    # Arguments
        in_folder: Folder containing raw clips
        out_folder: Folder that will contain the trimmed clips
        target_dir: Trim only a specific folder within the in_folder if desired
        target_Fs: Clips will also be downsamples to this rate

    # Returns
        None

    """
    if not path.exists(out_folder):
        makedirs(out_folder)
        for folder in listdir(in_folder):
            makedirs(out_folder + folder)
            
    tdirs = listdir(in_folder)
    for y in range(len(tdirs)):
        tfiles = listdir(in_folder + tdirs[y])
        for z in range(len(tfiles)-1):
            if not target_dir == None:
                if tdirs[y] == target_dir:
                    tfilename = in_folder + tdirs[y] + "/" + tfiles[z]
                    signal, Fs = getData(tfilename)
                    signal = downSample(signal, target_Fs/2, Fs, int(Fs//target_Fs))
                    signal = trim(signal)
                    signalToWav(signal, out_folder + tdirs[y] + "/" + tdirs[y] + str(z) + ".wav", target_Fs)
                else:
                    break
            else:
                    tfilename = in_folder + tdirs[y] + "/" + tfiles[z]
                    signal, Fs = getData(tfilename)
                    signal = trim(signal)
                    signal = downSample(signal, target_Fs/2, Fs, int(Fs//target_Fs))
                    signalToWav(signal, out_folder + tdirs[y] + "/" + tdirs[y] + str(z) + ".wav", target_Fs)
                


def generateClips(dataset_size, in_path, out_path, clip_words, clip_length, Fs):
    """
    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    """
    words = listdir(in_path)
    dataset_split = 0.5
    
    def appendSample(sound1, in_file):
        sound2 = AudioSegment.from_file(in_file, format="wav")
        sound2 = matchTargetAmplitude(sound2, -30.0)
        sound1 = sound1.append(sound2, crossfade = 0)
        return sound1
        
    for file in listdir(out_path):
        remove(out_path + file)
        
    #This loop generates the clips that do not contain the trigger word
    x = int(len(listdir(out_path))*dataset_split)
    x2 = int(x)
    while x < int(dataset_size*dataset_split):
        for y in range(clip_words):
            rand_word = randint(0, len(words) - 2)
            samples = listdir(in_path + words[rand_word] + '/')
            rand_sample = randint(0, len(samples) - 1)
            in_file = in_path + words[rand_word] + '/' + samples[rand_sample]
            if y == 0:
                sound1 = AudioSegment.from_file(in_file, format="wav").get_sample_slice()
                sound1 = matchTargetAmplitude(sound1, -30.0)
            else:
                sound1 = appendSample(sound1, in_file)
                
        if sound1.frame_count() > Fs*(clip_length - 1) and sound1.frame_count() <= Fs*clip_length:
            padding = AudioSegment.silent(1000*(clip_length - sound1.frame_count()/Fs))
            sound1 = sound1.append(padding, crossfade = 0)
            out_file = out_path + "0_" + str(x) + ".wav"
            sound1.export(out_file, format="wav")
            x = x + 1        
    

    # These clips do contain the trigger words
    while x2 < int(dataset_size*dataset_split):
        trigger_position = randint(0, clip_words-1) ##%#@$%#@$%@#$%@
        for y in range(clip_words):
            rand_word = randint(0, len(words) - 2)
            samples = listdir(in_path + words[rand_word] + '/')
            rand_sample = randint(0, len(samples) - 1)
            in_file = in_path + words[rand_word] + '/' + samples[rand_sample]
            if y == trigger_position:
                samples = listdir(in_path + words[len(words) - 1] + '/')
                rand_sample = randint(0, len(samples) - 1)
                if y == 0:
                    filename = in_path + words[len(words) - 1] + '/' + samples[rand_sample]
                    sound1 = AudioSegment.from_file(filename, format="wav")
                    sound1 = matchTargetAmplitude(sound1, -30.0)
                else:
                    in_file = in_path + words[len(words) - 1] + '/' + samples[rand_sample]
                    sound1 = appendSample(sound1, in_file)
            elif y == 0:
                sound1 = AudioSegment.from_file(in_file, format="wav")
                sound1 = matchTargetAmplitude(sound1, -30.0)
            else:
                sound1 = appendSample(sound1, in_file)
                
        if sound1.frame_count() > Fs*(clip_length - 1) and sound1.frame_count() <= Fs*clip_length:
            padding = AudioSegment.silent(1000*(clip_length - sound1.frame_count()/Fs))
            sound1 = sound1.append(padding, crossfade = 0)
            out_file = out_path + "1_" + str(x2) + ".wav"
            sound1.export(out_file, format="wav")
            x2 = x2 + 1        
            
#        splitDataset()
#    file_handle.close()
    
def createSpectrogram(data, fname, img_shape):
    """
    Create a spectrogram of an audio sample, uses fixed parameters for now as defined here.\n

    # Arguments
        data: 1-D numpy array containing the sample signal data\n
        fname: Name of the image file to be saved\n
        img_shape: A tuple indicating the image size. (height, width) in pixels\n

    # Returns
        None

    """
    # Key parameters of the spectrogram
    Fs = 8000
    noise_cutoff = 80
    NFFT = 256
    noverlap = NFFT/2
    padding = NFFT*1
    window = np.blackman(NFFT)
    cmap = clr.LinearSegmentedColormap.from_list('mycmap', ['black', '#222222', 'white'])
#    img_height = 128
#    img_width = 256
    
    
    # Create the Spectrogram
    vmin = 10*np.log10(np.max(data)) - noise_cutoff
    fig, ax = plt.subplots(1, figsize = (img_shape[1]/256, img_shape[0]/256), dpi = 256)
    fig.subplots_adjust(left = 0, right = 1, bottom = 0, top = 1)
    ax.axis('off')
    (spectrum, freqs, t, _) = ax.specgram(data, NFFT = NFFT, Fs = Fs, window = window, noverlap = noverlap, cmap = cmap, pad_to = padding, vmin = vmin) #cmap after overlap
    ax.axis('off')
    fig.savefig(fname[:-4], frameon = 'false')
    plt.close(fig)
    return (spectrum, t)

def createMelSpectrogram(data, fname, img_shape = (256, 256)):
    """
    Creates a spectrogram using the MFCC's
    
    # Arguments
        data: A 1-D array containing sampled audio data
        fname: Name of the image file to be saved
        
    # Returns
        None

    """   
    data = data/1.0
    # Key parameters of the spectrogram
    cmap = clr.LinearSegmentedColormap.from_list('mycmap', ['black', 'black', '#222222', 'white'])
    
    spectrogram = np.abs(stft(data, n_fft = 1024))**2
    S = feature.melspectrogram(S = spectrogram)

    fig, ax = plt.subplots(1, figsize = (img_shape[1]/256, img_shape[0]/256), dpi = 256)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
    librosa.display.specshow(power_to_db(S, ref=np.max), cmap = cmap)
    pylab.savefig(fname[:-4], bbox_inches=None, pad_inches=0)
    pylab.close(fig)
    
def melCoeffs(signal, Fs):
#    recordToFile("demo6.wav", 16000)
#    signal = getData("demo6.wav")
    coeffs = feature.mfcc(signal/1.0, Fs, None, 13)
    return coeffs
"""
####################################################################################################################
TRAINING THE CLASSIFIER

Not needed for the web version, these functions are used for training purposes
####################################################################################################################
"""

Fs = 8000
# Variables
dataFolder = "clips/"
split = 0.1
categories = 2
img_width = 256
img_height = 512
batch_size = 8
epochs = 5

def splitDataset(directory, folder, cat):
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
#    clips = listdir(audioFolder)
#    images = listdir(imageFolder)
    # Forming the test and training sets
    if not ospath.exists(directory + "training_set"):
        makedirs(directory + "training_set")
        makedirs(directory + "test_set")
        for i in range(categories):
            makedirs(directory + "training_set/" + str(i))
            makedirs(directory + "test_set/" + str(i))
    else:
        for file in listdir(directory + "training_set/" + str(cat)):
            remove(directory + "training_set/" + str(cat) + "/" + file)
        for file in listdir(directory + "test_set/" + str(cat)):
            remove(directory + "test_set/" + str(cat) + "/" + file)

#    if len(images) == 0:  
#        for file in clips:
#            if not file[:-4] + ".png" in images: 
#                data = getData(audioFolder + file)
##                coeffs = melCoeffs(data, Fs)
##                imwrite(imageFolder + "demo.png", coeffs[1:,:])
#                createMelSpectrogram(data, file, imageFolder)
            
    ber = bernoulli.rvs(split, size = len(listdir(folder)))
    for i, filename in enumerate(listdir(folder)):
        if ber[i] == 1:
            copyfile(folder + filename, directory + "test_set/" + str(cat) + "/" + filename)
        else:
            copyfile(folder + filename, directory + "training_set/" + str(cat) + "/" + filename)

def buildClassifier(model_name, img_shape):
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
    # Initializing the CNN
    classifier = Sequential()
    
    # First Layer
    classifier.add(Conv2D(filters = 8, kernel_size = (3, 3), strides = 1, padding = "same", input_shape = (img_shape[0], img_shape[1], 1), activation = "relu")) # 64 kernals of 3x3
#    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(rate = 0.25))
    
    ## Second Layer
    classifier.add(Conv2D(filters = 8, kernel_size = (3, 3), strides = 1, padding = "same", activation = "relu"))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(rate = 0.25))
#    
    ## Third Layer
    classifier.add(Conv2D(filters = 16, kernel_size = (3, 3), strides = 1, padding = "same", activation = "relu"))
#    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(rate = 0.25))
    
    ## Fourth Layer
    classifier.add(Conv2D(filters = 16, kernel_size = (3, 3), strides = 1, padding = "same", activation = "relu"))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(rate = 0.25))
    
    # Flattening
    classifier.add(Flatten())
    
    # Fully Connected Layer
    classifier.add(Dense(activation = "relu", units = 64))
    classifier.add(Dropout(rate = 0.5))
    classifier.add(Dense(activation = "relu", units = 128))
    classifier.add(Dropout(rate = 0.5))
    classifier.add(Dense(activation = "sigmoid", units = 1))
    
    # Compiling the CNN
    classifier.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
    classifier.save(model_name)
    return classifier

def fitClassifier(classifier, model_name, epochs, img_shape, batch_size, data_folder):
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

    train_samples = len(listdir(BASE_DIR + "capstoneModules/training_set/0")) + len(listdir(BASE_DIR + "capstoneModules/training_set/1"))
    test_samples = len(listdir(BASE_DIR + "capstoneModules/test_set/0")) + len(listdir(BASE_DIR + "capstoneModules/test_set/1"))
    
#    train_samples = 4000
#    test_samples = 1000
    
    # Fitting the CNN
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                       width_shift_range = 0.3)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    training_set = train_datagen.flow_from_directory(BASE_DIR + "capstoneModules/training_set",
                                                        target_size = (img_shape[0], img_shape[1]), 
                                                        color_mode = "grayscale",
                                                        batch_size = batch_size,
                                                        class_mode = 'binary')
    test_set = test_datagen.flow_from_directory(BASE_DIR + "capstoneModules/test_set",
                                                target_size = (img_shape[0], img_shape[1]),
                                                color_mode = "grayscale",
                                                batch_size = batch_size,
                                                class_mode = 'binary')
    early_stopping = EarlyStopping(monitor = 'val_accuracy', patience = 3)
    classifier.fit_generator(training_set,
                             steps_per_epoch = train_samples//batch_size,
                             epochs = epochs,
                             validation_data = test_set,
                             validation_steps = test_samples//batch_size,
                             callbacks = [early_stopping])
    classifier.save(model_name)
    
"""
####################################################################################################################
USING THE CLASSIFIER

These functions are used to detect filler words using pretrained models
####################################################################################################################
"""

# GLOBAL VARIABLES

    # Generate the image data to be fed into the network from the spectrograms.
def detectFillers(classifier, fname, img_shape, mel = False):
    """Detect filler words in an audio file with a conv-net classifier object.

    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze
        img_shape: A tuple containing the image size, (img_height, img_width)

    # Returns
        None

    # Raises
        Not handled yet
    """
    # Nueral Network Model
    sample_length = 2 # Window length in seconds for input into the network, this model uses 4
    outFolder = "capstoneModules/live/Images/"
    
    for file in listdir(BASE_DIR + outFolder):
        remove(BASE_DIR + outFolder + file)
        
    signal, Fs = getData(fname)
    samples = splitAudio(signal, sample_length, Fs)
    
    for i in range(len(samples)):
        if mel == True:
            createMelSpectrogram(samples[i,:]/1.0, BASE_DIR + outFolder + "demo" + str(i) + ".wav", img_shape = (256, 256))
        else:
            createSpectrogram(samples[i,:]/1.0, BASE_DIR + outFolder + "demo" + str(i) + ".wav", img_shape = (256, 256))
    
    live_datagen = ImageDataGenerator(rescale = 1./255)
    live_set = live_datagen.flow_from_directory('live',
                                            target_size = (img_shape[0], img_shape[1]),
                                            color_mode = "grayscale",
                                            batch_size = 32,
                                            shuffle = False,
                                            class_mode = 'binary')
    
    # Output a count of all detected instances of the word
    print("Filler words detected: ", np.sum(classifier.predict_classes(live_set[0][0])))
    
    # Use this to see which clips contained the word
    for ind, x in enumerate(classifier.predict_classes(live_set[0][0])):
        print("Clip ", ind,": ", x[0])
        
def mobileNet(img_shape):
    img_shape = (128, 256)
    model = mobilenet.MobileNet(input_shape=(img_shape[0], img_shape[1], 1),
                                alpha=1.0, 
                                depth_multiplier=1, 
                                dropout=1e-3, 
                                include_top=True, 
                                weights=None, 
                                input_tensor=None, 
                                pooling=None, 
                                classes=2)
    
"""
###############################################################################################
YIN Aglorithm Section

Used for pitch detection

###############################################################################################
"""
def crossCorr(x, tau, W, auto = False):
    """
    Autocorrelation, Step 1, Eq. (1)\n
    
    Computes the cross correlation between a signal and a shifted version. If auto = True, 
    computes the auto correlation of the signal shifted by tau.
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        tau: Integer sample lag
        W: Integer integration window size.
        auto: Boolean, set True for autocorrelation
        
    # Returns
        cross_corr_mat: A 2-D numpy array of the correlation function for each sample. 
        Each row corresponds to a sample.
    """
        
    cross_corr_mat = np.zeros((x.size//W, W), np.float32)
    x_orig = list(x)
    for i in range(cross_corr_mat.shape[0]):
        t = i*W
        # Unbias the signals
        x = x_orig[t:W+t] - np.mean(x_orig[t:W+t])
        x_tau = x_orig[t+tau:t+tau+W] - np.mean(x_orig[t+tau:t+tau+W])
        if len(x_tau) == 0:
            break
        if (auto == False):
            cross_corr = np.correlate(x, x_tau, 'full')#/npsum(x**2)
            cross_corr_mat[i,:] = cross_corr[cross_corr.shape[0]//2:]
            
        else:
            cross_corr = np.correlate(x_tau, x_tau, 'full')
            try:
                cross_corr_mat[i,:] = cross_corr[cross_corr.shape[0]//2:]
            except:
                cross_corr_mat[i,:] = np.append(cross_corr[cross_corr.shape[0]//2:], np.zeros((1, W-cross_corr[cross_corr.shape[0]//2:].size), np.float32))
                

    return cross_corr_mat


def diffEquation(x, W):
    """
    Difference Equation, Step 2, Eq. (7)\n
    
    Computes the difference equation for each sample
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        W: Integration window size
        
    # Returns
        diff_eq_mat: A 2-D numpy array of the computed difference equations for each sample.
        Each row corresponds to a sample.
    """
    
    auto_corr_mat = crossCorr(x, 0, W, auto = True)
    diff_eq_mat = np.zeros(auto_corr_mat.shape, np.float32)
    for i in range(0, diff_eq_mat.shape[0]):
        diff_eq_mat[i,:] = auto_corr_mat[i, 0] + crossCorr(x, i, W, auto = True)[i, 0] - 2 * auto_corr_mat[i,:]
    return diff_eq_mat

def cumMeanNormDiffEq(x, W):
    """
    Cumulative Mean Normal Difference Equation, Step 3, Eq. (8)\n
    
    Computes the cumulative mean normal difference equation for each sample
    
    # Arguments
        x: A 1-D numpy array containing the signal\n
        W: Integration window size
        
    # Returns
        cum_diff_mat: A 2-D numpy array of the computed difference equations
        for each sample. Each row corresponds to a sample.
    """
    diff_eq_mat = diffEquation(x, W)
    cum_diff_mat = np.zeros(diff_eq_mat.shape, np.float32)
    cum_diff_mat[:, 0] = 1
    for t in range(diff_eq_mat.shape[0]):
        for j in range(1, diff_eq_mat.shape[1]):
            cum_diff_mat[t, j] = diff_eq_mat[t, j]/((1/j)*np.sum(diff_eq_mat[t, 1:j+1]))
    return cum_diff_mat
        
def absoluteThresold(x, freq_range = (40, 300), threshold = 0.1, Fs = 16e3):
    """
    Absolute Threshold Method, Step 4\n
    
    Computes the initial period predicition of each sample using the method described
    in Step 4 of the paper.
    
    #Arguments
        x: A 1-D numpy array containging the signal\n
        freq-range: A tuple containing the search range ex. (min_freq, max_freq)\n
        threshold: A floating point threshold value for picking the minimum of the
        cumulative mean normal difference equation.\n
        Fs: The sampling rate.
    
    #Returns
        taus: A 1-D numpy array containing the candidate period estimates for each sample.\n
        cum_diff_mat: A 2-D numpy array, see documentaion for `cumMeanNormDiffEq`.
    

    """
    tau_min = int(Fs)//freq_range[1]
    tau_max = int(Fs)//freq_range[0]-1


    tau_star = 0
    minimum = 1e9
    cum_diff_mat = cumMeanNormDiffEq(x, tau_max+1)
    taus = np.zeros(cum_diff_mat.shape[0], np.int32)
    for i in range(taus.size):
        cum_diff_eq = cum_diff_mat[i,:]
        for tau in range(tau_min, tau_max):
            if cum_diff_eq[tau] < threshold:
                taus[i] = tau
                break
            elif cum_diff_eq[tau] < minimum:
                tau_star = tau
                minimum = cum_diff_eq[tau]
        if taus[i] == 0:
            taus[i] = tau_star
    return taus, cum_diff_mat
    
def parabolicInterpolation(diff_matrix, taus, freq_range, Fs):
    """
    Parabolic Interpolation, Step 4\n
    
    Applies parabolic interpolation onto the candidate period estimates using
    3 points corresponding to the estimate and it's adjacent values
    
    #Arguments
        diff_mat: A 2-D numpy array, see documentaion for `diffEquation`\n
        taus: A 1-D numpy array for the candidate estimates
        freq-range: A tuple containing the search range ex. (min_freq, max_freq)\n
        Fs: The sampling rate.
    
    #Returns
        local_min_abscissae: A 1-D numpy array containing the interpolated period estimates
        for each sample.
    

    """
    abscissae = np.zeros((len(taus)-2, 3), np.float32)
    ordinates = np.zeros(abscissae.shape, np.float32)
    #if taus == []:
    for i, tau in enumerate(taus[1:-1]):
        ordinates[i-1] = diff_matrix[i, tau-1:tau+2]
        abscissae[i-1] = np.asarray([tau-1, tau, tau+1], np.float32)
        
    period_min = int(Fs)//freq_range[1]
    period_max = int(Fs)//freq_range[0]
        
    coeffs = np.zeros((len(taus)-2, 3))
    local_min_abscissae = np.zeros(coeffs.shape[0])
    local_min_ordinates = np.zeros(coeffs.shape[0])
    for i in range(0, len(taus)-2):
        coeffs[i] = np.polyfit(abscissae[i,:], ordinates[i,:], 2)
        p = np.poly1d(coeffs[i]).deriv()
        if p.roots > period_min and p.roots < period_max:
            local_min_abscissae[i] = p.roots
        else:
            local_min_abscissae[i] = taus[i+1]
        local_min_ordinates[i] = p(local_min_abscissae[i])
        
    return local_min_abscissae

def pitchTrackingYIN(fname, freq_range = (40, 300), threshold = 0.1, timestep = 0.1, target_Fs = 8e3, Fc = 1e3):
    """
    Putting it all together, this function is my implementation the the YIN pitch detection algorithm. 
    
    #Arguments
        fname: The name of a WAV file to be analyzed.
        freq-range: An integer tuple containing the search range ex. (min_freq, max_freq)
        threshold: A float specifying the threshold for step 4
        timestep: Tracking period in milliseconds.
        target_Fs: Target sampling rate after downsampling. Use Fs for no downsampling. Note that the original sampling rate must
        be a multiple of the target rate. For example, this cannot downsample 44.1k to 16k.
        Fc: Cutoff frequency of the lowpass filter used in downsampling the signal. Must be less than target_Fs/2.
    
    #Returns
        f: A 1-D numpy array containing the frequency esimates
    #Raises
        ValueError: If a silent audio file is used.
    """
    # Extract signal from audio file
    signal, Fs = getData(fname)

    # Downsample signal if desired to improve speed
    step = int(Fs//target_Fs)
    if not step == 1:
        signal = downSample(signal, 1e3, Fs, step)
        Fs = int(target_Fs)

    # Remove silence from beginning and end of the file to improve speed
    signal = np.asarray(trim(signal))
    signal = signal.astype(np.float32)

    # Integration window is dependent on the lowest frequency to be detected
    W = int(np.ceil(Fs/freq_range[0]))
    # The idea here is to keep only what we need to analyze.
    # If we are going to track frequency every 25ms, then we don't need the information in between
    # these points outside of the integration window.
    sampled_signal = np.zeros(((signal.size//int(Fs*timestep)),2*W), np.float32)
    if sampled_signal.shape[0] < 5:
        raise RuntimeError("Speech is too short or possibly too quiet. Try again and make sure that the original file has been deleted")
        
    for i in range((signal.size//int(Fs*timestep))):
        t = int(i*Fs*timestep)
        sampled_signal[i,:] = signal[t:int(t+2*W)]/max(signal[t:int(t+2*W)])
        
    sampled_signal = sampled_signal.flatten()

    # This new signal has been minimized in length and normalized, preprocessing is finished
    signal = sampled_signal
    if len(signal) > 0:
        pass
    else:
        raise ValueError("Detected a silent file, you might need to speak louder")
    

    # Now apply the algorithm, note that step 6 is still missing
    taus = absoluteThresold(signal, freq_range, threshold, Fs)[0]
    diff_mat = diffEquation(signal, W)
    periods = parabolicInterpolation(diff_mat, taus, freq_range, Fs)
    # Minues 2 because the interpolation throws away two estimates
    f = np.zeros((int(signal.size/W-2), 1), np.int32)
    for i in range(int(signal.size/W-2)):
        f[i] = Fs//periods[i]
    return f

def volumeAnalysis(fname, window  = 500, threshold = -10):
    """
    Examine the change in volume throughout the audio clip
    
    #Arguments
        fname: String, name of the audio file to analyze
        window: Integer indicating the length of the moving window in milliseconds
    
    #Returns
        clip_powersdB: A 1-D array containing the power of each clip with respect to the whole signal in decibels
        
    """
    signal, Fs = getData(fname)
    
    def countPauses(power_vector, threshold = threshold, window = window):
        pauses = np.zeros((1, 2))
        num_silent = 0
        is_paused = False
        i = 0
        while i < power_vector.size:
            x = power_vector[i]
            if x < threshold:
                is_paused = True
                num_silent += 1
            else:
                is_paused = False
            if not is_paused and num_silent:
                # Append [start index, duration]
                pause = np.asarray([window*(i-num_silent)/1000, window*num_silent/1000]).reshape(1,-1)
                pauses = np.append(pauses, pause, axis = 0)
                num_silent = 0
            i += 1
        return pauses[1:]

    W = int(Fs*window/1000)
    signal = np.asarray(trim(signal, threshold = 1000), np.float32)
    signal = signal - np.mean(signal)
    signal_powerdB = 10*np.log10(np.dot(signal, signal)/signal.size**2)
    clip_powersdB = np.zeros((signal.size//W), np.float32)
    for i in range(clip_powersdB.size):
        t = i*W
        clip = signal[t:t+W] - np.mean(signal[t:t+W])
        clip_power = abs(np.dot(clip, clip)/W**2)
        if clip_power%100:
            clip_powersdB[i] = 10*np.log10(clip_power) - signal_powerdB
        else:
            clip_powersdB[i] = -100  
            
    pauses = countPauses(clip_powersdB)
             
    return clip_powersdB, pauses


"""
DO TESTING HERE

DON'T FORGET TO COMMENT STUFF OUT BEFORE PUSHING
"""

##### Testing new pause detection
#power_vector, pauses = volumeAnalysis("../../audio/output_mono.wav", 100, -10)
#plt.plot(power_vector)
#pauses = countPauses(power_vector, threshold = -10)

#### ConvNet stuff
#path = "C:/Users/Austin/Desktop/School/Capstone/LibriSpeech/train-clean-100/"
##out_path = BASE_DIR + "capstoneModules/recordings/"
#spectrograms = BASE_DIR + "capstoneModules/16k_mel_spectrograms/"
#generateDataset(path = "C:/Users/Austin/Desktop/School/Capstone/LibriSpeech/train-clean-100/",
#                out_path = BASE_DIR + "capstoneModules/16k_clips/",
#                spectrograms = BASE_DIR + "capstoneModules/16k_mel_spectrograms/",
#                size = 10000,
#                clip_length = 2,
#                set_Fs = 16000,
#                image_shape = (256, 256),
#                add_noise = None,
#                freq_shift = None,
#                mel = True,
#                use_negatives = True)
#for i, file in enumerate(listdir("ds_recordings/")):
#    file = "ds_recordings/" + file
#    audio = AudioSegment.from_file(file, format = "wav")
#    matchTargetAmplitude(audio, -30)
#    audio.export(file, format = "wav")
#    data, Fs = getData(file)
#    data = data[:-32000]
##    data = downSample(data, 4000, 16000, 2)
#    samples = splitAudio(data, 2, 16000)
#    for j, sample in enumerate(samples):
#            sample_file = "16k_clips/0/add_" + str(i) + "_" + str(j) + ".wav"
#            signalToWav(sample,  sample_file, 16000)
#            data, Fs = getData(sample_file)
#            data = spliceRandWord(data, "uhm's/", 2, Fs)
#            sample_file = "16k_clips/1/add_" + str(i) + "_" + str(j) + ".wav"
#            signalToWav(data, sample_file, Fs)
#
#for folder in listdir("16k_clips/"):
#    folder = "16k_clips/" + folder + "/"
#    for file in listdir(folder):
#        data, Fs = getData(folder + file)
#        createMelSpectrogram(data, spectrograms + folder[-2:] + file, img_shape = (256, 256))
##    
#generateDataset(path, out_path, spectrograms, 10000, use_negatives = True, mel = True)
#convertToWav()
#classifier = buildClassifier("filler_detector_mel_0.h5", (256, 256))
#fitClassifier(classifier, "filler_detector_mel_0.h5", 20, (256, 256), 32, BASE_DIR)

### TESTING THE DETECTOR
#file = "testing.wav"
#recordToFile(file, 16000)
#signal, Fs = getData(file)
#plt.figure()
#plt.plot(signal[0:32000])
#plt.figure()
#plt.plot(signal[16000:17024])
#F = np.abs(stft(signal[16000:17024]/1.0, n_fft = 1024))[:,0]
#F = 255*F/max(F)
#plt.figure()
#plt.plot(np.linspace(0, 8000, 513), F)
#librosa.display.specshow(librosa.amplitude_to_db(F, ref=np.max), y_axis='log', x_axis='time')
#classifier = load_model("ConvNets/filler_detector_mel_0_20_epochs.h5")
#detectFillers(classifier, "testing.wav", (256, 256), mel = True)

## Generating new uhms
#folder = "uhm's/"
#for file in listdir(folder):
#    for i in range(1, 10):
#        freqShift(folder + file, folder + str(i) + file, 2*i)
#        freqShift(folder + file, folder + "-" + str(i) + file, -1*i)
    

### Pitch Stuff
#file = "testing.wav"
#recordToFile(file, 16000)
#signal, Fs = getData(file)
#signal = signal[:32000]
#plt.figure()
#plt.plot(signal[16000:16400])

#cumulative = cumMeanNormDiffEq(signal[16000:17600], 400)
#plt.figure()
#plt.plot(cumulative[0])
#plt.plot(np.linspace(0,1600, 1600), 0.1*np.ones(1600))