# -*- coding: utf-8 -*-
from api.capstoneModules.audioFunctions import trim
from os import listdir, remove, makedirs, path
from random import randint
import wave
from struct import pack
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import pylab
import librosa
import librosa.display

PATH = "C:/Users/Austin/Desktop/School/Capstone/"

def matchTargetAmplitude(sound, target_dBFS):
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
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def zeroPadClip(path, filename, clip_length, Fs):
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
    spf = wave.open(path + filename, 'r')
    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, np.int16)
    clip = np.concatenate([signal, np.zeros(int(Fs*clip_length - signal.size), np.int16)])  # Zero pad up to multiple os our sample window
    clip = pack('<' + ('h' * len(clip)), *clip)
    wf = wave.open(path + filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(Fs)
    wf.writeframes(clip)
    wf.close()
    spf.close()

def trimSamples(directory, outFolder, Fs):
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
    if not path.exists(PATH + outFolder):
        makedirs(PATH + outFolder)
        for folder in listdir(directory):
            makedirs(PATH + outFolder + folder)
    tfolders = [directory]
    for x in range(len(tfolders)):
        tdirs = listdir(tfolders[x])
        for y in range(len(tdirs)):
            tfiles = listdir(tfolders[x] + tdirs[y])
            for z in range(len(tfiles)-1):
                tfilename = tfolders[x] + tdirs[y] + "/" + tfiles[z]
                spf = wave.open(tfilename, 'r')
                signal = spf.readframes(-1)
                signal = np.frombuffer(signal, np.int16)
                signal = trim(signal)
                clip = pack('<' + ('h' * len(signal)), *signal)
                wf = wave.open(outFolder + tdirs[y] + "/" + tdirs[y] + str(z) + ".wav", 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(Fs)
                wf.writeframes(clip)
                wf.close()
                spf.close()
                
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
    extension = filename[filename.find(".")+1:]
    if extension != "wav":
        audio = AudioSegment.from_file(file = filename, format = extension)
        audio.export(filename[0:len(filename)-4] + '.wav', format="wav")

def generateClips(dataset_size, in_path, out_path, clip_words, clip_length, Fs):
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
    words = listdir(in_path);
    dataset_split = 0.5
    
    def appendSample(sound1, in_file):
        sound2 = AudioSegment.from_file(in_file, format="wav")
        sound2 = matchTargetAmplitude(sound2, -30.0)
        sound1 = sound1.append(sound2, crossfade = 0)
        return sound1
        
#    for file in listdir(out_path):
#        remove(out_path + file)
        
    # This loop generates the clips that do not contain the trigger word
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
    #file_handle.close()       
    
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
    #file_handle.close()
    
def createSpectrogram(data, fname, outFolder):
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
    # Key parameters of the spectrogram
    Fs = 8000
    noise_cutoff = 80
    NFFT = 256
    noverlap = NFFT/2
    padding = NFFT*1
    window = np.blackman(NFFT)
    cmap = clr.LinearSegmentedColormap.from_list('mycmap', ['black', '#101010', 'white'])
    img_height = 256
    img_width = 512
    
    
    # Create the Spectrogram
    vmin = 10*np.log10(np.max(data)) - noise_cutoff
    fig, ax = plt.subplots(1, figsize = (img_width/128, img_height/128), dpi = 128)
    fig.subplots_adjust(left = 0, right = 1, bottom = 0, top = 1)
    ax.axis('off')
    (spectrum, freqs, t, _) = ax.specgram(data, NFFT = NFFT, Fs = Fs, window = window, noverlap = noverlap, cmap = cmap, pad_to = padding, vmin = vmin)
    ax.axis('off')
    fig.savefig(outFolder + fname[:-4], frameon = 'false')
    plt.close(fig)
    return (spectrum, t)

def createMelSpectrogram(data, fname, outFolder):
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
    data = data/1.0
    # Key parameters of the spectrogram
    cmap = clr.LinearSegmentedColormap.from_list('mycmap', ['black', 'black', '#222222', 'white'])
    
    spectrogram = np.abs(librosa.stft(data))**2
    S = librosa.feature.melspectrogram(S = spectrogram)

#    plt.figure(figsize=(10, 4))
#     fig, ax = plt.subplots(1, figsize = (img_width/128, img_height/128), dpi = 128)
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), cmap = cmap)
    pylab.savefig(outFolder + fname[:-4], bbox_inches=None, pad_inches=0)
    pylab.close()


