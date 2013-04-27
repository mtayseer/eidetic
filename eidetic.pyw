# This is based

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from datetime import datetime
from PyQt4 import QtGui, QtCore
from eidetic_ui import Ui_Dialog


class Window(QtGui.QDialog, Ui_Dialog):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.setVisible(True)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(60 * 1000)
        self.timer.timeout.connect(self.take_screenshot)
        self.buttonBox.accepted.connect(self.accepted)
        self.is_enabled = False
        self.enable()

    def accepted(self):
        self.timer.stop()
        self.timer.setInterval(self.doubleSpinBox.value() * 60 * 1000)
        self.timer.start()

    def take_screenshot(self):
        self.screenshot = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        filename = datetime.now().strftime("./screenshots/%Y-%m-%d-%H-%M-%S.png")
        self.screenshot.save(filename, "png")

    def enable(self):
        self.is_enabled = not self.is_enabled
        if self.is_enabled:
            self.timer.start()
            self.enableAction.setText("Disable")
            self.trayIcon.setToolTip("Enabled")
            self.trayIcon.setIcon(QtGui.QIcon('./images/camera.png'))
            self.setWindowIcon(QtGui.QIcon('./images/camera.png'))
        else:
            self.timer.stop()
            self.enableAction.setText("Enable")
            self.trayIcon.setToolTip("Disabled")
            self.trayIcon.setIcon(QtGui.QIcon('./images/camera_disabled.png'))
            self.setWindowIcon(QtGui.QIcon('./images/camera_disabled.png'))

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()

    def setVisible(self, visible):
        self.optionsAction.setEnabled(not visible)
        super(Window, self).setVisible(visible)

    def createActions(self):
        self.optionsAction = QtGui.QAction("&Options", self, triggered=self.showNormal)
        self.enableAction = QtGui.QAction("&Enable", self, triggered=self.enable)
        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.optionsAction)
        self.trayIconMenu.addAction(self.enableAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                                   "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    #window.show()
    sys.exit(app.exec_())
