import time
import threading
import win32gui
import win32api
import win32con
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox

def get_window_rect(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect, hwnd
    else:
        print(f"Window '{window_name}' not found!")
        return None, None

stop_event = threading.Event()
clicker_thread = None

def autoclicker(window_name):
    rect, hwnd = get_window_rect(window_name)
    if rect:
        while not stop_event.is_set():
            x = (rect[0] + rect[2]) // 2
            y = (rect[1] + rect[3]) // 2
            lParam = win32api.MAKELONG(x, y)
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
            time.sleep(float(window.delay_var.text()))

def start_autoclicker(window_name):
    global stop_event, clicker_thread
    stop_event.clear()
    clicker_thread = threading.Thread(target=autoclicker, args=(window_name,))
    clicker_thread.daemon = True
    clicker_thread.start()
    window.status_label.setText("Auto Clicker: ON")
    window.status_label.setStyleSheet("color: green;")

def stop_autoclicker():
    global stop_event, clicker_thread
    stop_event.set()
    if clicker_thread and clicker_thread.is_alive():
        clicker_thread.join(timeout=1)
    window.status_label.setText("Auto Clicker: OFF")
    window.status_label.setStyleSheet("color: red;")

def get_window_list():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd).strip()
            if window_text:
                windows.append(window_text)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

class AutoClickerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("click.ico"))  # Ensure click.ico is in the same directory

        tray_menu = QMenu()
        restore_action = tray_menu.addAction("Restore")
        restore_action.triggered.connect(self.show)
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()  # Add this line to show the tray icon

    def initUI(self):
        self.setWindowTitle("Auto Clicker")
        self.setGeometry(100, 100, 400, 250)
        self.setWindowIcon(QIcon("C:/4 - CODING FILES/PERSONAL PROJECTS/auto_clicker/click.ico"))  # Ensure click.ico is in the same directory
        self.setStyleSheet("background-color: #f0f0f0;")  # Add this line to set a light background color
        
        layout = QtWidgets.QVBoxLayout()

        self.window_var = QtWidgets.QComboBox(self)
        self.window_var.addItems(get_window_list())
        layout.addWidget(QtWidgets.QLabel("Select a window:"))
        layout.addWidget(self.window_var)

        self.delay_var = QtWidgets.QLineEdit(self)
        self.delay_var.setText("10")
        layout.addWidget(QtWidgets.QLabel("Set delay (seconds):"))
        layout.addWidget(self.delay_var)

        self.start_button = QtWidgets.QPushButton("Start Auto Clicker", self)
        self.start_button.clicked.connect(self.start_clicker)
        layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton("Stop Auto Clicker", self)
        self.stop_button.clicked.connect(stop_autoclicker)
        layout.addWidget(self.stop_button)

        self.status_label = QtWidgets.QLabel("Auto Clicker: OFF", self)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_clicker(self):
        selected_window = self.window_var.currentText()
        if selected_window:
            stop_autoclicker()
            start_autoclicker(selected_window)

    def closeEvent(self, event):
        # Close the program when the X button is clicked
        self.tray_icon.hide()
        event.accept()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AutoClickerApp()
    window.show()
    app.exec_()