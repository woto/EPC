#coding=UTF-8

from window_mgr import WindowMgr
from functions import *

check_or_start_febest()

wmgr = WindowMgr()
wmgr.find_window_wildcard("(.*)Febest")
wmgr.set_foreground(False, True, True)