from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings

# def authenticateToken(token):
# try:
#     # Specify the CLIENT_ID of the app that accesses the backend:
#     idinfo = id_token.verify_oauth2_token(token, requests.Request())

#     # Or, if multiple clients access the backend server:
#     # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#     # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#     #     raise ValueError('Could not verify audience.')

#     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#         raise ValueError('Wrong issuer.')

#     # If auth request is from a G Suite domain:
#     # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#     #     raise ValueError('Wrong hosted domain.')

#     # ID token is valid. Get the user's Google Account ID from the decoded token.
#     userid = idinfo['sub']
#     print('Token valid.')
# except ValueError:
#     # Invalid token
#     pass


def saveFileInDrive():
    gauth = GoogleAuth()
    # gauth.CommandLineAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    FOLDER_EXITS = 0

    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if(file1['title'] == 'SpeechBuddy'):
            FOLDER_EXITS = 1
            folderid = file1['id']
            break;
        
    if (FOLDER_EXITS == 0):
        folder_metadata = {'title': 'SpeechBuddy', 'mimeType': 'application/vnd.google-apps.folder'}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        # Get folder info and print to screen
        foldertitle = folder['title']
        folderid = folder['id']
        print('title: %s, id: %s' % (foldertitle, folderid))

    # Upload file to folder
    file = drive.CreateFile(
        {"parents": [{"kind": "drive#fileLink", "id": folderid}]})
    file.SetContentFile(settings.MEDIA_ROOT + "/output_mono.wav")
    file.Upload()
