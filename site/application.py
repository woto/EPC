#coding=UTF-8

import json
from lockfile import FileLock
from functools import partial
from flask import Flask, jsonify, request
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.datastructures import Headers
from window_mgr import WindowMgr
import shutil
import os, logging, sys, re, time, random
import subprocess
import Image
import ImageChops
import win32com.client as comclt
from functions import *
from tecdoc_manufacturer_synonyms import *

import win32api, win32con
import time, math, random, pdb
import win32com.client as comclt
from seed_vin import *
from config import *

logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.DEBUG, 
                    filename='../logs/application.log')

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

def check_or_start_toyota_epc():
  wmgr = WindowMgr()
  logging.debug('Проверяем запущено ли вообще Toyota EPC') 
  wmgr.find_window_wildcard("TOYOTA ELECTRONIC PARTS CATALOG(.*)")
  if len(wmgr._handle) == 0:  
    logging.debug('Нет, запускаем')
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", toyota_epc_path).group(0))
    os.startfile(toyota_epc_path)
    os.chdir(origWD)
  logging.debug("Далее считается, что Toyota EPC запущен")

  while True:
    logging.debug('Ищем любое окно TOYOTA...')
    wmgr = WindowMgr()
    wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)")
    logging.debug('Переходим в цикл перебора всех окон TOYOTA...')
    random.shuffle(wmgr._handle)
    print(wmgr._handle)
    for i, element in enumerate(wmgr._handle):
      logging.debug('Нашли' + wmgr._title[i])
      wmgr.set_foreground(False, False, False, i)
      logging.debug('Сделали его активным')
      #time.sleep(0.5)
      wsh.SendKeys("{ESC}")
      logging.debug('Отправили в него Esc')
    
    logging.debug('Ищем кнопку TMC...')
    main_wnd = find_match(None, ['images/Toyota EPC/TMC Part Number Translation/1.png', 'images/Toyota EPC/TMC Part Number Translation/2.png'], (11, 127, 511, 155), 100, False)
    
    if main_wnd:
      logging.debug('Нашли кнопку TMC Part Number Translation')
      break

  
def check_or_start_tectdoc():
  wmgr = WindowMgr()
  # Проверяем запущено ли вообще приложение
  logging.debug('Ищем окно TECDOC') 
  wmgr.find_window_wildcard("(.*)TECDOC(.*)")
  if len(wmgr._handle) == 0:
    logging.debug('TECDOC не был запущен, запускаем') 
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", tecdoc_path).group(0))
    os.startfile(tecdoc_path)
    os.chdir(origWD)

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
wsh = comclt.Dispatch("WScript.Shell")

@app.route('/json/ts/<catalog_number>/')
def toyota_substitution(catalog_number):
  wmgr = WindowMgr()
  wmgr.minimize_all_windows()
  check_or_start_toyota_epc()
  return post_process_allow_origin(jsonify(time=str(catalog_number)))

@app.route('/json/vin/<vin_code>/')
def vin(vin_code):
  
  return post_process_allow_origin(jsonify(time=str(vin_code)))
  
