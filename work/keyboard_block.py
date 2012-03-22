import pyHook
import pythoncom
import thread
import threading
import time

def onclick(event):
    print event.Position
    return False

#def run_thread (threadname, count, sleeptime):
hm = pyHook.HookManager()
hm.SubscribeMouseAllButtonsDown(onclick)
hm.HookMouse()
pythoncom.PumpMessages()
hm.UnhookMouse()