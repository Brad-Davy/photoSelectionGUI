from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

def check_and_create_credentials():

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    ############################################################
    # Deal with the case where the credentials have not been set
    ############################################################ 

    if creds == None or creds.valid == None:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def download_images():

    creds = check_and_create_credentials()

    ############################################################ 
    # Create the service and list all files
    ############################################################ 

    folder_id='1f2yYNOfnpNtXnlFSvjDJ4DwIq551FD1f'
    query = "'{}' in parents and trashed=false".format(folder_id)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q=query).execute()
    items = results.get('files', [])

    ########################################################### 
    # Extract all image ids and image names
    ########################################################### 

    image_Ids = []
    image_names = []

    for item in items:
        if item['mimeType'] == 'image/jpeg':
            image_Ids.append(item['id'])
            image_names.append(item['name'])


    print('There are {} files to download.'.format(len(image_names)))

    ########################################################### 
    # Go through each file name and download each to local storage
    ########################################################### 

    for idx, image_name in enumerate(image_names):

        file_path = os.path.join(os.getcwd()+'/temporary_image_directory', image_name) 
        fh = io.FileIO(file_path, 'wb')

        request = service.files().get_media(fileId=image_Ids[idx])
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download {}% complete. {}/{}".format(int(status.progress() * 100), idx, len(image_names)))

def upload_images():

    creds = check_and_create_credentials()
    service = build('drive', 'v3', credentials=creds)
    folder_id = '1cIg47pxY1I2d8NqbbDEhGg64uAt8oS5L'

    all_file_names = os.listdir('temporary_image_directory')
    print('{} files to upload.'.format(len(all_file_names)))

    for idx, file_name in enumerate(all_file_names):
        media = MediaFileUpload('temporary_image_directory/'+file_name, mimetype='image/jpeg')
        file_metadata = {'name': file_name.split('/')[-1], 'parents': [folder_id]}
        file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
        print('Upload 100% complete. {}/{}'.format(idx, len(all_file_names)))