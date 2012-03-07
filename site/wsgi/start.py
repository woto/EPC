#coding=UTF-8

import sys
import win32api, win32con
import time, math, random, pdb
import win32com.client as comclt
from seed_vin import *
from find_match import *
from window_mgr import WindowMgr

def click(x, y):  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def search_vin_in_current_area(vin, area):


  # Ждем появления Search.png
  while True:
    click(coords[0] + 100, coords[1] + 100)
    time.sleep(0.2)
  
    coords = find_match(False, ['images/Search.png'], (400, 50, 550, 200), 100, False)
  
    if coords:
      break
  
  # Магия с раскладкой
  win32api.SendMessage(0xFFFF, 0x50, 1, 0x4090409)
  time.sleep(0.2)
  wsh.SendKeys(vin)
  time.sleep(0.2)
  wsh.SendKeys("{ENTER}")

  # Ждем пока пропадет фокус с кнопки Search
  #while True:
  #  time.sleep(0.2)
  #  coords = find_match(None, ['images/Search (focused).png'], (400, 50, 550, 200), 100, False)
  #  if not coords:
  #    break
  
  for i in range(3):
    time.sleep(0.2)
    coords = find_match(None, ['images/Appropriate vehicle cannot be found.png'], None, 300, False)
    if coords:
      return

  print "Found " + vin + " in " + area




wsh = comclt.Dispatch("WScript.Shell")
wmgr = WindowMgr()
main_wnd = None
area_wnd = None


# Проверяем запущено ли вообще приложение
wmgr.find_window_wildcard("(.*)TOYOTA ELECTRONIC PARTS CATALOG(.*)")
if len(wmgr._handle) == 0:
  sys.exit("Toyota EPC doesn't running.")
  

# Ищем любое окно и в нем ищем кнопку TMC Part Number...
# повторяем пока не найдем
while True:
  wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)")
  for i, element in enumerate(wmgr._handle):
    wmgr.set_foreground(i)
    if wmgr._title[i].find("Main") == -1:
      wsh.SendKeys("{ESC}")
              
  print 'Cycle 1'
  
  main_wnd = find_match(None, ['images/TMC Part Number Translation/1.png', 'images/TMC Part Number Translation/2.png'], None, 100, False)  
  if main_wnd:
    break
    

# Кликаем по кнопке найденной в предыдущем шаге
for i in range(10):
  try:
    click(main_wnd[0] + 70, main_wnd[1] + 200)
    time.sleep(pow(i/2, 1.7))
    
    wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Area.*)")
    wmgr.set_foreground()
    time.sleep(pow(i/2, 1.7))
    
    print 'Cycle 2'
          
    # Убеждаемся, что окно действительно открылось
    area_wnd = find_match(None, ['images/Setup the necessary items.png'], None, 200, False)

    # Убеждаемся, что окно действительно закрылось    
    if area_wnd:
      while True:
        wsh.SendKeys("{ESC}")
        
        print 'Cycle 3'
        
        coords = find_match(None, ['images/TMC Part Number Translation/1.png', 'images/TMC Part Number Translation/2.png'], (main_wnd[0] - 10, main_wnd[1] - 10, main_wnd[0] + 200, main_wnd[1] + 50), 100, False)
        if coords:
          break
      break

  except:
    #print "Unexpected error:", sys.exc_info()[0]
    pass

    
print main_wnd
print area_wnd
sys.exit(-1)

for id, vin in enumerate(vins):
  
  areas = {'Europe': {'searched': False, 'coords' : None}, 
    'General': {'searched': False, 'coords': None},
    'USA, Canada': {'searched': False, 'coords': None},
    'Japan': {'searched': False, 'coords': None}}

  print "Searching " + vin

  for i in range(4):

    # Нажимаем ESC пока не выйдем в главное меню
    while True:
      wsh.SendKeys("{ESC}")
      time.sleep(0.2)
    
      coords = find_match(False, 
    	  ['images/Area Language setup/1.png', 'images/Area Language setup/2.png'], 
        (100, 300, 400, 400), 100, False)  
    
      if coords:
        break
    
    time.sleep(0.2)
    click(coords[0] + 100, coords[1] + 300)
    
    # Ждем появление окна настроек Area/Language
    while True:
      time.sleep(0.2)
      coords = find_match(False, ['images/Setup the necessary items.png'], False, 300, False)
      if coords:
        break

    for area in areas.keys():
      if areas[area]['searched']:
        continue
      coords = find_match(False, ['images/Areas/' + area + '.png'], (300, 300, 500, 500), 100, False)
      if coords:
        break

    time.sleep(0.2)
    areas[area]['searched'] = True

    click(coords[0] + 300, coords[1] + 300)
    time.sleep(0.2)

    wsh.SendKeys("{F8}")
    time.sleep(0.2)

    search_vin_in_current_area(vin, area)
