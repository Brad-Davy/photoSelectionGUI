import os
from ultralytics import YOLO

# Path to the directory containing images
image_folder = "C:/Users/Olayiwola/Desktop/UoY/Drones/privacy/imagesfolder"

model = YOLO('yolov8n.pt')

tensor_dict = {}
zero_filenames = []  # List to store filenames associated with tensors that do not have element 0

# Iterate over each file in the directory
for filename in os.listdir(image_folder):
    if filename.endswith(".JPG") or filename.endswith(".png"):  # Adjust file extensions as needed
        filepath = os.path.join(image_folder, filename)
        
        # Call your YOLOv8n prediction command here with the filepath
        result = model(filepath)
        
        # Iterate over the detected objects
        for r in result:
            tensor = str(r.boxes.cls)
            if tensor not in tensor_dict:
                tensor_dict[tensor] = [filename]  # Initialize list for the tensor if not already present
            else:
                tensor_dict[tensor].append(filename)  # Append filename to the existing list
            if '0.' in tensor:  # Check if tensor does not have element 0
                zero_filenames.append(filename)  # Add filename to the list

# Print all tensors and associated filenames
print("All Tensors and Associated Filenames:")
for tensor, filenames in tensor_dict.items():
    for filename in filenames:
        print(f"Tensor: {tensor}")
        print(f"Filename: {filename}")
        print()

# Print only tensors that do not have element 0
print("Tensors without Element 0:")
for tensor, filenames in tensor_dict.items():
    if '0.' not in tensor:
        print(f"Tensor: {tensor}")
        print("Filenames:")
        for filename in filenames:
            print(filename)
        print()

# List of filenames associated with tensors that has have element 0
print("Filenames associated with tensors that has element 0:", zero_filenames)





'''
AUTOMATED REMOVAL (PERMANENT DELETE) OF IMAGES/FILES FROM FOLDER
AUTOMATED REMOVAL (PERMANENT DELETE) OF IMAGES/FILES FROM FOLDER
AUTOMATED REMOVAL (PERMANENT DELETE) OF IMAGES/FILES FROM FOLDER
'''

import os

# Path to the folder containing the files
folder_path =  "C:/Users/Olayiwola/Desktop/UoY/Drones/privacy/imagesfolder1"

# List of filenames to delete
file_list = zero_filenames

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    # Check if the filename is in the list of files to delete
    if filename in file_list:
        # Construct the full path to the file
        file_path = os.path.join(folder_path, filename)
        # Delete the file
        os.unlink(file_path) # os.unlink for permanent delete, os.remove for deleting to bin
        print(f"Deleted file: {file_path}")

print("Deletion completed.")

'''
FACE BLURRING
FACE BLURRING
FACE BLURRING
'''

# Importing libraries 
import cv2 
import matplotlib.pyplot as plt 

# A function for plotting the images 


def plotImages(img): 
	plt.imshow(img, cmap="gray") 
	plt.axis('off') 
	plt.style.use('seaborn') 
	plt.show() 


# Reading an image using OpenCV 
# OpenCV reads images by default in BGR format 
image = cv2.imread('my_img.jpg') 

# Converting BGR image into a RGB image 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

# plotting the original image 
plotImages(image) 

face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') 
face_data = face_detect.detectMultiScale(image, 1.3, 5) 

# Draw rectangle around the faces which is our region of interest (ROI) 
for (x, y, w, h) in face_data: 
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
	roi = image[y:y+h, x:x+w] 
	# applying a gaussian blur over this new rectangle area 
	roi = cv2.GaussianBlur(roi, (23, 23), 30) 
	# impose this blurred image on original image to get final image 
	image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi 


# Display the output 
plotImages(image) 