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
    
    
                    
def search_vin_in_current_area(vin):
  logging.debug('search_vin_in_current_area')
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

  print "Found " + vin

  

if os.path.exists('./application.lock'):
  shutil.rmtree('./application.lock')

  
  
def check_or_start_toyota_epc():
  logging.debug('check_or_start_toyota_epc')
  wmgr = WindowMgr()
  logging.debug('Проверяем запущено ли вообще Toyota EPC') 
  wmgr.find_window_wildcard("TOYOTA ELECTRONIC PARTS CATALOG(.*)")
  if len(wmgr._handle) == 0:  
    logging.debug('Нет, запускаем')
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", toyota_epc_path).group(0))
    os.startfile(toyota_epc_path)
    os.chdir(origWD)
  logging.debug("Вышли из метода проверки запущенности Toyota EPC. Далее считается, что Toyota EPC запущен")

  
  
def check_or_start_tectdoc():
  logging.debug('check_or_start_tectdoc')
  wmgr = WindowMgr()
  logging.debug('Ищем окно TECDOC') 
  wmgr.find_window_wildcard(".*TECDOC(.*)")
  if len(wmgr._handle) == 0:
    logging.debug('TECDOC не был запущен, запускаем') 
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", tecdoc_path).group(0))
    os.startfile(tecdoc_path)
    os.chdir(origWD)
  logging.debug("Вышли из метода проверки запущенности Tecdoc. Далее считается, что Tecdoc запущен")
   

   
def goto_main_menu_toyota_epc():
  logging.debug("goto_main_menu_toyota_epc")
  i = 0
  
  while True:
    try:
      logging.debug('Ищем любое окно TOYOTA...')
      wmgr = WindowMgr()
      wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)")
      logging.debug('Переходим в цикл перебора всех окон TOYOTA... и смешиваем их')
      random.shuffle(wmgr._handle)
      for i, element in enumerate(wmgr._handle):
        logging.debug('Работаем с окном ' + wmgr._title[i] + " внутри цикла перебора всех окон Toyota...")
        wmgr.set_foreground(False, False, False, i)
        logging.debug('Сделали его активным')
        #time.sleep(0.1)
        wsh.SendKeys("{ESC}")
        logging.debug('Отправили в него Esc')
      
      logging.debug('Ищем кнопку TMC...')
      main_wnd = find_match(None, ['images/Toyota EPC/TMC Part Number Translation/1.png', 'images/Toyota EPC/TMC Part Number Translation/2.png'], (11, 127, 511, 155), 100, False)
      
      if main_wnd:
        logging.debug('Нашли кнопку TMC Part Number Translation, далее считается, что окно находится на самом верху и мы находимся в главном меню')
        break
    except:
      i = i + 0.1
      logging.debug("Спим " + str(i) + " с. перед следущей итерацией goto_main_menu_toyota_epc")
      time.sleep(i)

      
      
def in_each_region(some_method):
  logging.debug('in_each_region')
  
  areas = {
    'Europe': {'searched': False, 'coords': None, 'blue_point_y': 13}, 
    'General': {'searched': False, 'coords': None, 'blue_point_y': 30},
    'USA, Canada': {'searched': False, 'coords': None, 'blue_point_y': 46},
    'Japan': {'searched': False, 'coords': None, 'blue_point_y': 65}
  }

  for counter in range(4):
    goto_main_menu_toyota_epc()
    logging.debug("Выполняем " + str(counter+1) + " итерацию в цикле перехода по регионам")
    
    sleep = 0.1
    
    while True:
      try:
        logging.debug("Нахдимся внутри цикла щелканья на кнопку Area/Language и поиска Setup the necessary items")
        logging.debug("Щелкаем на Area/Language в главном меню")
        click(264, 344)
        logging.debug("Щелкнули на Area/Language в главном меню")
        time.sleep(sleep) # Обязтаельно
        logging.debug('Ищем любое окно TOYOTA...Area')
        time.sleep(sleep) # Обязательно
        wmgr = WindowMgr()
        wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*)Area.*")
        wmgr.set_foreground(False, False, False)
        logging.debug('Нашли окно TOYOTA...Area, сделали его активным')
        
        logging.debug('Ищем Setup the necessary items')   
        coords = find_match(False, ['images/Toyota EPC/Setup the necessary items.png'], (0, 342, 657, 368), 100, False)
        if coords:
          logging.debug('Теперь мы точно уверены, что окно выбора регионов открыто, т.к. нашли Setup the necessary items')
          break
        else:
          raise
      except:
        sleep = sleep + 0.1
        logging.debug("Где-то вылетел exception, будем повторять. Спим " + str(sleep) + " с. перед следущей итерацией поиска окна регионов с Setup the necessary items")
        time.sleep(sleep)

    break_upper = False
      
    for area in areas.keys():
      logging.debug("Обрабатываемый регион " + area)
      if areas[area]['searched']:
        logging.debug("Пропускаем регион " + area + " т.к. в нем уже искали")
        continue
      else:
        logging.debug("Регион " + area + " не помечен как searched")

      logging.debug("Ищем координаты региона " + area)
      coords = find_match(False, ['images/Toyota EPC/Areas/' + area + '.png'], (62, 135, 206, 252), 100, False)
      if coords:
        logging.debug("Нашли регион " + area + " возвращаемся из цикла")
        break_upper = True
        break
      else:
        logging.debug("Координаты региона " + area + " не найдены")
    
    logging.debug("На данном этапе мы точно знаем, что нашли регион, в котором еще не были " + area + ", отмечаем его")
    areas[area]['searched'] = True

    img = ImageGrab.grab((158, 135, 159, 252))
    img.save('1.png')
    
    img = img.convert("RGBA")
    pixdata = img.load()

    click(coords[0] + 62, coords[1] + 135)    
    if(pixdata[0, areas[area]['blue_point_y']] == (10, 36, 106, 255)):
      print 'good!'

    time.sleep(0.1)  
    
    wsh.SendKeys("{F8}")

