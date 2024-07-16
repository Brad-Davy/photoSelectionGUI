import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QProgressDialog
from PyQt6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QProgressDialog Example")
        self.setFixedSize(300, 200)

        # Create a button to start the long-running task
        self.start_button = QPushButton("Start Task", self)
        self.start_button.clicked.connect(self.start_task)

        # Create a layout and add the button to it
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)

        # Create a central widget and set the layout to it
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget to the main window
        self.setCentralWidget(central_widget)

    def start_task(self):
        # Step 4: Create and configure QProgressDialog
        progress_dialog = QProgressDialog("Task in progress...", "Cancel", 0, 100, self)
        progress_dialog.setWindowTitle("Progress")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)

        # Use a QTimer to simulate progress updates
        self.current_progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress(progress_dialog))
        self.timer.start(100)  # Update every 100 milliseconds

        self.progress_dialog = progress_dialog

    def update_progress(self, progress_dialog):
        # Increment the progress
        self.current_progress += 1

        # Update the progress dialog
        progress_dialog.setValue(self.current_progress)

        # Check if the user has requested to cancel
        if progress_dialog.wasCanceled():
            self.timer.stop()
            progress_dialog.close()
            print("Task was canceled!")
            return

        # Check if the task is complete
        if self.current_progress >= 100:
            self.timer.stop()
            progress_dialog.setLabelText("Task completed!")
            progress_dialog.setValue(100)
            QTimer.singleShot(500, progress_dialog.close)  # Close after 500 milliseconds
            print("Task completed!")

# Initialize the application
app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.show()

# Execute the application
sys.exit(app.exec())
