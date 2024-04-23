from PyQt6.QtWidgets import QApplication
import sys
import qdarkstyle

import windowInit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    
    window = windowInit.MainWindow(app)
    window.show()
    sys.exit(app.exec())
