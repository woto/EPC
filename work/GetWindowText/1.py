'''
import win32gui as w

WM_GETTEXTLENGTH = 0x0E
WM_GETTEXT = 0x0D

hwnd = 007410E8

t1 = w.SendMessage(hwnd, WM_GETTEXTLENGTH, 0, 0)  #hwnd has to be the handle to the text control
t = " "*t1
tl = w.SendMessage(hwnd, WM_GETTEXT, tl + 1, t)

print t
print t1
'''

import time

import win32gui

while True:
  window = win32gui.GetForegroundWindow()
  title = win32gui.GetWindowText(window)
  #if title == 'Errors occurred':
  control = win32gui.FindWindowEx(window, 0, None, None)
  print 'text: ', win32gui.GetWindowText(control)
  time.sleep(1)