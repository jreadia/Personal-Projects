import time
import threading
import pyautogui
import win32gui
import win32api
import win32con

def get_window_rect(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect, hwnd
    else:
        print(f"Window '{window_name}' not found!")
        return None, None

def autoclicker(window_name):
    rect, hwnd = get_window_rect(window_name)
    if rect:
        while True:
            x = (rect[0] + rect[2]) // 2
            y = (rect[1] + rect[3]) // 2
            lParam = win32api.MAKELONG(x, y)
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
            time.sleep(10)

def start_autoclicker(window_name):
    thread = threading.Thread(target=autoclicker, args=(window_name,))
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    minecraft_window = "Minecraft* 1.21.1 - Multiplayer (3rd-party Server)"
    print(f"Starting autoclicker on '{minecraft_window}' with 5 seconds delay...")
    start_autoclicker(minecraft_window)
    input("Press Enter to stop...\n")