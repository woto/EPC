﻿#coding=UTF-8

import redis, json, sys, logging, pdb, sys, os, re, time, random, shutil, subprocess, Image, ImageChops, time, math, random, pdb, win32api, win32con

import win32clipboard
import win32com.client as comclt
from window_mgr import WindowMgr
from functions import * 
from seed_vin import *
from tecdoc_manufacturer_alias import *
from juggernaut import Juggernaut
from config import *

import pyscreenshot as ImageGrab

key = ''

rs = redis.Redis(config['Redis'])
jug = Juggernaut(rs)
ps = rs.pubsub()
ps.subscribe('bee')

#rc.publish('foo', 'hello world')

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
  time.sleep(0.1)
  #TODO пока что это в зависимости от нужды и работоспособности, (потому что кажется можно обойтись банальным слипом) оставлю или изменю позже сейчас же разбираюсь с корректностью открытия поиска подходящих модеделей по детали и видимо окно не успевает закрыться до того момента, как мы уже пытаемся щелкнуть на кнопке вызывающем окно поиска подходящих моделей

  logging.debug("Вызываем метод выхода в главное меню непосредственно после выбора региона")
  goto_main_menu_toyota_epc()
  
  #  im.save('static/vin/' + area + "/" + vin_code + ".png")
  #  areas[area]['Found'] = "<img src='http://192.168.2.9:5000/static/vin/" + area + "/" + vin_code + ".png'>"  

