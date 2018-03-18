# Instructions Manual

## Initial Install
A brief overview of how to get the server running on your computer. These are just rough notes and they may be missing a step so add to this if I have missed anything.

Note: You must have Google Cloud Speech to Text API credentials. 

### Here are the steps
1. Clone the repo or download the zip file and extract it wherever you want. This will be referenced as PATH from now on.

2. Open a cmd line and install the following packages if you do not have them already:

Use these condensed pip installs to download all requirements:
```
pip install django djangorestframework nltk google SpeechRecognition numpy scipy wave matplotlib keras h5py
pip install --upgrade google-cloud-speech
pip install --update tensorflow 
```
Or select the requirements individually from the ones below:
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
You will also need to install Keras and tensorflow. If ```pip install tensorflow``` does not install tensorflow correctly, download Anaconda and run ```conda install tensorflow```. You should only have to do this once.

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

### Good Luck!

## Adding Features
Follow these steps to turn your python functions into web features

1. Open the recorder/templates/recorder/html/recorder.html file and add some divs to the front end for your new feature.

2. In the static/js folder, create a new javascript file to manipulate your created divs with the information that will come from your python function.

3. In this file, add a function with the same name as the file.
```
function name_of_your_js_file(data) {
  ...
}
```
4. Open a git bash in your project directory and add this new file to git so that it can be tracked.
  ```
  git add static/js/"name_of_your_js_file".js
  ```
5. Go back to the recorder.html file and add a new <script> tag at the bottom to include your new javascript function.
  ```
  <script src="../static/js/"name_of_your_js_file".js"></script>
  ```
6. Open the static/js/recorderWeb.js file and locate the AJAX call. Add your new js function here in the *success* response.
  ```
  $.ajax({
      ...
      success: function(data) {
          ...
					name_of_your_js_file(data);
      }
  });
  ```
7. Go to the api/ folder and copy/paste your python function file here if needed.
  
8. Open the api/views.py file and import your new python function.
  ```
  from api.python_file_name import python_function
  ```
9. At the bottom of views.py you will find the googleCall function (We need to change this). This is where you will call your new python function and apply any python logic if needed. Ex.
  ```
  var = python_function()
  ```
10. To send this new information to the front end, edit the JSON response of the return statement of this googleCall function. Give the var that you are trying to send a property name as a string. 
  ```
  Response({..., "property_name": var})
  ```
11. If you go back to the javascript file that you made in step 2, you can now access this information by using data.property_name in the js function.

  
