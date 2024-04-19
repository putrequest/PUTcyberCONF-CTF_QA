from PyQt6.QtWidgets import QApplication
import sys

import windowInit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = windowInit.MainWindow()
    window.show()
    sys.exit(app.exec())
