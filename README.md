# Install Instructions
A brief overview of how to get the server running on your computer. These are just rough notes and they may be missing a step so add to 
this if I have missed anything.

Note: You must have Google Cloud Speech to Text API credentials. 

### Here are the steps
1. Download the zip file and extract it wherever you want. This will be referenced as PATH from now on.
2. Open a cmd line and install the following packages if you do not have them already:
```
pip install django
pip install djangorestframework
pip install nltk
pip install google
pip install SpeechRecognition
pip install --upgrade google-cloud-speech
pip install numpy
pip install scipy
pip install wave
pip install matplotlib
pip install --update tensorflow
pip install keras
pip install h5py
```
You will also need to install Keras and tensorflow

3. Go to the nltkMethod file located in SpeechBuddy-master > api and run the 3 commented out download commands. Recomment them.
```
import nltk
import re
import json
from nltk.corpus import wordnet
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
```
4. Go back to the cmd line and run the following command. Alternatively you can drag the manage.py file into the cmd line 
instead of typing the path.
```
python PATH\SpeechBuddy-master\manage.py collectstatic
```
5. Next run this command to start the server:
```
python PATH\SpeechBuddy-master\manage.py runserver
```

6. Type the URL of the server (something like http://http://127.0.0.1:8000/) into chrome to see the webpage
7. Edit this README with whatever steps that I missed or fixes to other errors that you ran into.

## Good Luck!
