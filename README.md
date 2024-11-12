![Photo_Selection_GUI (1)](https://github.com/user-attachments/assets/1497bae7-fbed-4449-b5ee-0793184fc201)

# Overview
A graphical user interface developed in Python to download images from a Google Drive, process them and then re-upload them to another Google Drive.

# Install
- > git clone git@github.com:Brad-Davy/photoSelectionGUI.git
- > python3 -m venv env
- > source env/activate/bin
- > pip3 install -r requirements.txt

# Usage
Run the app by executing 
> python3 app.py

The following window should open. 

![Screenshot 2024-10-17 at 12 12 16](https://github.com/user-attachments/assets/5885c496-54bc-4e7f-a149-af4cb09f2582)

## Authentication
To use the GUI a Google account which has access to the required drives must be used. On this Google account a "Google Cloud Project" must be set up. The following link shows how this is done: https://medium.com/the-team-of-future-learning/integrating-google-drive-api-with-python-a-step-by-step-guide-7811fcd16c44. Once this is complete the credentials.json file must be stored within the working directory. 

## Example use case
First, select the 'Download Images' button. If the account has already been authenticated then this will download all images from the selected Google Drive. If not then the following screen will open.

![image](https://github.com/user-attachments/assets/84044878-fd18-47d1-af56-aaf07da9598f)

After selecting the Google account, a login screen will open prompting the user to enter there login details.

![image](https://github.com/user-attachments/assets/f1a80bef-7190-43eb-b0d2-6e4e8c5a9cf7)

Then this screen will appear,

![image](https://github.com/user-attachments/assets/3775de9e-e157-4760-bf37-7d363f58f259)

prompting the user to allow the Python code to access the Google drives. Finally, when the account has been authenticated this final screen will be displayed.

![image](https://github.com/user-attachments/assets/1974faa7-d2a8-4fa2-a145-1dd29acbeb41)

Now select the 'Remove Images' button. This will run the YOLO algorithm on each image. If a person is detected, the image is deleted.

Now select the 'Blur Images' button. This will use OpenCV to blur the remaining images, which may contain a person.

Finally, select the 'Upload Images' button. This uploads the processed images to a different selected Google Drive. 

# Contributors

Bradley Davy 
