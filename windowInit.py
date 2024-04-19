from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, QSize, QStandardPaths
from PyQt6 import QtGui, uic
from PyQt6 import QtWidgets as widget

from functools import partial

# local imports
import gui, strings

class MainWindow(widget.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.Ui_CTF_QA()
        self.ui.setupUi(self)
        
        self.setFixedSize(self.size())
        
        self.UI_manager()
        self.show()
    
    def new_task_submit_hint():
        # creating new task frame with description, answer and submit & hint buttons
        print("hee")
        

    def UI_manager(self):
        self.ui.title.setText("Warsztaty Forensics")
        
        self.task_layout = QVBoxLayout(self.ui.scroll_area_tasks_widget)
        
        for i in range(30):
            label = QLabel(f"Label {i}")
            self.task_layout.addWidget(label)