app = make_json_app(__name__)
wsh = comclt.Dispatch("WScript.Shell")

@app.route('/json/t_sub/<catalog_number>/')
def toyota_substitution(catalog_number):
  logging.debug('toyota_substitution')
  
  wmgr = WindowMgr()
  wmgr.minimize_all_windows()
  check_or_start_toyota_epc()
  
  return post_process_allow_origin(jsonify(time=str(catalog_number)))


  
@app.route('/json/t_vin/<vin_code>/')
def vin(vin_code):
  logging.debug('vin')
  
  check_or_start_toyota_epc()
  goto_main_menu_toyota_epc()
  
  i=0
  
  if True:
  #while True:
    #try:

      print "Searching " + str(vin)

      in_each_region(search_vin_in_current_area)  

    #except:
    #  print sys.exc_info()[0]
    #  print '345try34'

    #i = i + 0.3
    
  return post_process_allow_origin(jsonify(time=str(vin_code)))
  
  
  
@app.route('/json/info/<catalog_number>/', defaults={'manufacturer': None})
@app.route('/json/info/<catalog_number>/<manufacturer>')
def info(catalog_number, manufacturer):
  logging.debug('info')
  
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
    
      check_or_start_toyota_epc()
      
      goto_main_menu_toyota_epc()
          
      return post_process_allow_origin(jsonify(time=str(catalog_number)))
          
    else:
      
      check_or_start_tectdoc()
      i = 0        

      while True:
        try:
          logging.debug('Сейчас мы ищем TECDOC, мы уже знаем, что он точно запущен, ищем его') 
          wmgr.find_window_wildcard(".*TECDOC(.*)")
          
          logging.debug('Спим ' + str(i) + 'с. перед тем как сделать активным TECDOC')
          time.sleep(i)
          wmgr.set_foreground(True, True, True)

          logging.debug('Спим ' + str(i) + 'с. перед отправкой в него ESC')
          time.sleep(i)
          logging.debug('Нажимем ESC')
          wsh.SendKeys("{ESC}")
          time.sleep(0.1) # Обязательно!
          
          logging.debug('Ищем поставленную галочку на "Любой номер"')
          coords = find_match(None, ['images/Tecdoc/Check Box - Checked.png'], (749, 104, 767, 121), 10, False)
          
          if coords:
            logging.debug('Нашли поставленную галочку на "Любой номер"') 

            logging.debug('Спим ' + str(i) + 'с. перед перед снятием галочки с "Любой номер"')
            time.sleep(i) 
            click(757, 113)
            time.sleep(0.1) # Обязательно!
            
            logging.debug('Спим ' + str(i) + 'с. перед проверкой, что мы действительно сняли галочку с "Любой номер"')
            time.sleep(i)
            coords = find_match(None, ['images/Tecdoc/Check Box - Unchecked.png'], (749, 104, 767, 121), 10, False)
            if coords:
              logging.debug('Убедились, что галочка "Любой номер снята", спим перед нажатием на кнопку поиска запчастей (Увеличительное стекло)') 
              click(209, 43)
              
              logging.debug('Спим ' + str(i) + 'с. перед вводом каталожного номера')
              logging.debug('Вводим каталожный номер.')
              wsh.SendKeys(catalog_number)
              
              logging.debug('Спим ' + str(i) + 'с. перед нажатием Enter')
              wsh.SendKeys("{ENTER}")
              
              for i in range(50):
                logging.debug('Ищем ' + str(i+1) + ' раз наличие, либо отсутсвтие информации по запчасти') 
                
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
                time.sleep(0.1)
                
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
          print 'wertswg'

        i = i + 0.3
        
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
