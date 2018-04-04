# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
import io
# from PIL import Image
import base64
import re
# from serializers import nltkPostSerializer
from rest_framework.response import Response
# from models import nltkModel
# csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect

# corpus
from api.nltkMethod import mostCommon
from api.nltkMethod import synCreate
from api.googleMethod import googleApiCall
from api.googleDrive import saveFileInDrive
from api.sentimentMethod import sentimentCall
from api.stichPicsMethod import stichImagesCall
from api.azureMethod import AzureCall
from api.watsonToneMethod import watsontoneCall
import json
import cgi
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from api.capstoneModules import capstoneFunctions as cf
# from api.capstoneModules.YIN_Algorithm import pitchTrackingYIN
# from api.capstoneModules.audioFunctions import convertToFLAC, convertToMono
# from api.capstoneModules.fillerWordDetection import detectFillers
import os

from os import listdir, remove, path
from django.conf import settings
# from keras.backend import clear_session

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
ROOT = path.join(path.dirname(BASE_DIR))


# Create your views here.
# class ViewAPI(APIView):

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
        if(request.data['command'] == 'save'):
            print("User wants to save recording to drive.")
            saveFileInDrive()
    return Response({"message": "google post success"})


@api_view(['GET', 'POST'])
def googleCall(request):
    if request.method == 'POST':
        # Save the audio file
        dataDict = request.data
        dataDict = dataDict['audio']
        path = default_storage.save(
            settings.MEDIA_ROOT + "/output.wav", ContentFile(dataDict.read()))

        # Manipulate original audio file
        cf.convertToMono(settings.MEDIA_ROOT + "/output.wav",
                         settings.MEDIA_ROOT + "/output_mono.wav")
        cf.convertToFLAC(settings.MEDIA_ROOT + "/output_mono.wav",
                         settings.MEDIA_ROOT + "/output_mono.flac")

        # Delete original file
        if default_storage.exists(path):
            default_storage.delete(path)

        # Volume Tracking
        V, pauses = cf.volumeAnalysis(
            settings.MEDIA_ROOT + "/output_mono.wav", 100)

        volume = np.zeros((V.shape[0], 2))
        for i in range(volume.shape[0]):
            volume[i, :] = np.asarray([i, V[i]])

        # Get and format response from google cloud api
        res = googleApiCall(settings.MEDIA_ROOT +
                            "/Simon_Sinek_30.flac", pauses)

        if not res == "Empty Response":
            transcript = str(res[0])
            sentences = str(res[3])
            confidence = float(res[1])
            confidence = round(confidence, 4)*100
            sentencesEnd = res[2]
            resData = mostCommon(transcript)
            indexArray = str(resData[0])
            corpus = str(resData[1])
            tok = resData[2]
            list_of_sentences = res[3]
            listSyn = str(resData[3])
            filler = resData[4]
            fillerCount = resData[5]
            print("filler count:     ", fillerCount)
            list_of_sentences = res[3]
            wordsperminute = res[4]
            sentimentArray = sentimentCall(list_of_sentences)
            average_wpm = res[5]
            total_words = res[6]
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
            list_of_sentences = "empty response"
            wordsperminute = "empty response"
            average_wpm = "empty response"
            total_words = "rempty response"

        # Pitch Tracking
        # f0 = cf.pitchTrackingYIN(settings.MEDIA_ROOT + "/output_mono.wav",
        #                          freq_range=(40, 300),
        #                          threshold=0.1,
        #                          timestep=0.25,
        #                          Fc=1e3)
        # f1 = cf.pitchTrackingYIN(settings.MEDIA_ROOT + "/output_mono.wav",
        #                          freq_range=(300, 600),
        #                          threshold=0.1,
        #                          timestep=0.25,
        #                          Fc=1e3)
        # pitch = np.zeros((f0.shape[0], 3))
        # for i in range(pitch.shape[0]):
        #     pitch[i, :] = np.asarray([i, f0[i], f1[i]])

        # Adjust wpm

        # Filler word detection
#        global graph
       # with settings.GRAPH.as_default():
        # str(cf.detectFillers(settings.MEDIA_ROOT, settings.MODEL, "/output_mono.wav"))
        filler_count = 0
#            clear_session()

#        #Get rid of files
#        if default_storage.exists(path):
#            default_storage.delete(path)
        # res = '''{"Transcript": "my problem has been resolved thanks to colleague Brian call at text up the problem is that before the PIP I try to install Google Cloud manually by downloading the source and running setup talk to you why","Confidence": 0.931040287018,"Words": [["my", 0.0, 1.2],["problem", 1.2, 1.7],["has", 1.7, 1.9],["been", 1.9, 2.0],["resolved", 2.0, 2.6],["thanks", 2.6, 3.0],["to", 3.0, 3.2],["colleague", 3.2, 3.7],["Brian", 3.7, 4.1],["call", 4.1, 4.5],["at", 4.5, 4.9],["text", 4.9, 5.4],["up", 5.4, 5.6],["the", 5.6, 6.7],["problem", 6.7, 7.0],["is", 7.0, 7.6],["that", 7.6, 8.2],["before", 8.2, 8.6],["the", 8.6, 9.1],["PIP", 9.1, 9.4],["I", 9.4, 10.1],["try", 10.1, 10.6],["to", 10.6, 10.9],["install", 10.9, 11.1],["Google", 11.1, 11.6],	["Cloud", 11.6, 12.0],["manually", 12.0, 12.7],["by", 12.7, 12.9],["downloading", 12.9, 13.5],["the", 13.5, 13.7],["source", 13.7, 14.1],	["and", 14.1, 14.3],["running", 14.3, 14.8],["setup", 14.8, 15.8],["talk", 15.8, 16.1],	["to", 16.1, 16.2], ["you", 16.2, 16.3],["why", 16.3, 16.5]]}'''
        # print(res)
