#coding=UTF-8

import redis, json, sys, logging, pdb, sys, os, re, time, random
from window_mgr import WindowMgr
from config import *
import win32com.client as comclt

from functools import partial
import shutil
import subprocess
import Image
import ImageChops
from functions import * 
import pyscreenshot as ImageGrab

import win32api, win32con
import time, math, random, pdb
import win32com.client as comclt
from seed_vin import *


logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.DEBUG, 
                    filename='../logs/application.log')
key = ''

rs = redis.Redis(config['Redis'])

ps = rs.pubsub()
ps.subscribe('bee')

#rc.publish('foo', 'hello world')

def check_or_start_toyota_epc():
  logging.debug('check_or_start_toyota_epc')
  wmgr = WindowMgr()
  logging.debug('Проверяем запущено ли вообще Toyota EPC') 
  wmgr.find_window_wildcard("TOYOTA ELECTRONIC PARTS CATALOG(.*)")
  if len(wmgr._handle) == 0:  
    logging.debug('Нет, запускаем')
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", config['Toyota EPC']['path']).group(0))
    os.startfile(config['Toyota EPC']['path'])
    os.chdir(origWD)
  logging.debug("Вышли из метода проверки запущенности Toyota EPC. Далее считается, что Toyota EPC запущен")


def search_vin_in_current_area(vin):
  logging.debug('search_vin_in_current_area')
  # Ждем появления Search.png
  while True:
    click(245, 147)
    time.sleep(0.2)
  
    coords = find_match(False, ['images/Toyota EPC/Search.png'], (419, 93, 504, 124), 100, False)
  
    if coords:
      break
    else:
      time.sleep(0.1)
  
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
      return False

  return True

  
  
  
def check_or_start_tecdoc():
  logging.debug('check_or_start_tectdoc')
  wmgr = WindowMgr()
  logging.debug('Ищем окно TECDOC') 
  wmgr.find_window_wildcard(".*TECDOC(.*)")
  if len(wmgr._handle) == 0:
    logging.debug('TECDOC не был запущен, запускаем') 
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", config['Tecdoc']['path']).group(0))
    os.startfile(config['Tecdoc']['path'])
    os.chdir(origWD)
  logging.debug("Вышли из метода проверки запущенности Tecdoc. Далее считается, что Tecdoc запущен")
   

   
   
def goto_main_menu_toyota_epc():
  logging.debug("goto_main_menu_toyota_epc")
  sleep = 0.1
  
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
        time.sleep(sleep) # Обязательно
        wsh.SendKeys("{ESC}")
        logging.debug('Отправили в него Esc')
      
      logging.debug('Ищем кнопку TMC...')
      main_wnd = find_match(None, ['images/Toyota EPC/TMC Part Number Translation/1.png', 'images/Toyota EPC/TMC Part Number Translation/2.png'], (178, 142, 184, 151), 100, False)
      
      if main_wnd:
        logging.debug('Нашли кнопку TMC Part Number Translation, далее считается, что окно находится на самом верху и мы находимся в главном меню')
        break
      else: 
        logging.debug('Не нашли кнопку TMC')
        raise 
    except Exception, exc:
      print exc
      sleep = sleep + 0.1
      logging.debug("Exception. Спим " + str(sleep) + " с. перед следущей итерацией goto_main_menu_toyota_epc")
      time.sleep(sleep)
      

  
  
def choose_region(area):
  logging.debug('choose_region("' + area + '")')
  
  areas = {
    'Europe': {'blue_point_y': 148}, 
    'General': {'blue_point_y': 165},
    'USA, Canada': {'blue_point_y': 181},
    'Japan': {'blue_point_y': 200}
  }
  
  goto_main_menu_toyota_epc()
  logging.debug("Теперь мы точно знаем, что находимся в главном меню, обрабатываемый регион " + str(area))
  
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
      wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Area).*")
      wmgr.set_foreground(False, False, False)
      logging.debug('Нашли окно TOYOTA...Area, сделали его активным')
      
      logging.debug('Ищем Setup the necessary items')   
      coords = find_match(False, ['images/Toyota EPC/Setup the necessary items.png'], (182, 350, 190, 361), 100, False)
      if coords:
        logging.debug('Теперь мы точно уверены, что окно выбора регионов открыто, т.к. нашли Setup the necessary items')
        break
      else:
        logging.debug("Генерируем исключение. Не удалось найти 'Setup the necessary items'")
        raise
    except:
      sleep = sleep + 0.1
      logging.debug("Exception. Спим " + str(sleep) + " с. перед следущей итерацией поиска окна регионов с Setup the necessary items")
      time.sleep(sleep)

  sleep = 0.1
  
  while True:
    try:
      time.sleep(sleep) # Обязательно
      click(130, areas[area]['blue_point_y'])
      time.sleep(sleep) # Обязательно        
      img = ImageGrab.grab((158, 135, 159, 252))
      img = img.convert("RGBA")
      pixdata = img.load()

      if(pixdata[0, areas[area]['blue_point_y'] - 135] == (10, 36, 106, 255)):
        logging.debug('Проверка синей полоски прошла успешно, регион действительно выбран')
        break
      else:
        logging.debug('В процессе клика на конкретном регионе и последующей проверкой синей полоски произошла ошибка')
        raise
    except:
      sleep = sleep + 0.1
      logging.debug("Спим " + str(sleep) + " с. перед следущей итерацией проверки факта того что мы щелкнули на базе заранее известных координат синих точек")
      time.sleep(sleep)

  # ДАЛЕЕ НЕ ПРОВЕРЯЛ TODO
  wsh.SendKeys("{F8}")
  
  #if (some_method(vin_code) == True):
  #  im = ImageGrab.grab((0, 0, 1030, 745))
  #  im.save('static/vin/' + area + "/" + vin_code + ".png")
  #  areas[area]['Found'] = "<img src='http://192.168.2.9:5000/static/vin/" + area + "/" + vin_code + ".png'>"
  

def search_applicability_in_current_area(catalog_number):
  pass
  


wsh = comclt.Dispatch("WScript.Shell")  
  
for item in ps.listen():
  #pdb.set_trace()
  data = json.loads(item['data'])
  print data
  print ''
  
  manufacturer = data['data']['data']['manufacturer']
  catalog_number = data['data']['data']['catalog_number']  
  caps = data['caps']
  
  if manufacturer == "TOYOTA":
    if caps == "Toyota EPC":
      logging.debug('Проверяем, есть ли на этой машине Toyota EPC.')
      if config['Toyota EPC']['present']:
        logging.debug('Судя по настройке в конфиге - есть')
        area = data['area']
        command = data['command']
        key = "%s:%s:%s:%s:%s" % (command, catalog_number, manufacturer, caps, area)
        logging.debug('Ключ lock:' + str(key))
        if(rs.setnx('lock:' + key, 1)):
          rs.expire('lock:' + key, 10)
          if command == 'applicability':
            check_or_start_toyota_epc()
            choose_region(area)
            search_applicability_in_current_area(catalog_number)
            #post_process_allow_origin(jsonify(time=str(catalog_number)))
          if command == 'images etc... ':
            pass
          if command == 'substitution etc...':
            pass
          if command == 'procurement...':
            pass

    elif caps == "Tecdoc":
      '''
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
      '''    
      
  elif manufacturer == "MITSUBISHI":
    pass
  else:
    pass
  
  
  #if rs.setnx(data['data']['url'], 1):
  #  #print '1'
  #  rs.expire(data['data']['url'], 10)
  #else:
  #  print '2'