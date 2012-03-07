import sys
sys.path.append("C:\\opencv\\build\\python\\2.7")

import win32api, win32con
#
#def click(x,y):
#    win32api.SetCursorPos((x,y))
#    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
#    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
#
#click(100, 100) # simulate mouse click at 100px, 100px

import win32api
import time
import math
import random

for i in range(500):
    x = int(random.uniform(1, 500))
    y = int(random.uniform(1, 500))
    win32api.SetCursorPos((x,y))
    time.sleep(1.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)