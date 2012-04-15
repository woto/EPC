
# http://www.ivings.org.uk/2010/11/grab-ui-window-text-with-python/

import win32con
import win32gui
import array
import ctypes
import struct
import sys
import win32api
from ctypes import *
import time
import pdb
from functions import *

results = []
topWindows = []
#chatHwnd = 0
windowTitleText = "ELECT"
#The text that the wanted window string begins with, so we can find it
windowStartText = ""

 
 
'''Handler to enumerate the window with param hwnd
Returns resultsList; the window details as an array,
with hwnd, text and class'''
def _windowEnumerationHandler(hwnd, resultList):
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))
                       

'''Recursive function, checks the text of all the children of
the window with handle param hwnd until it reaches the text that
we require, returns the String of this data'''
def searchChildWindows(hwnd):
    childWindows = []
    try:
        #get child windows
        win32gui.EnumChildWindows(hwnd, _windowEnumerationHandler, childWindows)
    except win32gui.error, exception:
        # This seems to mean that the control does not or cannot have child windows
        return
 
    #get details of each child window
    for childHwnd, windowText, windowClass in childWindows:
        searchChildWindows(childHwnd)
        win32gui.SetFocus(childHwnd)
        win32gui.SetForegroundWindow(childHwnd)       
        #create text buffer
        buf_size = 1 + win32gui.SendMessage(childHwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        buffer = win32gui.PyMakeBuffer(buf_size)
        #get text from Window using hardware call. (getWindowText() did not return anything)
        win32gui.SendMessage(childHwnd, win32con.WM_GETTEXT, buf_size, buffer)
        #check to see if it's the data we want...
        logging.debug(buffer)
        #if buffer[0:buf_size].find(windowStartText)>-1:
            #pdb.set_trace()
            #return the hwnd
 
            #global chatHwnd
            #chatHwnd = childHwnd
            #return int(childHwnd)
        #    pass
        #else recurse, checking this window for children
        #might not be needed...
                       
if __name__ == '__main__':
    #declare global
    global chatHwnd
    #enumerate all open windows, return topWindows
    win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
    #check each window to fin the one we need
    for hwnd, windowText, windowClass in topWindows:
        if windowText.find(windowTitleText)>-1:
            #search the child windows
            # save the window handle
            chatHwnd = searchChildWindows(hwnd)
            #set the appropriate window focus (if needed)
            #win32gui.SetFocus(hwnd)
            #win32gui.SetForegroundWindow(hwnd)
 
            initBuff = 0
            #get text
            while chatHwnd>0:
 
                buf_size = 1 + win32gui.SendMessage(chatHwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
                buffer = win32gui.PyMakeBuffer(buf_size)
                # send a win GETTEXT request to the window and read into buffer
                win32gui.SendMessage(chatHwnd, win32con.WM_GETTEXT, buf_size, buffer)
                if buf_size-initBuff>1:
                      print buffer[initBuff:buf_size]
 
                initBuff = buf_size
                #after 5 seconds, get any new text
                time.sleep(1)
                # needed for Java to read the output correctly
                sys.stdout.flush()