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
from juggernaut import Juggernaut


logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.DEBUG, 
                    filename='../logs/application.log')
key = ''

rs = redis.Redis(config['Redis'])
jug = Juggernaut(rs)
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
  
  logging.debug("Вызываем метод выхода в главное меню")
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
    logging.debug("Зашли в цикл проверки факта выделения и соответствующего поиска синенькой полоски")
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

  logging.debug("Отправляем F8 - выбор и закрытие окна выбора региона")
  wsh.SendKeys("{F8}")
  #TODO пока что это в зависимости от нужды и работоспособности, (потому что кажется можно обойтись банальным слипом) оставлю или изменю позже сейчас же разбираюсь с корректностью открытия поиска подходящих модеделей по детали и видимо окно не успевает закрыться до того момента, как мы уже пытаемся щелкнуть на кнопке вызывающем окно поиска подходящих моделей

  logging.debug("Вызываем метод выхода в главное меню непосредственно после выбора региона")
  goto_main_menu_toyota_epc()
  
  #  im.save('static/vin/' + area + "/" + vin_code + ".png")
  #  areas[area]['Found'] = "<img src='http://192.168.2.9:5000/static/vin/" + area + "/" + vin_code + ".png'>"
  

def search_applicability_in_current_area(catalog_number, cookie):

  # TODO этот блок скопирован с блока открытия окна выбора регионов

  sleep = 0.1
  
  while True:
    try:
      logging.debug("Нахдимся внутри цикла щелканья на кнопку Part Number Application to Models")
      logging.debug("Щелкаем на Part Number Application to Models в главном меню")
      click(254, 175)
      logging.debug("Щелкнули на Part Number Application to Models в главном меню")
      time.sleep(sleep) # Обязтаельно
      logging.debug('Ищем любое окно TOYOTA...Part Number Application to Models')
      time.sleep(sleep) # Обязательно
      wmgr = WindowMgr()
      wmgr.find_window_wildcard(".*TOYOTA ELECTRONIC PARTS CATALOG(.*Part Number Application to Models).*")
      wmgr.set_foreground(False, False, False)
      logging.debug('Нашли окно TOYOTA...Part Number Application to Models, сделали его активным')
      
      
      logging.debug('Ищем Enter part numbers and press F10 key')   
      coords = find_match(False, ['images/Toyota EPC/Enter part numbers and press F10 key.png'], (389, 692, 397, 703), 100, False)
      if coords:
        logging.debug('Теперь мы точно уверены, что окно поиска моделей по каталожному номеру открыто, т.к. нашли Enter part numbers and press F10 key')
        break
      else:
        logging.debug("Генерируем исключение. Не удалось найти 'Enter part numbers and press F10 key'")
        raise
    except:
      sleep = sleep + 0.1
      logging.debug("Exception. Спим " + str(sleep) + " с. перед следущей итерацией поиска окна поиска моделей по каталожному номеру")
      time.sleep(sleep)
  
  
  # TODO опять же, этот блок скопирован с старого раздела поиска по вин коду, потом возможно вынесу просто в метод.
  logging.debug("Магия с раскладкой")
  win32api.SendMessage(0xFFFF, 0x50, 1, 0x4090409)
  logging.debug("Спим перед набором каталожного номера")
  time.sleep(0.2)
  logging.debug("Печатаем каталожный номер " + str(catalog_number))
  wsh.SendKeys(str(catalog_number))
  logging.debug("Спим перед нажатием на Entrer")
  time.sleep(0.2)
  logging.debug("Жмем Enter")
  wsh.SendKeys("{ENTER}")
  logging.debug("Жмем F10")
  wsh.SendKeys("{F10}")
  logging.debug("Вбили каталожный номер, нажали Enter и F10")
  
  while True:
    time.sleep(0.3)
    logging.debug("Вертимся в цикле поиска подходящих моделей.")
    # TODO херня какая-то, должно быть 702, а работает только с 703 :\
    # выяснил, ошибки в размерах нет, это так работает метод opencv, обязательно потом хочу попробовать
    # выяснить проблему и решить. Пока можно обходить ситуацию заданием чуть большего размера.
    # Кстати интересно, что с буквами у меня такой ситуации не возникало
    
    coords = find_match(False, ['images/Toyota EPC/Select the next function by pressing an approriate PF key.png'], (326, 691, 334, 703), 100, False)
    if coords:
      #print coords
      logging.debug("Получили список подходящих моделей")

      #print 'start: ' + str(time.time())

      #img = cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_COLOR)
      
      im = ImageGrab.grab((16, 351, 998, 673))
      img_rgb = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)
      cv.SetData(img_rgb, im.tostring(), im.size[0]*3)
      img = cv.CreateImage((982, 322), cv.IPL_DEPTH_8U, 1)
      cv.CvtColor(img_rgb, img, cv.CV_RGB2GRAY)  
      # тут img_rgb и im уже не нужны, не знаю что там с памятью

      logging.debug("Ищем серые полоски, а точнее точки - разделители (как выяснилось высота строк разнится)")
      cv.SetImageROI(img, (0, 0, 1, 673))
      tpl = cv.LoadImage('images/Toyota EPC/Search result delimiter point.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
      res = cv.CreateImage((cv.GetImageROI(img)[2] - tpl.width + 1, cv.GetImageROI(img)[3] - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
      cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)  
      lines = []
      for y in range(0, res.height):
        s = cv.Get2D(res, y, 0)
        if s[0] <= 10:
          lines.append(y)
      cv.ResetImageROI(img)

      #pdb.set_trace()
      logging.debug("Найденные полоски " + str(lines))
      for y1, y2 in pairwise(lines):
        logging.debug("Крутимся в цилке прохода по линейкам")
        logging.debug("y1: " + str(y1) + " y2: " + str(y2))
        for top in range(y1 + 4, y2, 16):
          print top
          accumulator = []
          logging.debug("Крутимся в цилке прохода по строкам внутри линейки, текущий верх: " + str(top))
          cv.SetImageROI(img, (0, top, 998, 11))
          
          #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
          #cv.ShowImage('image', img)
          #cv.WaitKey(0)
                  
          for element, first in pairs((('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('(', 'Open Bracket'), (')', 'Close Bracket'), (',', 'Comma'), ('#', 'Octothorpe'), ('-', 'Hyphen'), ('/', 'Slash'), (' | ', 'Delimiter'), ('.', 'Point'))):
            tpl = cv.LoadImage('images/Toyota EPC/Fonts/Main Font/' + str(element[1]) + '.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
            
            # Можно было бы эту проверку вынести вверх, учитывая, что в данном случае высота шрифта постоянная,
            # но... ради потомков :)
            #if y2 - y1 < tpl.height:
            #  break
              
            res = cv.CreateImage((cv.GetImageROI(img)[2] - tpl.width + 1, cv.GetImageROI(img)[3] - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
            cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)

            for y in range(0, res.height):
              for x in range(0, res.width):
                #print x, y
                s = cv.Get2D(res, y, x)
                #print s[0]
                if s[0] <= 10:
                  #print element[0]
                  accumulator.append({'x': x, 'y': top, 'letter': element[0]})
                  #print x, y 
                  #if debug:
                  cv.Rectangle(img,
                      (x, y),
                      (x+tpl.width-1, y+tpl.height-1),
                  cv.Scalar(255, 255, 255, 255), cv.CV_FILLED)

                  #cv.ResetImageROI(img)

                  #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
                  ##cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
                  #cv.ShowImage('image', img)
                  #cv.WaitKey(0)
                  ##cv.ShowImage('template', tpl)
                x = x + tpl.width
              y = y + tpl.width

          #time.sleep(0.1)
          
          #print time.time()
          #cv.DestroyWindow('template')

          #for f, s in pairs(accumulator):
          #  print s['letter'],

          #cv.ResetImageROI(img)

          #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
          ##cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
          #cv.ShowImage('image', img)
          ##cv.ShowImage('template', tpl)
          #
          #cv.WaitKey(0)

          #cv.DestroyWindow('image')
          print 'asdf'
          if len(accumulator) > 0:
            tmp = ''
            accumulator = sorted(sorted(accumulator, key=lambda k: k['x']), key=lambda k: k['y'])
            #accumulator = sorted(accumulator, key=lambda k: k['x']) 
            for i, letter in enumerate(accumulator):
              if((letter['x'] - accumulator[i-1]['x']) > 10):
                tmp += "&nbsp;" 
                #sys.stdout.write('\t')
              if((letter['x'] - accumulator[i-1]['x']) < 0):
                tmp += "<br />"
                #print ''
              tmp += letter['letter']
              #sys.stdout.write(letter['letter'])
              
            jug.publish(cookie, tmp + "<br />")
            #pdb.set_trace()
            print tmp 
            #print '' 
            #print 'end ' + str(time.time())
          
          #break      
      
      logging.debug("Проверяем, а нет ли случайно скролла в результатах поиска")
      coords = find_match(False, ['images/Toyota EPC/Scroll down.png'], (1005, 653, 1006, 673), 100, False)
    
      if coords:
        logging.debug("Действительно, есть, щелкаем по нему")
        click(1005, 656)
        continue
      
      return
    
    # TODO Тут блок, в котором надо проверить ситуацию в случае если модели не найдены
    #coords = find_match(False, ['Select the next function by pressing an approriate PF key.png'], (326, 691, 334, 702), 100, False)
    #if coords:
    #  logging.debug("Получили список подходящих моделей")
    #  find_app()
    #  break
  

  
  
  
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
   


wsh = comclt.Dispatch("WScript.Shell")  
  
for item in ps.listen():
  #pdb.set_trace()
  data = json.loads(item['data'])
  #print data
  #print ''
  
  manufacturer = data['data']['data']['manufacturer']
  catalog_number = data['data']['data']['catalog_number']  
  caps = data['caps']
  cookie = data['data']['data']['cookie']
  
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
          rs.expire('lock:' + key, 30)
          if command == 'applicability':
            check_or_start_toyota_epc()
            choose_region(area)
            #print str(catalog_number)
            
            jug.publish(cookie, "<b>" + area + "</b><br />")
            
            search_applicability_in_current_area(catalog_number, cookie)
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
