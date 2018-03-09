# -*- coding: utf-8 -*-

# Importing required libraries for training
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing.image import ImageDataGenerator

from scipy.stats import bernoulli
from os import listdir, makedirs, path
from shutil import copyfile

from capstoneModules.dataGenerator import createMelSpectrogram
from capstoneModules.audioFunctions import getData

PATH = "C:/Users/Austin/Desktop/School/Capstone/"

# Variables
dataFolder = "clips/"
split = 0.2
categories = 2
img_width = 400
img_height = 300
batch_size = 32
epochs = 1

def createSets(audioFolder, imageFolder):
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
    # Forming the test and training sets
    if not path.exists(PATH + "training_set"):
        makedirs(PATH + "training_set")
        makedirs(PATH + "test_set")
        for i in range(categories):
            makedirs(PATH + "training_set/" + str(i))
            makedirs(PATH + "test_set/" + str(i))
                
    if len(listdir(imageFolder)) == 0:  
        for file in listdir(audioFolder):
            data = getData(audioFolder + file)
            createMelSpectrogram(data, file, imageFolder)
            
    ber = bernoulli.rvs(split, size = len(listdir(imageFolder)))
    for i, filename in enumerate(listdir(imageFolder)):
        if ber[i] == 1:
            copyfile(imageFolder + filename, PATH + "test_set/" + filename[0] + "/" + filename)
        else:
            copyfile(imageFolder + filename, PATH + "training_set/" + filename[0] + "/" + filename)

def buildClassifier(model_name):
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
    classifier.add(Conv2D(filters = 8, kernel_size = (3, 3), strides = 1, padding = "same", input_shape = (img_height, img_width, 1), activation = "relu")) # 64 kernals of 3x3
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    
    ## Second Layer
    classifier.add(Conv2D(filters = 8, kernel_size = (3, 3), strides = 1, padding = "same", activation = "relu"))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    
    ## Third Layer
    classifier.add(Conv2D(filters = 16, kernel_size = (3, 3), strides = 1, padding = "same", activation = "relu"))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    
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

def fitClassifier(classifier):
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
    classifier = classifier
    train_samples = len(listdir(PATH + "training_set/0")) + len(listdir(PATH + "training_set/1"))
    test_samples = len(listdir(PATH + "test_set/0")) + len(listdir(PATH + "test_set/1"))
    
#    train_samples = 4000
#    test_samples = 1000
    
    # Fitting the CNN
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                       width_shift_range = 0.3)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    training_set = train_datagen.flow_from_directory(PATH + 'training_set',
                                                        target_size = (img_height, img_width), 
                                                        color_mode = "grayscale",
                                                        batch_size = batch_size,
                                                        class_mode = 'binary')
    test_set = test_datagen.flow_from_directory('test_set',
                                                target_size = (img_height, img_width),
                                                color_mode = "grayscale",
                                                batch_size = batch_size,
                                                class_mode = 'binary')
    classifier.fit_generator(training_set,
                             steps_per_epoch = train_samples,
                             epochs = epochs,
                             validation_data = test_set,
                             validation_steps = test_samples)
    classifier.save("Model_4_GoNoGo_5.h5")