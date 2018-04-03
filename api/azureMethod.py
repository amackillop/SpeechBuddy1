import requests
from api.keys import ApiKeys
import json
import os

subscription_key = ApiKeys['subscriptionkey']


# emotion_recognition_url = " https://westus.api.cognitive.microsoft.com/face/v1.0/recognize"
# headers = {'Ocp-Apim-Subscription-Key': subscription_key }
# image_url = 'https://how-old.net/Images/faces2/main007.jpg'
# #image_data = open(image_path, "rb").read()
#
#
# import requests
#
# params = {
#     'returnFaceId': 'true',
#     'returnFaceLandmarks': 'false',
#     'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
# }
#
# response = requests.post(emotion_recognition_url, params=params, headers=headers, json={"url": image_url})
# faces = response.json()
# print faces
def AzureCall():
    folder = '/home/sanghs3/Capstone/SpeechBuddy1/audio/finalImages/'
    listofImages = sorted(os.listdir(folder))
    Sadness = [0] * len(listofImages)
    Joy = [0] * len(listofImages)
    Anger = [0] * len(listofImages)
    Disgust = [0] * len(listofImages)
    Fear = [0] * len(listofImages)
    for i in range(len(listofImages)):
        temp = AzureImageCall(folder + listofImages[i])
        print(temp,listofImages[i], i)
        Sadness[i] = round(temp[0],5)
        Joy[i] = round(temp[1],5)
        Anger[i] = round(temp[2],5)
        Disgust[i] = round(temp[3],5)
        Fear[i] = round(temp[4],5)
    print("Sadness: ", Sadness)
    print("Joy: ", Joy)
    print("Anger: ", Anger)
    print("Disgust: ", Disgust)
    print("Fear: ", Fear)

    SadnessNum = sum(Sadness)/len(Sadness)
    JoyNum = sum(Joy)/len(Joy)
    AngerNum = sum(Anger)/len(Anger)
    DisgustNum = sum(Disgust)/len(Disgust)
    FearNum = sum(Fear)/len(Fear)

    EmotionalAvg = [SadnessNum, JoyNum, AngerNum, DisgustNum,FearNum]
    return [Sadness,Joy,Anger, Disgust, Fear, EmotionalAvg]


def AzureImageCall(image_path):
    emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=emotion"

    image_data = open(image_path, "rb").read()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
    response = requests.post(emotion_recognition_url, headers=headers, data=image_data)
    # response.raise_for_status()
    # analysis = response.json()
    result = json.loads(response.content.decode("utf-8"))
    # print(result)

    Sadness = [0] * 4
    Joy = [0] * 4
    Anger = [0] * 4
    Disgust = [0] * 4
    Fear = [0] * 4

    SadnessNum = 0
    JoyNum = 0
    AngerNum = 0
    DisgustNum = 0
    FearNum = 0

    for z in range(len(result)):
        # print(result[i]['faceAttributes']['emotion']['sadness'])
        SadnessNum = SadnessNum + result[z]['faceAttributes']['emotion']['sadness']
        JoyNum = JoyNum + result[z]['faceAttributes']['emotion']['happiness']
        AngerNum = AngerNum + result[z]['faceAttributes']['emotion']['anger']
        DisgustNum = DisgustNum + result[z]['faceAttributes']['emotion']['disgust']
        FearNum = FearNum + result[z]['faceAttributes']['emotion']['fear']
    SadnessNum = SadnessNum / len(result)
    JoyNum = JoyNum / len(result)
    AngerNum = AngerNum / len(result)
    DisgustNum = DisgustNum / len(result)
    FearNum = FearNum / len(result)

    return [SadnessNum, JoyNum, AngerNum,DisgustNum, FearNum]
