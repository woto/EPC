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

# Ищем Area/Language, если находим, то запоминаем координаты меню, и вылетаем.
# Вылет произойдет по Exception если попытаемся передать фокус окну.
try:
  while True:
    wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Area.*)")
    wmgr.set_foreground()
    print 'Проверка на цикл 1'    
    time.sleep(0.2)
    area_wnd = find_match(None, ['images/Menu.png'], None, 100, True)
    # Для того чтобы выравнять значения
    area_wnd[0] = area_wnd[0] + 54
    area_wnd[1] = area_wnd[1] + 322
    wsh.SendKeys("{ESC}")
    
except:
  pass


# Ищем любое окно и в нем ищем кнопку TMC Part Number...
# повторяем пока не найдем
while True:
  wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)")
  wmgr.set_foreground()
  print 'Проверка на цикл 2'
  time.sleep(0.2)  
  wsh.SendKeys("{ESC}")
  main_wnd = find_match(None, ['images/TMC Part Number Translation/1.png', 'images/TMC Part Number Translation/2.png'], None, 100, False)  
  if main_wnd:
    break
    
# Если координаты Area/Language не найдены ранее
if not area_wnd:
  while True:
    # Кликаем на кнопке Area/Language
    click(main_wnd[0] + 70, main_wnd[1] + 200)
    
    print 'Проверка на цикл 3'
    time.sleep(0.2)
    
    # Убеждаемся что окно действительно открылось
    area_wnd = find_match(None, ['images/Setup the necessary items.png'], None, 100, False)
    if area_wnd:
      #while True:
      #  wsh.SendKeys("{ESC}")
      #  print type(main_wnd[0] + 100)
      #  main_wnd = find_match(None, ['images/TMC Part Number Translation/1.png', 'images/TMC Part Number Translation/2.png'], (main_wnd[0], main_wnd[1], main_wnd[0]+500, main_wnd[1]+500), 300, False)
      #  break
      break

    wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Area.*)")
    if wmgr._title.find('Area') >= 0:
      wmgr.set_foreground()
    
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
