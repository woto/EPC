import pythoncom, pyHook 
 
def OnKeyboardEvent(event):
  # block only the letter A, lower and uppercase
  return False
  
def OnMouseEvent(event):
  return False
    
# create a hook manager
hm = pyHook.HookManager()
# watch for all keyboard events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# watch for all mouse events
hm.MouseAll = OnMouseEvent
# set the hook
hm.HookMouse()
# wait forever
pythoncom.PumpMessages()