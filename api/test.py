import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = '/home/sanghs3/Capstone/SpeechBuddy/speechbuddy/audio/output.flac'

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

stringData="{";

for result in response.results:
        alternative = result.alternatives[0]
        stringData= stringData + '"Transcript":"'+ alternative.transcript.encode('ascii') +'",'
        stringData= stringData + '"Confidence":'+ str(alternative.confidence) +','
	    stringData= stringData +  '"Words":['
        index = 1
        length = len (alternative.words)
        for word_info in alternative.words:
            word = word_info.word.encode('ascii')
            start_time = str(word_info.start_time.seconds + word_info.start_time.nanos * 1e-9)
            end_time = str(word_info.end_time.seconds + word_info.end_time.nanos * 1e-9)
            stringData = stringData + '["' + word + '",' + start_time + ","+ end_time + "]"
	        print index, length
            if index == length:
                stringData = stringData + "]}"
            else:
                stringData = stringData + ","
	        index = index + 1
print stringData