from __future__ import print_function
import json
from watson_developer_cloud import ToneAnalyzerV3
from keys import ApiKeys

tone_analyzer = ToneAnalyzerV3(
    username=ApiKeys['username'],
    password=ApiKeys['password'],
    version=ApiKeys['version'])


# print("\ntone() example 1:\n")
# print(json.dumps(tone_analyzer.tone(tone_input='I am very happy. It is a good day.',
#                                    content_type="text/plain", sentences=False, tones="social"), indent=2))


def watsontoneCall(sentencesLIST):
    sentencesStr = ""
    for i in range(len(sentencesLIST)):
        sentencesStr = sentencesStr + " " + sentencesLIST[i] + "."
    print(sentencesStr)
    social = json.dumps(
        tone_analyzer.tone(tone_input=sentencesStr, content_type="text/plain", sentences=True, tones="social"),
        indent=2)
    emotionLIST = json.dumps(
        tone_analyzer.tone(tone_input=sentencesStr, content_type="text/plain", sentences=True, tones="emotion"),
        indent=2)

    # print(emotion)
    arrayEmo = json.loads(emotionLIST)
    emotions = arrayEmo['document_tone']['tone_categories'][0]['tones']
    EmotionalAVG = [0] * 5
    Sadness = [0] * 5
    Joy = [0] * 5
    Anger = [0] * 5
    Disgust = [0] * 5
    Fear = [0] * 5

    for i in range(len(emotions)):
        # print(emotions[i])
        if emotions[i]['tone_id'] == 'sadness':
            EmotionalAVG[0] = emotions[i]['score']
        if emotions[i]['tone_id'] == 'joy':
            EmotionalAVG[1] = emotions[i]['score']
        if emotions[i]['tone_id'] == 'anger':
            EmotionalAVG[2] = emotions[i]['score']
        if emotions[i]['tone_id'] == 'disgust':
            EmotionalAVG[3] = emotions[i]['score']
        if emotions[i]['tone_id'] == 'fear':
            EmotionalAVG[4] = emotions[i]['score']

    emotionsOrder = []
    for i in range(len(arrayEmo['sentences_tone'])):

        # print(arrayEmo['sentences_tone'][i])
        emotions = arrayEmo['sentences_tone'][i]['tone_categories'][0]['tones']
        for j in range(len(emotions)):

            if emotions[j]['tone_id'] == 'sadness':
                Sadness[arrayEmo['sentences_tone'][i]['sentence_id']] = emotions[j]['score']
            if emotions[j]['tone_id'] == 'joy':
                Joy[arrayEmo['sentences_tone'][i]['sentence_id']] = emotions[j]['score']
            if emotions[j]['tone_id'] == 'anger':
                Anger[arrayEmo['sentences_tone'][i]['sentence_id']] = emotions[j]['score']
            if emotions[j]['tone_id'] == 'disgust':
                Disgust[arrayEmo['sentences_tone'][i]['sentence_id']] = emotions[j]['score']
            if emotions[j]['tone_id'] == 'fear':
                Fear[arrayEmo['sentences_tone'][i]['sentence_id']] = emotions[j]['score']

    return [EmotionalAVG, Sadness, Joy, Anger, Fear,social]


arraylist = ['Here, statements may be a single statement or a block of statements',
             'The condition may be any expression, and true is any non-zero value',
             'I am having an amazing day because I had the best food ever',
             'I just missed my exam and now I am going to fail and drop out of school',
             'I just got an interview for at EY']

arrayEmo = watsontoneCall(arraylist)

# print(arrayEmo[1])

# print(arrayEmo['document_tone']['tone_categories'][0]['tones'])
