import sys
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QProgressDialog
from imageProcessing import IP  # Assume this is your custom module
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
            self.IP.determineImagesWithPerson()
            self.progress.emit(i)  # Emit progress signal
            time.sleep(0.1)  # Simulate work

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Processing GUI")
        self.setFixedSize(QSize(600, 200))
        self.UiComponents()
        self.IP = IP()
        self.yoloThread = Parallel(self.IP)
        self.yoloThread.progress.connect(self.update_progress)

    def UiComponents(self): 
        button = QPushButton("Set Image File", self) 
        button.setGeometry(350, 30, 100, 30)
        button.clicked.connect(self.setImageFile)

        #button = QPushButton("Run YOLO Algorithm", self) 
        #button.setGeometry(350, 60, 150, 30)
        #button.clicked.connect(self.determineImages) 

        button = QPushButton("Remove Images", self) 
        button.setGeometry(350, 60, 150, 30)
        button.clicked.connect(self.removeImages)

        button = QPushButton("Blur Images", self) 
        button.setGeometry(350, 90, 150, 30)
        button.clicked.connect(self.blurImages) 

        #button = QPushButton("Test", self) 
        #button.clicked.connect(self.start_task) 
        #button.setGeometry(350, 150, 150, 30)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(30, 30, 250, 30)

    def setImageFile(self):
        filePath = self.lineEdit.text()
        self.IP.setImagePath(filePath)
        print('Image path has been set too: {}'.format(filePath))

    def determineImages(self):
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

    def removeImages(self):
        self.IP.determineImagesWithPerson()
        self.IP.removeImages()

    def blurImages(self):
        self.IP.blurImages()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
