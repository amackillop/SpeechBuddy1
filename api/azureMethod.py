import requests
from keys import ApiKeys
print(ApiKeys)
subscription_key = ApiKeys.subscription_key

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

emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=emotion"


#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
image_path = "/home/sanghs3/Capstone/SpeechBuddy/speechbuddy/audio/test.jpg"
image_data = open(image_path, "rb").read()

headers  = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream" }
response = requests.post(emotion_recognition_url, headers=headers, data=image_data)
# response.raise_for_status()
# analysis = response.json()
print(response.content)