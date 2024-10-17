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

First, select the 'Download Images' button. This will download all images from the selected Google Drive and open the following window.

Now select the 'Remove Images' button. This will run the YOLO algorithm on each image. If a person is detected, the image is deleted.

Now select the 'Blur Images' button. This will use OpenCV to blur the remaining images, which may contain a person.

Finally, select the 'Upload Images' button. This uploads the processed images to a different selected Google Drive. 

# Contributors

Bradley Davy 
