#coding=UTF-8

import re, win32gui, win32con
import time

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = []
        self._title = []

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle.append(win32gui.FindWindow(class_name, window_name))
        self._title.append(window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        result = re.match(wildcard, str(win32gui.GetWindowText(hwnd)))
        if result != None:
            #print str(win32gui.GetWindowText(hwnd))
            self._handle.append(hwnd)
            self._title.append(result.group(1))

    def find_window_wildcard(self, wildcard):
        self._handle = []
        self._title = []
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self, element=0):
        """put the window in the foreground"""
        #time.sleep(0.2)
        #win32gui.SetForegroundWindow(self._handle[element])        
        win32gui.SetWindowPos(self._handle[element], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        #win32gui.ShowWindow (self._handle[element],win32con.SW_SHOWMAXIMIZED)
        #time.sleep(0.2)
        win32gui.SetActiveWindow(self._handle[element])
        time.sleep(0.2)
        win32gui.ShowWindow(self._handle[element], win32con.SW_RESTORE)
        win32gui.ShowWindow(self._handle[element], win32con.SW_SHOW)
        time.sleep(0.2)
        win32gui.SetFocus(self._handle[element])
