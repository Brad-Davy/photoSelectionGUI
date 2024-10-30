import sys
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QProgressDialog
from image_processing import IP  
from image_input_output_google_drive import download_images, upload_images
import threading
import time

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

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Processing GUI")
        self.setFixedSize(QSize(300, 300))
        self.ui_components()
        self.IP = IP()
        self.yoloThread = Parallel(self.IP)
        self.yoloThread.progress.connect(self.update_progress)
        self.setStyleSheet("background-color: gray;")

    def ui_components(self): 
        button = QPushButton("Download Images", self) 
        button.setGeometry(75, 30, 150, 30)
        button.clicked.connect(download_images)

        button = QPushButton("Remove Images", self) 
        button.setGeometry(75, 80, 150, 30)
        button.clicked.connect(self.remove_images)

        button = QPushButton("Blur Images", self) 
        button.setGeometry(75, 130, 150, 30)
        button.clicked.connect(self.blur_images) 

        button = QPushButton("Upload Images", self) 
        button.setGeometry(75, 180, 150, 30)
        button.clicked.connect(upload_images) 

    def set_image_file(self):
        filePath = self.lineEdit.text()
        self.IP.setImagePath(filePath)
        print('Image path has been set too: {}'.format(filePath))

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

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def check_completion(self):
        if not self.thread.is_alive():
            self.check_completion_timer.stop()
            self.progress_dialog.setValue(100)
            self.progress_dialog.setLabelText("Task completed!")
            QTimer.singleShot(500, self.progress_dialog.close)  # Close after 500 milliseconds
            print("Task completed!")

    def remove_images(self):
        self.IP.determine_images_with_person()
        self.IP.remove_images()

    def blur_images(self):
        self.IP.blur_images()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
