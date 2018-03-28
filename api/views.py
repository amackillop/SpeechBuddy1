# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
#from serializers import nltkPostSerializer
from rest_framework.response import Response
#from models import nltkModel
#csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect

#corpus
from api.nltkMethod import mostCommon
from api.nltkMethod import synCreate
from api.googleMethod import googleApiCall
from api.sentimentMethod import sentimentCall
import json
import cgi
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from api.capstoneModules import capstoneFunctions as cf
#from api.capstoneModules.YIN_Algorithm import pitchTrackingYIN
#from api.capstoneModules.audioFunctions import convertToFLAC, convertToMono
#from api.capstoneModules.fillerWordDetection import detectFillers

from os import listdir, remove, path
from django.conf import settings
#from keras.backend import clear_session

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
ROOT = path.join(path.dirname(BASE_DIR))



# Create your views here.
#class ViewAPI(APIView):

@api_view(['GET', 'POST'])
def nltkCall(request):
    if request.method == 'POST':
        dictData = request.data
        data = dictData['string']
        data = data.encode('ascii')
        print(data)
        resData = mostCommon(data)
        indexArray = str(resData[0])
        corpus = str(resData[1])
        tok = resData[2]
        listSyn = str(resData[3])
        return Response({"indexArray": indexArray, "corpus": corpus, "tok": tok, "listSyn": listSyn})
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def googleOAuthCall(request):
    if request.method == 'POST':
        dictData = request.data
        print(dictData)
    return Response({"message": "User Authenticated"})

@api_view(['GET', 'POST'])
def googleCall(request):
    if request.method == 'POST':
        # Save the audio file
        dataDict = request.data
        dataDict = dataDict['audio']
        path = default_storage.save(settings.MEDIA_ROOT + "/output.wav", ContentFile(dataDict.read()))
        
        # Manipulate original audio file
        cf.convertToMono(settings.MEDIA_ROOT + "/output.wav", settings.MEDIA_ROOT + "/output_mono.wav")
        cf.convertToFLAC(settings.MEDIA_ROOT + "/output_mono.wav", settings.MEDIA_ROOT + "/output_mono.flac")
        
        # Delete original file
        if default_storage.exists(path):
            default_storage.delete(path)
        res = googleApiCall(settings.MEDIA_ROOT + "/Simon_Sinek_30.flac")
        
        if not res == "Empty Response":
            transcript = str(res[0])
            sentences = str(res[3])
            confidence = float(res[1])
            confidence = round(confidence, 4)*100
            wpm = str(res[2])
            resData = mostCommon(transcript)
            indexArray = str(resData[0])
            corpus = str(resData[1])
            tok = resData[2]
            list_of_sentences = res[3]
            listSyn = str(resData[3])
            list_of_sentences = res[3]
            wordsperminute = res[4]
            sentimentArray = sentimentCall(list_of_sentences)
            print(sentimentArray)


        else:
            transcript = "empty response"
            sentences = "empty response"
            confidence = 1
            wpm = str(0)
            indexArray = [""]
            corpus = ""
            tok = ""
            listSyn = ""
            list_of_sentences="empty response"
            wordsperminute="empty response"
            
        
        # Pitch Tracking
        f0 = cf.pitchTrackingYIN(settings.MEDIA_ROOT + "/output_mono.wav", freq_range = (40, 500), threshold = 0.1, timestep = 0.25, Fc = 1e3)
        f1 = cf.pitchTrackingYIN(settings.MEDIA_ROOT + "/output_mono.wav", freq_range = (500, 1000), threshold = 0.1, timestep = 0.25, Fc = 1e3)
        f = np.zeros((f0.shape[0], 3))
        for i in range(f.shape[0]):
            f[i, :] = np.asarray([i, f0[i], f1[i]])

        # Volume Tracking
        vol = cf.volumeAnalysis(settings.MEDIA_ROOT + "/output_mono.wav", 100)
        V = np.zeros((vol.shape[0], 2))
        for i in range(V.shape[0]):
            V[i, :] = np.asarray([i, -vol[i]])

        # Filler wod detection
#        global graph
       # with settings.GRAPH.as_default():
        filler_count = 0
        return Response({
            "transcript": transcript,
            "sentences": sentences,
            "confidence": confidence,
            "wpm": wpm,
            "indexArray": indexArray,
            "corpus": corpus,
            "tok": tok,
            "listSyn": listSyn,
            "pitch": f,
            "filler_count": filler_count,
            "volume": V,
            "list_of_sentences" : list_of_sentences,
            "wordsperminute" : wordsperminute
        })
    return Response({"message": "Hello, world!"})
