from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

############################################################
# This function checks if the temporary image directory exists
# and if not creates it.
############################################################

def check_if_temporary_image_directory_exists():

    ############################################################
    # Check if the temporary image directrory exists, if not
    # install it.
    ############################################################ 

    if os.path.isdir('temporary_image_directory'):
        return 
    else:
        os.system('mkdir temporary_image_directory')

############################################################
# This function checks if the credentials have been set, if not 
# it will create them and save them to a file called 'token.json' 
# in the current directory.
############################################################

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


############################################################
# This function downloads all images from the google drive
# folder with the id '1f2yYNOfnpNtXnlFSvjDJ4DwIq551FD1f'
# and saves them to the local directory 'temporary_image_directory'.
############################################################

def download_images(folder_id='1f2yYNOfnpNtXnlFSvjDJ4DwIq551FD1f'):

    creds = check_and_create_credentials()
    check_if_temporary_image_directory_exists()

    ############################################################ 
    # Create the service and list all files
    ############################################################ 

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


############################################################
# This function uploads all images from the local directory
# 'temporary_image_directory' to the google drive folder with
# the id '1cIg47pxY1I2d8NqbbDEhGg64uAt8oS5L'.
############################################################

def upload_images(folder_id='1cIg47pxY1I2d8NqbbDEhGg64uAt8oS5L'):

    if os.path.isdir('temporary_image_directory'):
        creds = check_and_create_credentials()
        service = build('drive', 'v3', credentials=creds)

        all_file_names = os.listdir('temporary_image_directory')
        print('{} files to upload.'.format(len(all_file_names)))

        for idx, file_name in enumerate(all_file_names):
            media = MediaFileUpload('temporary_image_directory/'+file_name, mimetype='image/jpeg')
            file_metadata = {'name': file_name.split('/')[-1], 'parents': [folder_id]}
            file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
            print('Upload 100% complete. {}/{}'.format(idx, len(all_file_names)))

    else:
        raise Exception('The temporary_image_directory does not exist.')
    

if __name__ == '__main__':
    pass