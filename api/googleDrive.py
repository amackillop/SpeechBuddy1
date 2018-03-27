# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive


# gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

# drive = GoogleDrive(gauth)

# folder_metadata = {'title' : 'SpeechBuddy', 'mimeType' : 'application/vnd.google-apps.folder'}
# folder = drive.CreateFile(folder_metadata)
# folder.Upload()

# #Get folder info and print to screen
# foldertitle = folder['title']
# folderid = folder['id']
# print('title: %s, id: %s' % (foldertitle, folderid))

# #Upload file to folder
# file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}]})
# file.SetContentFile('output_mono.wav')
# file.Upload()

# # file1 = drive.CreateFile({'title': 'HelloMoiz.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
# # file1.SetContentString('Hello World!') # Set content of the file from given string.
# # file1.Upload()