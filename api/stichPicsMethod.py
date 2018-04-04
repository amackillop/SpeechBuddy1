import sys
from PIL import Image
from random import *
import os
from django.core.files.storage import default_storage


def pick4oflist(listofImages):
    NewlistofImages = []
    while len(NewlistofImages) < 4:
        pick = randint(0, len(listofImages) - 1)
        if pick not in NewlistofImages:
            NewlistofImages.append(listofImages[pick])
    return NewlistofImages


def stichImagesCall(sentencesEnd):
    sentencesEnd[len(sentencesEnd)-2] = sentencesEnd[len(sentencesEnd)-1]
    sentencesEnd = sentencesEnd[:len(sentencesEnd)-1]
    # print("Sentences: ", sentencesEnd)
    start = 0
    folder = '/home/sanghs3/Capstone/SpeechBuddy1/audio/image/'
    SentenceofImages = [0]*len(sentencesEnd)
    listofImages = os.listdir(folder)
    for i in range(len(sentencesEnd)):
        end = int(sentencesEnd[i])
        temp = []
        for j in range(len(listofImages)):
            #print(listofImages[j], int(listofImages[j][0:len(listofImages[j])-4]),int(listofImages[j][0:len(listofImages[j])-4]) <= end, end, int(listofImages[j][:len(listofImages[j])-4]) > start, start)
            if int(listofImages[j][:len(listofImages[j])-4]) <= end and int(listofImages[j][:len(listofImages[j])-4]) > start:
                temp.append(folder + listofImages[j])
        start = end
        if len(temp) > 4:
            temp = pick4oflist(temp)
        # print(temp, i)
        creatImage(temp, i)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                default_storage.delete(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def creatImage(listofImages,counter):
    #print(listofImages)
    stringFile = ""
    for i in range(len(listofImages)):
        stringFile = listofImages[i][listofImages[i].index("/image") + 7:len(listofImages[i])-3] +"-" + stringFile

    # folder = '/home/sanghs3/Capstone/SpeechBuddy1/audio/image/'
    # listofImages = os.listdir(folder)
    # for i in range(len(listofImages)):
    #     listofImages[i] = folder + listofImages[i]
    #
    # print(listofImages)

    # listofImages = ['/home/sanghs3/PycharmProjects/PicStitch/img/temp1.png',
    #         '/home/sanghs3/PycharmProjects/PicStitch/img/temp2.png',
    #         '/home/sanghs3/PycharmProjects/PicStitch/img/temp3.png',
    #         '/home/sanghs3/PycharmProjects/PicStitch/img/temp4.png']

    # if len(listofImages) > 4:
    #     listofImages = pick4oflist(listofImages)

    images = map(Image.open, listofImages)

    widths, heights = zip(*(i.size for i in images))

    if len(listofImages) == 1:
        total_width = int(max(widths))
        total_hieght = int(max(heights))

        # print(total_width, total_hieght)
        new_im = Image.new('RGB', (total_width, total_hieght))
        temp = Image.open(listofImages[0])
        new_im.paste(temp, (0, 0))

    x_offset = 0

    if len(listofImages) == 2:
        total_width = int(sum(widths))
        total_hieght = int(max(heights))

        # print(total_width, total_hieght)
        new_im = Image.new('RGB', (total_width, total_hieght))
        for i in range(2):
            temp = Image.open(listofImages[i])
            new_im.paste(temp, (x_offset, 0))
            x_offset += temp.size[0]

    if len(listofImages) >= 3:
        total_width = int(max(widths) * 2)
        total_hieght = int(max(heights) * 2)

        #print(total_width, total_hieght)
        new_im = Image.new('RGB', (total_width, total_hieght))
        for i in range(2):
            temp = Image.open(listofImages[i])
            new_im.paste(temp, (x_offset, 0))
            x_offset += temp.size[0]

        x_offset = 0
        y_offset = int(temp.size[1])
        if len(listofImages) == 3:
            for i in range(1):
                temp = Image.open(listofImages[2])
                new_im.paste(temp, (x_offset, y_offset))
                x_offset += temp.size[0]
        else:
            for i in range(2):
                temp = Image.open(listofImages[i+2])
                new_im.paste(temp, (x_offset, y_offset))
                x_offset += temp.size[0]

    # new_im.save('/home/sanghs3/Capstone/SpeechBuddy1/audio/finalImages/' + stringFile + '.jpg')
    # new_im.save('C:/Users/Gladiator/Desktop/Capestone/Updated UI/SpeechBuddy1/audio/finalimages/' + str(counter) + '.jpg')
    # new_im.save('/home/sanghs3/Capstone/SpeechBuddy1/audio/finalImages/' + stringFile + '.jpg')
    new_im.save('/home/sanghs3/Capstone/SpeechBuddy1/audio/finalImages/' + str(counter) + '.jpg')
