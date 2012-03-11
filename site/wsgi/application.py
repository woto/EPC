#coding=UTF-8

import json
from lockfile import FileLock
import time, random
from functools import partial
from flask import Flask, jsonify, request
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.datastructures import Headers
from window_mgr import WindowMgr
from find_match import *
import shutil
import sys
import subprocess
import sys
import Image
import ImageChops
import win32com.client as comclt
import os
from functions import *
from tecdoc_manufacturer_synonyms import *

import sys
import win32api, win32con
import time, math, random, pdb
import win32com.client as comclt
from seed_vin import *
from find_match import *
from window_mgr import WindowMgr
import os


def search_vin_in_current_area(vin, area):


  # Ждем появления Search.png
  while True:
    click(coords[0] + 100, coords[1] + 100)
    time.sleep(0.2)
  
    coords = find_match(False, ['images/Toyota EPC/Search.png'], (400, 50, 550, 200), 100, False)
  
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
  #  coords = find_match(None, ['images_toyota_epc/Search (focused).png'], (400, 50, 550, 200), 100, False)
  #  if not coords:
  #    break
  
  for i in range(3):
    time.sleep(0.2)
    coords = find_match(None, ['images/Toyota EPC/Appropriate vehicle cannot be found.png'], None, 300, False)
    if coords:
      return

  print "Found " + vin + " in " + area



if os.path.exists('./application.lock'):
  shutil.rmtree('./application.lock')
wsh = comclt.Dispatch("WScript.Shell")
  

def make_json_app(import_name, **kwargs):
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return post_process_allow_origin(response)

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app


app = make_json_app(__name__)

