
# Importing required modules for using the model
from api.capstoneModules.audioFunctions import getData, splitAudio, downSample
from api.capstoneModules.dataGenerator import createMelSpectrogram, createSpectrogram
from keras.preprocessing.image import ImageDataGenerator
#from keras.models import load_model

import numpy as np
from os import listdir, remove

# GLOBAL VARIABLES
IMG_HEIGHT = 256
IMG_WIDTH = 512
    # Generate the image data to be fed into the network from the spectrograms.
def detectFillers(ROOT, classifier, fname, Fs = 48e3):
    """Detect filler words in an audio file with a conv-net classifier object.

    # Arguments
        classifier: Name of the h5 file containing the classifier
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    fname = ROOT + "/SpeechBuddy1/audio/" + fname
    # Nueral Network Model
#    classifier = load_model(ROOT + "/SpeechBuddy1/audio/"+ classifier)
    sample_length = 4 # Window length in seconds for input into the network, this model uses 4
    outFolder = ROOT + "/SpeechBuddy1/audio/live/Images/"
    
    for file in listdir(outFolder):
        remove(outFolder + file)
        
    signal = getData(fname)
    step = int(Fs//16e3)
    signal = downSample(signal, 8e3, 48e3, step)
    samples = splitAudio(signal, sample_length)
    Fs = 16e3
    
    for i in range(len(samples)):
        createSpectrogram(samples[i,:]/1.0, "demo" + str(i) + ".wav", outFolder)
#        createMelSpectrogram(samples[i,:]/1.0, "demo" + str(i) + ".wav", outFolder)
    
    live_datagen = ImageDataGenerator(rescale = 1./255)
    live_set = live_datagen.flow_from_directory(ROOT + '/SpeechBuddy1/audio/live',
                                            target_size = (IMG_HEIGHT, IMG_WIDTH),
                                            color_mode = "grayscale",
                                            batch_size = 32,
                                            class_mode = 'binary')
    
    num_fillers = np.sum(classifier.predict_classes(live_set[0][0]))
    # Output a count of all detected instances of the word
    print("Filler words detected: ", num_fillers)
    
    # Use this to see which clips contained the word
    for ind, x in enumerate(classifier.predict_classes(live_set[0][0])):
        print("Clip ", ind,": ", x[0])

    return num_fillers

    