#coding=UTF-8

from window_mgr import WindowMgr
from functions import *

check_or_start_febest()

wmgr = WindowMgr()
wmgr.find_window_wildcard("Каталог(.*)Febest")
wmgr.set_foreground(False, True, True)

time.sleep(0.5)
drag_drop((784, 96), (1050, 96))
img = ImageGrab.grab((272, 106, 1262, 322))
img.save('1.png')