import io
import os


#Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave

def googleApiCall(path, pauses):
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
        response = formatResponse(response, pauses)
    except:
        return "Empty Response"
#    print(response)
    return response

def formatResponse(response, pauses):

    stringData="{"

    for result in response.results:
        alternative = result.alternatives[0]
        stringData = stringData + '"Transcript":"' + str(alternative.transcript.encode('ascii')) + '",'
        stringData = stringData + '"Confidence":' + str(alternative.confidence) + '}'

        # Holds duration of each word from response
        wordslist = []
        # Holds duration of each sentence based on a 15 words/sentence assumption
        sentence_duration= []
        wordsperminute=[]
        strings_of_words=[]
        temp_string = ""
        list_of_sentences=[]

         

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
#            for pause in pauses:
#                if start_time < pause[0] and end_time > pause[0]:
#                    end_time -= pause[1]
            wordslist.append((end_time.seconds + end_time.nanos * 1e-9) - ( start_time.seconds + start_time.nanos * 1e-9))

        #alternate way to get the words in the list
        for word_info in alternative.words:
            word = word_info.word
            strings_of_words.append(word)

        #getting the words in 15-word based sentence based list
        for i in range(0,len(strings_of_words)):
            
            if(i==len(strings_of_words)-1):
                temp_string= temp_string + str(strings_of_words[i]) + ' '
                list_of_sentences.append(temp_string)
                

            elif(i % 15 !=0 or i==0):
                temp_string= temp_string + str(strings_of_words[i]) + ' '
               

            elif(i % 15 ==0 or i != 0):
                list_of_sentences.append(temp_string)
                temp_string= ""
                temp_string = temp_string + str(strings_of_words[i]) + ' '
        
        #calculate total duration per 15 words
        time_per_sentence = 0
        time_per_last_sentence=0
        speaking_rate=0
        speaking_rate_last_sentence=0
        for i in range(0,len(wordslist)):

            if (len(wordslist)<15):
                print('less than 15 words in the Speech')

            elif( i % 15 != 0 or i == 0):
                time_per_sentence = time_per_sentence + wordslist[i]
                
            else:
                # print(time_per_sentence)
                sentence_duration.append(time_per_sentence)
                speaking_rate=(60*15)/(time_per_sentence)
                wordsperminute.append(speaking_rate)
                time_per_sentence = 0
                speaking_rate=0

        #taking care of the last few words
        if((len(wordslist)-1) % 15 !=0):  
            for i in range(len(wordslist)-15,len(wordslist)):
                time_per_last_sentence=time_per_last_sentence + wordslist[i]
        
            sentence_duration.append(time_per_last_sentence)
            speaking_rate_last_sentence=(60*15)/(time_per_last_sentence)
            wordsperminute.append(speaking_rate_last_sentence)
            speaking_rate_last_sentence=0

        sentenceEnds=[0] * len(sentence_duration)

        for i in range(len(sentence_duration)):
            if i == 0:
                sentenceEnds[i] = sentence_duration[i]
            else:
                sentenceEnds[i] = round(sentence_duration[i]+sentenceEnds[i-1],2)

        print(sentenceEnds)


        print("\n\n ************************************************** Printing calculations [for testing] **************************************************")
        print("\nTotal time taken to complete each sentence:")
        print (["%0.2f" % i for i in sentence_duration])
        print("\n\n ************************************************** Printing calculations [for testing] **************************************************")
        print("\nWords per Minute based on sentence time:")
        print (["%d" % i for i in wordsperminute])
        print("\n\n ************************************************** Printing calculations [for testing] **************************************************")
        print("\nList of Sentences:")
        print(list_of_sentences)
        print(len(list_of_sentences))
        #print(len(alternative.words))
                # add more calcs to print here for testing...
        print("###############################~~~~~~~LOOK HERE~~~~~~~~~########################")
        print(sentenceEnds, list_of_sentences, wordsperminute)
        print("\n ************************************************** Done Printing calculations [for testing] **********************************************\n\n")
    return [alternative.transcript.encode('ascii'),alternative.confidence, sentenceEnds, list_of_sentences, wordsperminute]
