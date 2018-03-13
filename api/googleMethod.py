import io
import os


#Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave

def googleApiCall(path):
#    path = "C:/Users/Austin/Desktop/school/capstone/speechbuddy/audio/output_mono.flac"
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = path #'/home/sanghs3/Capstone/umm.flac'


    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US',
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    try:
        response = formatResponse(response)
    except:
        return "Empty Response"
#    print(response)
    return response

def formatResponse(response):
    stringData="{"

    for result in response.results:
        alternative = result.alternatives[0]
        stringData = stringData + '"Transcript":"' + str(alternative.transcript.encode('ascii')) + '",'
        stringData = stringData + '"Confidence":' + str(alternative.confidence) + '}'
        movingWindow=[]

        # Holds duration of each word from response
        wordslist = []
        # Holds duration of each sentence based on a 15 words/sentence assumption
        sentence_duration= []
    
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            wordslist.append((end_time.seconds + end_time.nanos * 1e-9) - ( start_time.seconds + start_time.nanos * 1e-9))
            print('Word: {}, start_time: {}, end_time: {}, duration: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9, 
                (end_time.seconds + end_time.nanos * 1e-9) - ( start_time.seconds + start_time.nanos * 1e-9)
                ))

        #calculate total duration per 15 words
        time_per_sentence = 0
        for i in range(0,len(wordslist)):

            if (len(wordslist)<15):
                print('less than 15 words in the Speech')

            elif( i % 15 != 0 or i == 0):
                time_per_sentence = time_per_sentence + wordslist[i]
                
                
            else:
                # print(time_per_sentence)
                sentence_duration.append(time_per_sentence)
                time_per_sentence = 0


        print("\n\n ************************************************** Printing calculations [for testing] **************************************************")
        print("\nTotal time taken to complete each sentence:")
        print(sentence_duration)
        # add more calcs to print here for testing...
        print("\n ************************************************** Done Printing calculations [for testing] **********************************************\n\n")
    return [alternative.transcript.encode('ascii'),alternative.confidence, movingWindow]