@app.route('/info/<catalog_number>', defaults={'manufacturer': None})
@app.route('/info/<catalog_number>/<manufacturer>')
def info(catalog_number, manufacturer):
  # На случай с FRI.TECH. когда Rails почему-то делает не .../catalog_number/manufacturer, a .../catalog_number?manufacturer=manufacturer
  if (manufacturer == None):
    manufacturer = request.args.get('manufacturer', '')

  lock = FileLock("./application")
  with lock:

    if manufacturer == "TOYOTA":

      wsh = comclt.Dispatch("WScript.Shell")
      wmgr = WindowMgr()
      main_wnd = None
      area_wnd = None


      # Проверяем запущено ли вообще приложение
      wmgr.find_window_wildcard("(.*)TOYOTA ELECTRONIC PARTS CATALOG(.*)")
      if len(wmgr._handle) == 0:  
        origWD = os.getcwd()
        os.chdir("C:\TMCEPCW3\APLI")
        os.startfile("C:\TMCEPCW3\APLI\TMAIN.EXE")
        os.chdir(origWD)  
        #sys.exit("Toyota EPC doesn't running.")
        

      # Ищем любое окно и в нем ищем кнопку TMC Part Number...
      # повторяем пока не найдем
      while True:
        wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)")
        for i, element in enumerate(wmgr._handle):
          wmgr.set_foreground(False, False, i)
          if wmgr._title[i].find("Main") == -1:
            wsh.SendKeys("{ESC}")
                    
        print 'Cycle 1'
        
        main_wnd = find_match(None, ['images/Toyota EPC/TMC Part Number Translation/1.png', 'images/Toyota EPC/TMC Part Number Translation/2.png'], None, 100, False)  
        if main_wnd:
          break
          

      # Кликаем по кнопке найденной в предыдущем шаге
      for i in range(10):
        try:
          click(main_wnd[0] + 70, main_wnd[1] + 200)
          time.sleep(pow(i/2, 1.7))
          
          wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Area.*)")
          wmgr.set_foreground(False, False)
          time.sleep(pow(i/2, 1.7))
          
          print 'Cycle 2'
                
          # Убеждаемся, что окно действительно открылось
          area_wnd = find_match(None, ['images/Toyota EPC/Setup the necessary items.png'], None, 200, False)

          # Убеждаемся, что окно действительно закрылось    
          if area_wnd:
            while True:
              wsh.SendKeys("{ESC}")
              
              print 'Cycle 3'
              
              coords = find_match(None, ['images/Toyota EPC/TMC Part Number Translation/1.png', 'images/Toyota EPC/TMC Part Number Translation/2.png'], (main_wnd[0] - 10, main_wnd[1] - 10, main_wnd[0] + 200, main_wnd[1] + 50), 100, False)
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
               ['images/Toyota EPC/Area Language setup/1.png', 'images/Toyota EPC/Area Language setup/2.png'], 
              (100, 300, 400, 400), 100, False)  
          
            if coords:
              break
          
          time.sleep(0.2)
          click(coords[0] + 100, coords[1] + 300)
          
          # Ждем появление окна настроек Area/Language
          while True:
            time.sleep(0.2)
            coords = find_match(False, ['images/toyota EPC/Setup the necessary items.png'], False, 300, False)
            if coords:
              break

          for area in areas.keys():
            if areas[area]['searched']:
              continue
            coords = find_match(False, ['images/Toyota EPC/Areas/' + area + '.png'], (300, 300, 500, 500), 100, False)
            if coords:
              break

          time.sleep(0.2)
          areas[area]['searched'] = True

          click(coords[0] + 300, coords[1] + 300)
          time.sleep(0.2)

          wsh.SendKeys("{F8}")
          time.sleep(0.2)

          search_vin_in_current_area(vin, area)
          
    else:
        
      if os.path.exists("../images/" + catalog_number + ".png"):
        return post_process_allow_origin(jsonify(time=str(catalog_number)))
      
      wmgr = WindowMgr()

      # Проверяем запущено ли вообще приложение
      wmgr.find_window_wildcard("(.*)TECDOC(.*)")
      if len(wmgr._handle) == 0:
        #sys.exit("TECDOC doesn't running.")
        origWD = os.getcwd()
        os.chdir("C:/TECDOC_CD/1_2012/pb/")
        os.startfile("C:/TECDOC_CD/1_2012/pb/tof.exe")
        os.chdir(origWD)
        
      while True:
        try:
          wmgr.find_window_wildcard("(.*)TECDOC(.*)")
          wmgr.set_foreground(True, True)
          break
        except:
          time.sleep(0.5)
          pass
        
      while True:
        # Ищем кнопку поиска и щелкаем по ней
        coords = find_match(None, ['images/Tecdoc/Check Box - Checked.png'], (749, 104, 767, 121), 100, False)
        wsh.SendKeys("{ESC}")
        if coords:
          # Убираем галочку с "Любой номер"
          click(757, 113)
          # И нажимаем на Увеличительном стекле (Поиск запчастей)
          click(209, 43)
          # Вводим каталожный номер
          wsh.SendKeys(catalog_number)
          wsh.SendKeys("{ENTER}")
          while True:
            coords = find_match(None, ['images/Tecdoc/Not Found.png'], (564, 466, 732, 584), 100, False)
            if coords:
              return post_process_allow_origin(jsonify(time="Ничего не нашли"))
            coords = find_match(None, ['images/Tecdoc/Found Any.png'], (1128, 238, 1192, 258), 100, False)
            if coords:
              im = ImageGrab.grab((207, 204, 1128, 890))
              im.save("../images/" + catalog_number + ".png")
              return post_process_allow_origin(jsonify(time=str(catalog_number)))        
        time.sleep(0.1)
    
  return post_process_allow_origin(jsonify(time=time.time()))

@app.route('/')
def hello_world():
  pyDict = {'one':1,'two':2}
  response = jsonify(one='1', two='2')
  return post_process_allow_origin(response)

def post_process_allow_origin(response):
  response.headers['Access-Control-Allow-Origin'] = "*"

  callback = request.args.get('callback', False)
  content = str(callback) + '(' + response.data + ')'
  return app.response_class(content)
  
  return response

if __name__ == '__main__':
  app.debug = True
  app.run('192.168.2.9', 5000)
