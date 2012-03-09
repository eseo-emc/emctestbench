import sys
from PyQt4.QtGui import QApplication
from gui.applicationwindow_controller import ApplicationWindowController


application = QApplication(sys.argv)
window = ApplicationWindowController()
window.show()
sys.exit(application.exec_())