# -*- coding: utf-8 -*-
from capstoneModules.audioFunctions import loadAudio, splitAudio, downSample
from numpy import zeros, average, float16, int16
import matplotlib.pyplot as plt

# GLOBAL VARIABLES
def analyzePitch(fname, Fs): 
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
    # Extract the audio data from the wav file
    sample_length = 0.5 #seconds
    
    signal = loadAudio(fname)
    
    live_samples = splitAudio(signal, sample_length)
    
    # Downsamples the samples, most variation occurs at frequencies under 4k
    downsampled_audio = zeros((live_samples.shape[0], int(live_samples.shape[1]/2)), int16)
    step = 2
    for i in range(len(live_samples)):
        downsampled_audio[i,:] = downSample(live_samples[i,:], cutoff = Fs/(2*step), Fs = Fs, step = step)
    Fs_down = Fs/step  
    
    bin_width = 500
    n_bins = int((Fs_down/2)/bin_width)
    avg_freqs = zeros((downsampled_audio.shape[0], n_bins), float16)
    max_freqs = zeros(avg_freqs.shape, float16)
    avg_freqs_zeroed = zeros(avg_freqs.shape, float16)
    max_freqs_zeroed = zeros(avg_freqs.shape, float16)
    max_proportions = zeros(avg_freqs.shape, float16)
    for i in range(len(downsampled_audio)):
        (spectrum, freqs, _) = plt.magnitude_spectrum(downsampled_audio[i,:], Fs = Fs_down)
        freqs = freqs/(2*max(freqs))
        spectrum = spectrum
        for j in range(int(n_bins)):
            #avg_freqs[i, j] = (Fs_down)*np.dot(spectrum[int(j*Fs_down/n_bins):int((j+1)*Fs_down/n_bins)], freqs[int(j*Fs_down/n_bins):int((j+1)*Fs_down/n_bins)])/sum(spectrum[int(j*Fs_down/n_bins):int((j+1)*Fs_down/n_bins)])
            max_freqs[i, j] = max(spectrum[int(j*sample_length*Fs_down/(2*n_bins)):int((j+1)*sample_length*Fs_down/(2*n_bins))])
    
    for i in range(n_bins):        
        avg_freqs_zeroed[:, i] = avg_freqs[:, i] - average(avg_freqs[:, i])
        max_freqs_zeroed[:, i] = max_freqs[:, i] - average(max_freqs[:, i])
        
    for i in range(live_samples.shape[0]):
        if sum(max_freqs[i, :]) != 0:
            max_proportions[i, :] = max_freqs[i, :]/sum(max_freqs[i, :])
    
    plt.figure()
    plt.boxplot(max_proportions)