<<<<<<< HEAD

        # stichImagesCall(sentencesEnd)
        # emotionImages = AzureCall()

=======
        # stichImagesCall(sentencesEnd)
        # emotionImages = AzureCall()
        #
>>>>>>> d3adaa5f145fab382a9af81052501ffa749bcfab
        # SadnessI = emotionImages[0]
        # JoyI = emotionImages[1]
        # AngerI = emotionImages[2]
        # DisgustI = emotionImages[3]
        # FearI = emotionImages[4]
        # AvgI = emotionImages[5]

        emotionText = watsontoneCall(list_of_sentences)

        SadnessT = emotionText[0]
        JoyT = emotionText[1]
        AngerT = emotionText[2]
        DisgustT = emotionText[3]
        FearT = emotionText[4]
        AvgT = emotionText[5]

<<<<<<< HEAD
        # print(len(SadnessT), len(SadnessI))
        # print(len(JoyT), len(JoyI))
        # print(len(AngerT), len(AngerI))
        # print(len(DisgustT), len(DisgustI))
        # print(len(FearT), len(FearI))

        # SadnessC = np.corrcoef(SadnessI, SadnessT)[0][1]
        # JoyC = np.corrcoef(JoyI, JoyT)[0][1]
        # AngerC = np.corrcoef(AngerI, AngerT)[0][1]
        # DisgustC = np.corrcoef(DisgustI, DisgustT)[0][1]
        # FearC = np.corrcoef(FearI, FearT)[0][1]
=======
        # print(len(SadnessT),len(SadnessI))
        # print(len(JoyT),len(JoyI))
        # print(len(AngerT),len(AngerI))
        # print(len(DisgustT),len(DisgustI))
        # print(len(FearT),len(FearI))

        # SadnessC = np.corrcoef(SadnessI,SadnessT)[0][1]
        # JoyC = np.corrcoef(JoyI,JoyT)[0][1]
        # AngerC = np.corrcoef(AngerI, AngerT)[0][1]
        # DisgustC = np.corrcoef(DisgustI, DisgustT)[0][1]
        # FearC = np.corrcoef(FearI, FearT)[0][1]
        #
        # print("Sadness", SadnessC, SadnessI, SadnessT)
        # print("JoyC", JoyC, JoyI, JoyT)
        # print("AngerC", AngerC, AngerI, AngerT)
        # print("DisgustC", DisgustC, DisgustI, DisgustT)
        # print("FearC", FearC, FearI, FearT)
>>>>>>> d3adaa5f145fab382a9af81052501ffa749bcfab

        # print("Sadness", SadnessC, SadnessI, SadnessT)
        # print("JoyC", JoyC, JoyI, JoyT)
        # print("AngerC", AngerC, AngerI, AngerT)
        # print("DisgustC", DisgustC, DisgustI, DisgustT)
        # print("FearC", FearC, FearI, FearT)

        return Response({
            "transcript": transcript,
            "sentences": sentences,
            "confidence": confidence,
            "indexArray": indexArray,
            "corpus": corpus,
            "tok": tok,
            "listSyn": listSyn,
            # "pitch": pitch,
            "filler_count": filler_count,
            "volume": volume,
            "list_of_sentences": list_of_sentences,
            "wordsperminute": wordsperminute,
            "average_wpm": average_wpm,
            "total_words": total_words,
<<<<<<< HEAD
            "pauses": pauses#,
            # "imagesSadness": SadnessI,
            # "imagesJoy": JoyI,
            # "imagesAnger": AngerI,
            # "imagesDisgust": DisgustI,
            # "imagesFear": FearI,
            # "imagesAvg": AvgI
=======
            "pauses": pauses,
            # "SadnessI": SadnessI,
            # "JoyI": JoyI,
            # "AngerI": AngerI,
            # "DisgustI": DisgustI,
            # "FearI": FearI,
            # "AvgI": AvgI,
            "SadnessT": SadnessT,
            "JoyT": JoyT,
            "AngerT": AngerT,
            "DisgustT": DisgustT,
            "FearT": FearT,
            "AvgT": AvgT,
            "fillerCount": fillerCount,
            "EndTime": sentencesEnd[len(sentencesEnd)-1],
            "sentencesEnd": sentencesEnd,
            "V": V
>>>>>>> d3adaa5f145fab382a9af81052501ffa749bcfab

        })
    return Response({"message": "Hello, world!"})



    # def imagefoldertest():
        
    #     temp = settings.IMAGE_ROOT

    #     while(default_storage.exists(temp)):
    #         default_storage.delete(temp)
number = 0
@api_view(['POST'])
def screenshotCall(request):
    global number

    if request.method == 'POST':
        # Save the audio file
        dataDict=request.data
        dataDict=dataDict['image']
        number=number+1
        dataDict.seek(22)   # skip the first 22 bytes
        rest=dataDict.read()
        decode=base64.standard_b64decode(rest)
        path=default_storage.save(
            settings.IMAGE_ROOT + "/" + str(number)+".png", ContentFile(decode))

    return Response({"message": "image saved"})

