from ultralytics import YOLO
import os
import cv2 
import matplotlib.pyplot as plt 

#####################################
## Declarations 
#####################################
model = YOLO('yolov8n.pt')
tensor_dict = {}
zero_filenames = []  

class IP:

    def __init__(self):
        self.PATH_TO_IMAGES = ""
        self.IMAGES_TO_REMOVE = []
        self.IMAGES_HAVE_BEEN_REMOVED = False

    def setImagePath(self, imagePath):
        self.PATH_TO_IMAGES = imagePath

    def getImagePath(self, imagePath):
        return self.PATH_TO_IMAGES

    def __delattr__(self, name: str) -> None:
        pass

    def determineIfImageContainsPerson(self, imagePath):
            imagePath = os.path.join(self.PATH_TO_IMAGES, imagePath)
            print(imagePath)
            result = model(imagePath)
            for r in result:
                tensor = str(r.boxes.cls)
                if tensor not in tensor_dict:
                    tensor_dict[tensor] = [imagePath]  # Initialize list for the tensor if not already present
                else:
                    tensor_dict[tensor].append(imagePath)  # Append filename to the existing list
                if '0.' in tensor:  # Check if tensor does not have element 0
                    return imagePath

    def determineImagesWithPerson(self):

        if os.path.exists(self.PATH_TO_IMAGES):
            pass
        else:
            print('Cant find images at: {} :, please check path is correct.'.format(self.PATH_TO_IMAGES))
            return 0 
        
        imageFileNames = os.listdir(self.PATH_TO_IMAGES)

        for fileName in imageFileNames:

            if self.determineIfImageContainsPerson(fileName) is not None:
                self.IMAGES_TO_REMOVE.append(self.determineIfImageContainsPerson(fileName))
        
    def removeImages(self):

        if len(self.IMAGES_TO_REMOVE) == 0:
            print('Make sure the images to be removed have been set.')
            return 
        
        for images in self.IMAGES_TO_REMOVE:
            os.remove(images)

        self.IMAGES_HAVE_BEEN_REMOVED = True


    def blurImageHelper(self, faceData, image):

        for (x, y, w, h) in faceData: 

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            roi = image[y:y+h, x:x+w] 
            roi = cv2.GaussianBlur(roi, (23, 23), 30) 
            image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi 

        return image

    def blurImages(self):

        if self.IMAGES_HAVE_BEEN_REMOVED == False:
            print('Please remove images before trying to blur the remaining images.')
            return
        
        for images in os.listdir(self.PATH_TO_IMAGES):
            imagePath = os.path.join(self.PATH_TO_IMAGES, images)
            imageCv2 = cv2.imread(imagePath)
            imageCv2Converted = cv2.cvtColor(imageCv2, cv2.COLOR_BGR2RGB) 
            faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') 
            
            if faceDetect.empty():
                print("Error loading cascade classifier")
                return
            
            faceData = faceDetect.detectMultiScale(imageCv2Converted, 1.3, 5)  
            blurredImage = self.blurImageHelper(faceData, imageCv2Converted)
            cv2.imwrite(imagePath, blurredImage)
