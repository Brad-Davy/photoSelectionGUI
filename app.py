import sys
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QProgressDialog
from image_processing import IP  
from image_input_output_google_drive import download_images, upload_images
import threading
import time

############################################################
# This class is used to run the image processing functions in parallel
# with the GUI.
############################################################

class Parallel(QObject):
    progress = pyqtSignal(int)

    def __init__(self, IP):
        super().__init__()
        self.IP = IP

    def work(self):
        print('this worked')
        for i in range(101):
            self.IP.determine_images_with_person()
            self.progress.emit(i)  # Emit progress signal
            time.sleep(0.1)  # Simulate work



############################################################
# This class is the main window of the GUI.
############################################################

class MainWindow(QMainWindow):
    
    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Processing GUI")
        self.setFixedSize(QSize(300, 400))
        self.ui_components()
        self.download_folder_id = ''
        self.upload_folder_id = ''
        self.IP = IP()
        self.yoloThread = Parallel(self.IP)
        self.yoloThread.progress.connect(self.update_progress)
        self.setStyleSheet("background-color: white;")

    ###########################################################
    # This function creates all the buttons and input fields
    # for the GUI.
    ###########################################################

    def ui_components(self): 

        self.download_file_id_input = QLineEdit(self)
        self.download_file_id_input.setPlaceholderText("Enter Download File ID")
        self.download_file_id_input.setGeometry(5, 30, 180, 30)
        self.download_file_id_input.setStyleSheet("color: black;")

        self.upload_file_id_input = QLineEdit(self)
        self.upload_file_id_input.setPlaceholderText("Enter Upload File ID")
        self.upload_file_id_input.setGeometry(5, 80, 180, 30)
        self.upload_file_id_input.setStyleSheet("color: black;")

        button = QPushButton("Download Images", self) 
        button.setGeometry(75, 150, 150, 30)
        button.setStyleSheet("background-color: gray;")
        button.clicked.connect(self.download_image_wrapper)

        button = QPushButton("Set File Id", self) 
        button.setGeometry(193, 37, 100, 70)
        button.setStyleSheet("background-color: green;")
        button.clicked.connect(self.set_file_ids)

        button = QPushButton("Remove Images", self) 
        button.setGeometry(75, 200, 150, 30)
        button.setStyleSheet("background-color: gray;")
        button.clicked.connect(self.remove_images)

        button = QPushButton("Blur Images", self) 
        button.setGeometry(75, 250, 150, 30)
        button.setStyleSheet("background-color: gray;")
        button.clicked.connect(self.blur_images) 

        button = QPushButton("Upload Images", self) 
        button.setGeometry(75, 300, 150, 30)
        button.setStyleSheet("background-color: gray;")
        button.clicked.connect(self.upload_image_wrapper) 
     
    ###########################################################
    # This function sets the image path for the image processing
    # class.
    ###########################################################

    def set_file_ids(self):
        download_file_id_input = self.download_file_id_input.text()
        upload_file_id_input = self.upload_file_id_input.text()
        self.download_folder_id = download_file_id_input
        self.upload_folder_id = upload_file_id_input
        print('{} set as download folder id.'.format(download_file_id_input))
        print('{} set as upload folder id.'.format(upload_file_id_input))

    def set_image_file(self):
        filePath = self.lineEdit.text()
        self.IP.setImagePath(filePath)
        print('Image path has been set too: {}'.format(filePath))

    ###########################################################
    # This function determines the images with a person in them
    # and removes the images without a person.
    ###########################################################

    def determine_images(self):
        progress_dialog = QProgressDialog("Task in progress...", "Cancel", 0, 100, self)
        progress_dialog.setWindowTitle("Progress")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)

    def start_task(self):
        # Step 4: Create and configure QProgressDialog
        self.progress_dialog = QProgressDialog("Task in progress...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Progress")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)

        # Start worker thread
        self.thread = threading.Thread(target=self.yoloThread.work)
        self.thread.start()

        # Use a QTimer to periodically check if the task is complete
        self.check_completion_timer = QTimer()
        self.check_completion_timer.timeout.connect(self.check_completion)
        self.check_completion_timer.start(100)  # Check every 100 milliseconds


    def download_image_wrapper(self):
        download_images(self.download_folder_id)

    def upload_image_wrapper(self):
        upload_images(self.upload_folder_id)

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def check_completion(self):
        if not self.thread.is_alive():
            self.check_completion_timer.stop()
            self.progress_dialog.setValue(100)
            self.progress_dialog.setLabelText("Task completed!")
            QTimer.singleShot(500, self.progress_dialog.close)  # Close after 500 milliseconds
            print("Task completed!")

    ###########################################################
    # This function removes the images with a person.
    ###########################################################

    def remove_images(self):
        self.IP.determine_images_with_person()
        self.IP.remove_images()

    ###########################################################
    # This function blurs the images.
    ###########################################################
    
    def blur_images(self):
        self.IP.blur_images()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


