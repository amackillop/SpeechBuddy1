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
import json
import cgi
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from api.capstoneModules.YIN_Algorithm import pitchTrackingYIN
from api.capstoneModules.audioFunctions import convertToFLAC, convertToMono
from api.capstoneModules.fillerWordDetection import detectFillers

from os import listdir, remove, path
from django.conf import settings

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
def synCall(request):
    if request.method == 'POST':
        dictData = request.data
        data = dictData['string']
        data = data.encode('ascii')
        print(type(data))
        resData = synCreate(data)
        resData=str(resData)

        return Response({"message": "Got some data!", "resData": resData})
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def googleCall(request):
    if request.method == 'POST':
        # Save the audio file
        dataDict = request.data
        dataDict = dataDict['audio']
        path = default_storage.save(ROOT+'/SpeechBuddy1/audio/output.wav', ContentFile(dataDict.read()))
        
        # Manipulate original audio file
        convertToMono(ROOT+'/SpeechBuddy1/audio/output.wav', ROOT + "/SpeechBuddy1/audio/output_mono.wav")
        convertToFLAC(ROOT+'/SpeechBuddy1/audio/output_mono.wav', ROOT + "/SpeechBuddy1/audio/output_mono.flac")
        
        # Delete original file
        if default_storage.exists(path):
            default_storage.delete(path)
        res = googleApiCall(ROOT+'/SpeechBuddy1/audio/Simon_Sinek_30.flac')
        
#        fundementals = f0.tolist
        if not res == "Empty Response":
            transcript = str(res[0])
            confidence = float(res[1])
            confidence = round(confidence, 4)*100
            wpm = str(res[2])
            resData = mostCommon(transcript)
            indexArray = str(resData[0])
            corpus = str(resData[1])
            tok = resData[2]
            listSyn = str(resData[3])
        else:
            transcript = "empty response"
            confidence = 1
            wpm = str(0)
            indexArray = [""]
            corpus = ""
            tok = ""
            listSyn = ""
            
        
        # Pitch Tracking
        f0 = pitchTrackingYIN(ROOT+'/SpeechBuddy1/audio/output_mono.wav', freq_range = (40, 300), threshold = 0.1, timestep = 0.25, Fs = 48e3, Fc = 1e3)
        
        # Filler wod detection
#        global graph
        with settings.GRAPH.as_default():
            filler_count = str(detectFillers(ROOT, settings.MODEL, "output_mono.wav", Fs = 48e3))
        
#        #Get rid of files
#        if default_storage.exists(path):
#            default_storage.delete(path)
        #res = '''{"Transcript": "my problem has been resolved thanks to colleague Brian call at text up the problem is that before the PIP I try to install Google Cloud manually by downloading the source and running setup talk to you why","Confidence": 0.931040287018,"Words": [["my", 0.0, 1.2],["problem", 1.2, 1.7],["has", 1.7, 1.9],["been", 1.9, 2.0],["resolved", 2.0, 2.6],["thanks", 2.6, 3.0],["to", 3.0, 3.2],["colleague", 3.2, 3.7],["Brian", 3.7, 4.1],["call", 4.1, 4.5],["at", 4.5, 4.9],["text", 4.9, 5.4],["up", 5.4, 5.6],["the", 5.6, 6.7],["problem", 6.7, 7.0],["is", 7.0, 7.6],["that", 7.6, 8.2],["before", 8.2, 8.6],["the", 8.6, 9.1],["PIP", 9.1, 9.4],["I", 9.4, 10.1],["try", 10.1, 10.6],["to", 10.6, 10.9],["install", 10.9, 11.1],["Google", 11.1, 11.6],	["Cloud", 11.6, 12.0],["manually", 12.0, 12.7],["by", 12.7, 12.9],["downloading", 12.9, 13.5],["the", 13.5, 13.7],["source", 13.7, 14.1],	["and", 14.1, 14.3],["running", 14.3, 14.8],["setup", 14.8, 15.8],["talk", 15.8, 16.1],	["to", 16.1, 16.2], ["you", 16.2, 16.3],["why", 16.3, 16.5]]}'''
        #print(res)
        return Response({"transcript": transcript, "confidence": confidence, "wpm": wpm, "indexArray": indexArray, "corpus": corpus, "tok": tok, "listSyn": listSyn, "pitch": f0, "filler_count": filler_count})
    return Response({"message": "Hello, world!"})