@app.route('/json/info/<catalog_number>/', defaults={'manufacturer': None})
@app.route('/json/info/<catalog_number>/<manufacturer>')
def info(catalog_number, manufacturer):

  # На случай с FRI.TECH. когда Rails почему-то делает не .../catalog_number/manufacturer, a .../catalog_number?manufacturer=manufacturer
  if (manufacturer == None):
    manufacturer = request.args.get('manufacturer', '')  
  
  logging.debug('Проверяем наличие закешированной картинки') 
  if os.path.exists("./static/" + catalog_number + ".png"):
    logging.debug('Нашли и показали') 
    return post_process_allow_origin(jsonify(time=str(catalog_number))) 
    
  lock = FileLock("./application")
  with lock:
  
    wmgr = WindowMgr()
    wmgr.minimize_all_windows()    

    if manufacturer == "TOYOTA":
      main_wnd = None
      area_wnd = None

      check_or_start_toyota_epc()
      return post_process_allow_origin(jsonify(time=str(catalog_number)))


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
      
      check_or_start_tectdoc()
      i = 0        

      while True:
        try:
          logging.debug('Сейчас мы ищем TECDOC, мы уже знаем, что он точно запущен, ищем его') 
          wmgr.find_window_wildcard(".*TECDOC(.*)")
          
          logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед тем как сделать активным TECDOC')
          time.sleep(pow(i/2, 1.7))
          wmgr.set_foreground(True, True, True)

          logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед отправкой в него ESC')
          time.sleep(pow(i/2, 1.7))
          logging.debug('Нажимем ESC')
          wsh.SendKeys("{ESC}")
          time.sleep(0.1) # Обязательно!
          
          logging.debug('Ищем поставленную галочку на "Любой номер"')
          coords = find_match(None, ['images/Tecdoc/Check Box - Checked.png'], (749, 104, 767, 121), 10, False)
          
          if coords:
            logging.debug('Нашли поставленную галочку на "Любой номер"') 

            logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед перед снятием галочки с "Любой номер"')
            time.sleep(pow(i/2, 1.7)) 
            click(757, 113)
            time.sleep(0.1) # Обязательно!
            
            logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед проверкой, что мы действительно сняли галочку с "Любой номер"')
            time.sleep(pow(i/2, 1.7))
            coords = find_match(None, ['images/Tecdoc/Check Box - Unchecked.png'], (749, 104, 767, 121), 10, False)
            if coords:
              logging.debug('Убедились, что галочка "Любой номер снята", спим перед нажатием на кнопку поиска запчастей (Увеличительное стекло)') 
              click(209, 43)
              
              logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед вводом каталожного номера')
              logging.debug('Вводим каталожный номер.')
              wsh.SendKeys(catalog_number)
              
              logging.debug('Спим ' + str(pow(i/2, 1.7)) + 'с. перед нажатием Enter')
              wsh.SendKeys("{ENTER}")
              
              for i in range(10):
                logging.debug('Зашли в цикл, в котором будем искать либо наличие, либо отсутсвтие информации по запчасти') 
                
                logging.debug('Ищем окно, сообщающее, что каталожный номер не найден') 
                coords = find_match(None, ['images/Tecdoc/Not Found.png'], (564, 466, 732, 584), 100, False)
                if coords:
                  while True:
                    wsh.SendKeys("{ESC}")
                    coords = find_match(None, ['images/Tecdoc/Not Found.png'], (564, 466, 732, 584), 100, False)   
                    if not coords: 
                      return post_process_allow_origin(jsonify(time="Ничего не нашли"))
                    time.sleep(0.1)
                logging.debug('Ищем что-то там :), сообщающее, что каталожный номер найден') 
                coords = find_match(None, ['images/Tecdoc/Found Any.png'], (1128, 238, 1192, 258), 100, False)
                if coords:
                  logging.debug('Нашли что-то там :)') 
                  logging.debug('Граббим экран') 
                  im = ImageGrab.grab((207, 204, 1128, 890))
                  logging.debug('Сохраняем изображением в папке') 
                  im.save("./static/" + catalog_number + ".png")
                  logging.debug('Возвращаем результат') 
                  return post_process_allow_origin(jsonify(time=str(catalog_number)))        

                #TODO МУХЛЕЖ!
                time.sleep(0.3)
                
              logging.debug('По видимому столкнулись с проблематичной деталью, делаем возврат')
              #TODO МУХЛЕЖ!
              return post_process_allow_origin(jsonify(time=str(catalog_number)))
            else:
              logging.debug('Не смогли убедиться, что снята галочка с "Любой номер"')
              raise
          else:
            logging.debug('Не нашли поставленную галочку на "Любой номер"')
            raise
        except:
          print 'yes'

        i = i+1
  logging.debug('Безусловный возврат результата.') 
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
