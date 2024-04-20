from PyQt6.QtWidgets import QVBoxLayout
from PyQt6 import QtWidgets as widget
# local imports
import gui, functions

class MainWindow(widget.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.Ui_CTF_QA()
        self.ui.setupUi(self)
        
        self.setFixedSize(self.size())
        
        self.UI_manager()
        self.show()

    def UI_manager(self):
        # SET MENU BAR
        self.ui.action_reset_progress.triggered.connect(functions.reset_progress)
        
        font = self.ui.title.font()
        font.setBold(True)
        font.setPointSize(18)
        font.setFamily("Fira Code")
        self.ui.title.setFont(font)
        
        self.task_layout = QVBoxLayout(self.ui.scroll_area_tasks_widget)
        functions.populate_task_list(self.task_layout, self.ui.title)
        self.task_layout.addStretch()