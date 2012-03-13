import win32api, win32con

def move(x, y):  
  win32api.SetCursorPos((x,y))

  
def click(x, y):  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise
