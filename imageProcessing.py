from ultralytics import YOLO
import os

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

    def setImagePath(self, imagePath):
        self.PATH_TO_IMAGES = imagePath

    def getImagePath(self, imagePath):
        return self.PATH_TO_IMAGES

    def __delattr__(self, name: str) -> None:
        pass

    def determineIfImageContainsPerson(self, imagePath):
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
            print('Make sure the images to be removed have been set')
            return 
        
        for images in self.IMAGES_TO_REMOVE:
            filePath = os.path.join(self.PATH_TO_IMAGES, images)
            os.remove(filePath)

    def blurImages(self):

        if len(self.IMAGES_TO_REMOVE) == 0:
            print('Make sure the images to be removed have been set')
            return 
        
        for images in self.IMAGES_TO_REMOVE:
            filePath = os.path.join(self.PATH_TO_IMAGES, images)
            os.remove(filePath)

