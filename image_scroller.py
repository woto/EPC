#coding=UTF-8
import sys
sys.path.append("C:\\opencv\\build\\python\\2.7")

import win32api, win32con
import time, math, random, pdb
import pyscreenshot as ImageGrab
import cv2.cv as cv
import win32com.client as comclt

from window_mgr import WindowMgr

wsh = comclt.Dispatch("WScript.Shell")
wmgr = WindowMgr()
wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG.*")
wmgr.set_foreground()

def find_match(file_name, template_array, roi, minimal, debug):

  if not file_name:
    file_name = 'img.png'
    if roi:
      im = ImageGrab.grab(roi)
    else:
      im = ImageGrab.grab()
    im.save(file_name)

  for id, template in enumerate(template_array):
    img = cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_COLOR)
    tpl = cv.LoadImage(template, cv.CV_LOAD_IMAGE_COLOR)
  
    res = cv.CreateImage((img.width - tpl.width + 1, img.height - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
    cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)
    (minval, maxval, minloc, maxloc) = cv.MinMaxLoc(res)

    if debug:
      print "minval:" + str(minval)
      print "maxval:" + str(maxval)
      print '"' + template + '": ' + str(minloc)
      cv.Rectangle(img, 
        (minloc[0], minloc[1]),
        (minloc[0] + tpl.width, minloc[1] + tpl.height),
      cv.Scalar(0, 1, 0, 0))
      
      cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
      cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
      cv.ShowImage('image', img)
      cv.ShowImage('template', tpl)
      
      cv.WaitKey(0)

      cv.DestroyWindow('image')
      cv.DestroyWindow('template')
    
    if minval < minimal:
      return (minloc[0], minloc[1])

def click(x, y):  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def goto_main_menu():
  # Нажимаем ESC пока не выйдем в главное меню
  while True:
    wsh.SendKeys("{ESC}")
    time.sleep(0.1)
  
    return find_match(False, 
      ['images/TMC Part Number Translation/3.png', 'images/TMC Part Number Translation/4.png'],
      False, 100, False)


def search_vin_in_current_area(vin):
  
  (x, y) = goto_main_menu()

  # Ждем появления Search.png
  while True:
    click(x, y)
    time.sleep(0.1)
  
    coords = find_match(False, ['images/Search.png'], False, 100, False)
  
    if coords:
      break
  
  # Магия с раскладкой
  win32api.SendMessage(0xFFFF, 0x50, 1, 0x4090409)
  time.sleep(1)
  wsh.SendKeys(vin)
  wsh.SendKeys("{ENTER}")
  coords = find_match(None, ['images/Appropriate vehicle cannot be found.png'], None, 100, False)
  if coords:
   raise Exception("found")
  else:
    time.sleep(3)

for i in range(4):

  goto_main_menu()
  
  (x, y) = find_match(None, 
	['images/Area Language setup/1.png', 'images/Area Language setup/2.png', 'images/Area Language setup/3.png'], 
    None, 100, False)
  
  click(x, y)
  
  # Ждем появление окна настроек Area/Language
  while True:
    time.sleep(0.1)
    coords = find_match(False, ['images/Setup the necessary items.png'], False, 100, False)
    if coords:
      break
  
  # Поднимаемся безусловно на самый верх
  for j in range(4):
    time.sleep(0.1)
    wsh.SendKeys("{UP}")
  
  # Опускаемся на нужное количество в соответствии с итерацией
  for j in range(i):
    time.sleep(0.1)
    wsh.SendKeys("{DOWN}")
  
  time.sleep(0.1)
  wsh.SendKeys("{ENTER}")
  time.sleep(0.1)
  wsh.SendKeys("{F8}")

  search_vin_in_current_area("JTEHH20V410084243")