def search_applicability_in_current_area(catalog_number, data):

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
  
  
  sended_models = []
  uniq_catalog_code = []
  scroll_avaliable_first_check = True
  scroll_avaliable = False
  bottom_counter = 0
  
  while True:
    time.sleep(0.3)
    logging.debug("Вертимся в цикле поиска подходящих моделей.")
    # TODO херня какая-то, должно быть 702, а работает только с 703 :\
    # выяснил, ошибки в размерах нет, это так работает метод opencv, обязательно потом хочу попробовать
    # выяснить проблему и решить. Пока можно обходить ситуацию заданием чуть большего размера.
    # Кстати интересно, что с буквами у меня такой ситуации не возникало
    
    coords = find_match(False, ['images/Toyota EPC/Select the next function by pressing an approriate PF key.png'], (326, 691, 334, 703), 100, False)
    if coords:
      logging.debug("Получили список подходящих моделей")
      
      time.sleep(0.1)
      logging.debug("Поспали 0.1")
      
      logging.debug("Грабим область экрана с результатом списка моделей")
      img = pil2gray(ImageGrab.grab((16, 351, 1014, 673)))

      logging.debug("Ищем серые точки")
      cv.SetImageROI(img, (0, 0, 1, img.height))
      tpl = cv.LoadImage('images/Toyota EPC/Search result delimiter point.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
      res = cv.CreateImage((cv.GetImageROI(img)[2] - tpl.width + 1, cv.GetImageROI(img)[3] - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
      cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF) 
      cv.ResetImageROI(img)
      
      lines = []
      for y in range(0, res.height):
        s = cv.Get2D(res, y, 0)
        if s[0] <= 10:
          lines.append(y)
      
      if lines:
        logging.debug("Найденные полоски " + str(lines) + ". Заходим в цикл перебора полосок")
        
        for y1, y2 in pairwise(lines):
          logging.debug("Крутимся в цилке прохода по полоскам")
          logging.debug("y1: " + str(y1) + " y2: " + str(y2))
          
          accumulator = []
          
          #a
          # Могу отсекать прямо здесь для начала
          #if (y1+4+16 >= y2):
          #  #pdb.set_trace()
          #  continue
            
          #b
          # Получается, что я закрашиваю соседнюю строку (решение) Ошибка возникает из-за того, что я беру top и независимо от всего
          # прибавляю к нему 11 (ниже)
          #if (y1+11 < 11):
          #  continue 
            
          for top in range(y1 + 4, y2, 16):
            logging.debug("Крутимся в цилке прохода по строкам внутри полоски, текущий верх: " + str(top))
            cv.SetImageROI(img, (0, top, 998, 11))
            
            if (float(y2-y1)/16 != (y2-y1)/16):
              continue
              
            # 1
            #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
            #cv.ShowImage('image', img)
            #cv.WaitKey(0)
            #pdb.set_trace()
            # 1
                    
            for element, first in pairs((('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('(', 'Open Bracket'), (')', 'Close Bracket'), (',', 'Comma'), ('#', 'Octothorpe'), ('-', 'Hyphen'), ('/', 'Slash'), ('&', 'And'), ('+', 'Plus'), (' | ', 'Delimiter'), ('.', 'Point'))):
              tpl = cv.LoadImage('images/Toyota EPC/Fonts/Main Font/' + str(element[1]) + '.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
                
              res = cv.CreateImage((cv.GetImageROI(img)[2] - tpl.width + 1, cv.GetImageROI(img)[3] - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
              cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)

              for y in range(0, res.height):
                for x in range(0, res.width):
                  s = cv.Get2D(res, y, x)
                  if s[0] <= 20:
                    accumulator.append({'x': x, 'y': top, 'letter': element[0]})
                    cv.Rectangle(img,
                        (x, y),
                        (x+tpl.width-1, y+tpl.height-1),
                    cv.Scalar(255, 255, 255, 255), cv.CV_FILLED)
                  x = x + tpl.width
                y = y + tpl.width

          if len(accumulator) > 0:
            tmp = ['']
            idx = 0
            accumulator = sorted(sorted(accumulator, key=lambda k: k['x']), key=lambda k: k['y'])
            #accumulator = sorted(accumulator, key=lambda k: k['x'])
            for i, letter in enumerate(accumulator):
              if((letter['x'] - accumulator[i-1]['x']) >= 15):
                tmp[idx] += " "
                #sys.stdout.write('\t')
              if((letter['y'] > accumulator[i-1]['y'])):
                idx = 0
              if(letter['letter'] == ' | '):
                #pdb.set_trace()
                tmp[idx] += '<br />'
                idx += 1
                tmp.append('')
                continue
              
              tmp[idx] += letter['letter']
              #sys.stdout.write(letter['letter'])
            
            
            # Этот способ возник после того, как я обнаружил, что полоска сверху рисуется всвегда, значит, вверху всегда будет
            # половинчатая полоска, если конечно на неё так попадет скролл, а следовательно мы получим только часть данных,
            # этого можно избежать, если убедиться в том, что в нулевом столбце присутствует порядковый номер, т.е. не пусто
            tmp = [x.strip() for x in tmp]
            if (tmp[0] != ''):
              if tmp[0] not in sended_models:
                #pdb.set_trace()
                sended_models.append(tmp[0])
                
                tmp[6] = tmp[6].replace(' ', '')
                tmp = filter(len, tmp)
                tmp = [x for x in tmp]
                
                if tmp[4] not in uniq_catalog_code:
                  rs.publish('bee', json.dumps({
                    'caps': 'Toyota EPC',
                    'manufacturer': data['manufacturer'],
                    'area': data['area'],
                    'command': 'get_precisely_info_by_car_catalog',
                    'catalog_number': data['catalog_number'],
                    'line': tmp
                  }))
                  uniq_catalog_code.append(tmp[4])

                rs.publish('queen', json.dumps({
                  'caps': 'Toyota EPC',
                  'manufacturer': data['manufacturer'],
                  'area': data['area'],
                  'command': 'part_number_application_to_models',
                  'catalog_number': data['catalog_number'],     
                  'line': tmp
                }))
      
        if scroll_avaliable_first_check:
          logging.debug("Единоразовая проверка наличия скролла на 1 запрос каталожного(ых) номера(ов)")
          scroll_avaliable_first_check = False
          logging.debug("Проверяем, а нет ли случайно скролла в результатах поиска")
          if (find_match(False, ['images/Toyota EPC/Scroll down.png'], (1005, 653, 1006, 673), 100, False)):
            logging.debug("Скролл обнаружен")
            scroll_avaliable = True
          else:
            logging.debug("Скролл не обнаружен")
        
        if scroll_avaliable:
        
          if bottom_counter < 2:
          
            # Уменьшил правый x на 1. Было 997
            logging.debug("Запоминаем нижнюю часть экрана")
            tpl_gray = pil2gray(ImageGrab.grab((16, 351+lines[-2], 996, 673)))

            #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
            #cv.ShowImage('image', tpl_gray)
            #cv.WaitKey(0)                

            logging.debug("Нажимаем на скролл вниз")
            click(1005, 656)
            time.sleep(0.1)
            logging.debug("Поспали 0.1")
            
            logging.debug("Проверяем не находимся ли мы в самому низу")
            coords = find_match(False, ['images/Toyota EPC/Scroll at bottom.png'], (993, 647, 1018, 673), 100, False)
            
            if not coords:
              logging.debug("Нет, не находимся")
            else:
              bottom_counter += 1
              logging.debug("Да, находимся, прибавили bottom_counter и стало: " + str(bottom_counter))

            if bottom_counter == 2:
              logging.debug("bottom_counte == 2, это значит, что мы уже опускались вниз один раз, сейчас мы опустились второй, следовательно, необходимо просто распознать последнюю часть экрана и выйти, т.к. ЛОЖЬ == (bottom_counter < 2).")
              continue
            
            logging.debug("Следующим шагом заходим в цикл, в котором будем подниматься постепенно вверх, пока не найдем нижнюю область, запомненную ранее")
              
            while True:
              logging.debug("Возвращаемся назад щелчком на стрелку верхнего скролла")
              click(1005, 340)
              time.sleep(0.1)
              logging.debug("Поспали 0.1")
              
              img_gray = pil2gray(ImageGrab.grab((16, 351, 1014, 673)))
              
              res = cv.CreateImage((img_gray.width - tpl_gray.width + 1, img_gray.height - tpl_gray.height + 1), cv.IPL_DEPTH_32F, 1)
              cv.MatchTemplate(img_gray, tpl_gray, res, cv.CV_TM_SQDIFF)
              
              (minval, maxval, minloc, maxloc) = cv.MinMaxLoc(res)
              
              previous_roi = cv.GetImageROI(img_gray)
              cv.SetImageROI(img_gray, (minloc[0], minloc[1], tpl_gray.width, tpl_gray.height))

              #img_gray_copy = cv.CreateImage((cv.GetImageROI(img_gray)[2] - cv.GetImageROI(img_gray)[0], cv.GetImageROI(img_gray)[3] - cv.GetImageROI(img_gray)[1]), cv.IPL_DEPTH_8U, 1)
              #pdb.set_trace()
              #cv.Copy(img_gray, img_gray_copy)
              norm = -1
              norm = cv.Norm( img_gray, tpl_gray );

              cv.SetImageROI(img_gray, previous_roi)
              
              ## 2
              #cv.Rectangle(img_gray, 
              #  (minloc[0], minloc[1]),
              #  (minloc[0] + tpl_gray.width, minloc[1] + tpl_gray.height),
              #cv.Scalar(0, 1, 0, 0))
              #
              #
              #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
              #cv.ShowImage('image', img_gray)
              #
              #cv.NamedWindow('tpl', cv.CV_WINDOW_AUTOSIZE)
              #cv.ShowImage('tpl', tpl_gray)
              #
              #cv.WaitKey(0)
              #
              #cv.DestroyWindow('image')
              #cv.DestroyWindow('tpl')
              ## 2

              #print "minval: " + str(minval)
              #print "norm: " + str(norm)
              
              if (norm == 0):
                logging.debug("Нашли интересующую область, запомненную ранее")
                continue_iteration = True
                break
              
            if continue_iteration:
              logging.debug("Переходим к следующей итерации цикла по полоскам")
              continue
              
        logging.debug("Осуществляем возврат из метода")
        return

wsh = comclt.Dispatch("WScript.Shell")  

def search_in_tecdoc(catalog_number, manufacturer, data):

  check_or_start_tecdoc()
  i = 0
  
  while True:
    try:
      logging.debug('Сейчас мы ищем TECDOC, мы уже знаем, что он точно запущен, ищем его') 
      wmgr = WindowMgr()
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
          time.sleep(0.2)
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
                  #return post_process_allow_origin(jsonify(time="Ничего не нашли"))
                  return
                time.sleep(0.1)
            logging.debug('Ищем что-то там :), сообщающее, что каталожный номер найден') 
            coords = find_match(None, ['images/Tecdoc/Found Any.png'], (1128, 238, 1192, 258), 100, False)
            if coords:
              break_outer = False
              while True:
                click(1252, 916)
                # TODO тут сделать инкрементный слип
                time.sleep(0.1)
                im = ImageGrab.grab((875, 905, 876, 906))
                im = im.convert("RGBA")
                pixdata = im.load()
                
                if(pixdata[0, 0] == (0, 0, 0, 255)):
                  break_outer = True
                  break
              
              if break_outer:
                logging.debug('Нашли что-то там :)')
                
                if (tecdoc_manufacturer_alias.has_key(manufacturer)):
                  tecdoc_manufacturer = tecdoc_manufacturer_alias[manufacturer]
                else:
                  tecdoc_manufacturer = manufacturer
                wsh.SendKeys(tecdoc_manufacturer)
                time.sleep(0.2)
                wsh.SendKeys("{Enter}")
                time.sleep(0.2)
                wsh.SendKeys("^c", 0)
                time.sleep(0.2)
                win32clipboard.OpenClipboard()
                #win32clipboard.EmptyClipboard()
                data = win32clipboard.GetClipboardData()
                #win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
                click(868, 916)
                if(tecdoc_manufacturer != data):
                  print catalog_number
                  print tecdoc_manufacturer
                  print ''
                else:
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': tecdoc_manufacturer,
                    'command': 'specifically_number_info',
                    'catalog_number': catalog_number,
                    'bla': 'i need a dollar'
                  }))                  
                  
                #time.sleep(1)
                return

              #logging.debug('Граббим экран') 
              #im = ImageGrab.grab((207, 204, 1128, 890))
              #logging.debug('Сохраняем изображением в папке') 
              #im.save("./static/" + catalog_number + ".png")
              #logging.debug('Возвращаем результат')
              #return post_process_allow_origin(jsonify(time=str(catalog_number)))        

            time.sleep(0.1)
            
          logging.debug('По видимому столкнулись с проблематичной деталью')
          raise
        else:
          logging.debug('Не смогли убедиться, что снята галочка с "Любой номер"')
          raise
      else:
        logging.debug('Не нашли поставленную галочку на "Любой номер"')
        raise
    except Exception as exc:
      print type(exc)     # the exception instance
      print exc.args      # arguments stored in .args
      print exc           # __str__ allows args to printed directly 

    i = i + 0.3

for item in ps.listen():

  data = json.loads(item['data'])
    
  if data['caps'] == "Tecdoc":
    logging.debug('Проверяем, есть ли на этой машине Tecdoc.')
    if config['Tecdoc']['present']:
      logging.debug('Судя по настройке в конфиге - есть')
      if data['command'] == 'specifically_number_info':
        key = "%s:%s:%s:%s" % (data['command'], data['catalog_number'], data['caps'], data['manufacturer'])
        logging.debug('Ключ lock:' + str(key))
        if(rs.setnx('lock:' + key, 1)):
          rs.expire('lock:' + key, 300)
          search_in_tecdoc(data['catalog_number'], data['manufacturer'], data)
  elif data['caps'] == "Toyota EPC":
    logging.debug('Проверяем, есть ли на этой машине Toyota EPC.')
    if config['Toyota EPC']['present']:
      logging.debug('Судя по настройке в конфиге - есть')
      if data['command'] == 'get_precisely_info_by_car_catalog':
        #print 'Тут надо получать более точную инфорацию по каталожному номеру'
        pass
      elif data['command'] == 'part_number_application_to_models':
        key = "%s:%s:%s:%s:%s" % (data['command'], data['catalog_number'], data['caps'], data['manufacturer'], data['area'])
        logging.debug('Ключ lock:' + str(key))
        if(rs.setnx('lock:' + key, 1)):
          rs.expire('lock:' + key, 300)

          check_or_start_toyota_epc()
          choose_region(data['area'])
          search_applicability_in_current_area(data['catalog_number'], data)

      elif data['command'] == 'testing':
        print data
        pass
        
      elif data['command'] == 'images etc... ':
        pass
        
      elif data['command'] == 'substitution etc...':
        pass
        
      elif data['command'] == 'procurement...':
        pass

  else:
    pass