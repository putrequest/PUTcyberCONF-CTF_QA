from PyQt6.QtWidgets import QVBoxLayout, QApplication
from PyQt6 import QtWidgets as widget
from PyQt6 import QtGui
# local imports
import gui, functions
import qdarkstyle

class MainWindow(widget.QMainWindow):
    
    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        self.ui = gui.Ui_CTF_QA()
        self.ui.setupUi(self)
        
        functions.set_app_icon(app)
        
        self.UI_manager(app)
        self.show()

    def UI_manager(self, app: QApplication):
        # SET MENU BAR
        self.ui.action_reset_progress.triggered.connect(functions.reset_progress)
        # appearance
        def set_appearance_dark():
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
            self.ui.action_appearance_light.setChecked(False)
            self.ui.action_appearance_dark.setChecked(True)
        def set_appearance_light():
            app.setStyleSheet("")
            self.ui.action_appearance_light.setChecked(True)
            self.ui.action_appearance_dark.setChecked(False)
            
        self.ui.action_appearance_dark.triggered.connect(set_appearance_dark)
        self.ui.action_appearance_light.triggered.connect(set_appearance_light)
        
        font = self.ui.title.font()
        font.setBold(True)
        font.setPointSize(24)
        font_id = QtGui.QFontDatabase.addApplicationFont(functions.resource_path("assets/fonts/AnonymousPro-Bold.ttf"))
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        font.setFamily(font_family)
        self.ui.title.setFont(font)
        
        self.task_layout = QVBoxLayout(self.ui.scroll_area_tasks_widget)
        functions.populate_task_list(self.task_layout, self.ui.title)
        self.task_layout.addStretch()