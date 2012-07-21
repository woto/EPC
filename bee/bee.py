#coding=UTF-8

import time, redis, json, sys, logging, pdb, sys, os, re, time, random, shutil, subprocess, Image, ImageChops, time, math, random, pdb, win32api, win32con
import win32clipboard
import win32com.client as comclt
from window_mgr import WindowMgr
from functions import *
from seed_vin import *
from tecdoc_manufacturer_alias import *
from juggernaut import Juggernaut
from config import *
import cgi

import pyscreenshot as ImageGrab

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


  # Этот workaround нужен для обработки номеров от нерадивых поставщиков,
  # которые указывают, производителя как Toyota, а номер совсем не Toyot'ы

  old_catalog_number = catalog_number

  if len(catalog_number) < 10:
    catalog_number = 'WRONG_NUMBER'

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

  catalog_number = old_catalog_number


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

      logging.debug("Далее проверяем количество полосок, более 1 или нет (другими словами есть ли результаты поиска)")

      # Единичка видимо потому что одна верхняя полоска всегда присутствует в области
      if len(lines) > 1:

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
                  if local_stub == False:
                    rs.publish('bee', json.dumps({
                      'caps': 'Toyota EPC',
                      'manufacturer': data['manufacturer'],
                      'area': data['area'],
                      'command': 'get_precisely_info_by_car_catalog',
                      'catalog_number': data['catalog_number'],
                      'data': tmp
                    }))
                  uniq_catalog_code.append(tmp[4])

                if local_stub == False:
                  rs.publish('queen', json.dumps({
                    'caps': 'Toyota EPC',
                    'manufacturer': data['manufacturer'],
                    'area': data['area'],
                    'command': 'part_number_application_to_models',
                    'catalog_number': data['catalog_number'],
                    'data': tmp
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

            # TODO DIRTY BUG WORKAROUND Необходим в том случае, когда три полоски с применимостью детали не помещаются в одно окно, позже буду переделывать склейкой скриншотов, эта проблема устранится.
            global_lock_counter_when_line_very_high = 0

            while True:
              global_lock_counter_when_line_very_high += 1
              if(global_lock_counter_when_line_very_high >= 10):
                continue_iteration = True
                break

              #print global_lock_counter_when_line_very_high
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

      else:
        logging.debug("Результаты поиска не найдены. Отправили пустышку, что в данном регионе поискали")
        if local_stub == False:
          rs.publish('queen', json.dumps({
            'caps': 'Toyota EPC',
            'manufacturer': data['manufacturer'],
            'area': data['area'],
            'command': 'part_number_application_to_models',
            'catalog_number': data['catalog_number'],
            'data': None
          }))

      logging.debug("Осуществляем возврат из метода")
      return

wsh = comclt.Dispatch("WScript.Shell")
# глобальная переменная - признак локальной заглушки
local_stub = config['Hornet']['local_stub']

def search_in_tecdoc(catalog_number, manufacturer, data):

  if(catalog_number == None or len(catalog_number) <= 0):
    catalog_number = 'WRONG_CATALOG_NUMBER'

  if(manufacturer == None or len(manufacturer) <= 0):
    manufacturer = 'WRONG_MANUFACTURER'

  check_or_start_tecdoc()
  sleep = 0

  while True:
    try:
      logging.debug('Сейчас мы ищем TECDOC, мы уже знаем, что он точно запущен, ищем его')
      wmgr = WindowMgr()
      wmgr.find_window_wildcard(".*TECDOC(.*)")

      logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
      time.sleep(sleep)
      wmgr.set_foreground(True, True, True)
      logging.debug('Считаем, что сделали TECDOC активным')

      logging.debug('Спим ' + str(sleep) + 'с. перед щелчком на увеличительном стекле (как выяснилось из внутренних разделов меню {а так же если не ошибаюсь при запуске}) мы не выходим на начальное требуемое состояние.')
      time.sleep(sleep)
      click(219, 53)

      logging.debug('Спим ' + str(sleep) + 'с. перед отправкой в него ESC')
      time.sleep(sleep)
      logging.debug('Нажимаем ESC')
      wsh.SendKeys("{ESC}")
      time.sleep(0.1) # Обязательно!

      logging.debug('Ищем поставленную галочку на "Любой номер"')
      coords = find_match(None, ['images/Tecdoc/Check Box - Checked.png'], (749, 104, 767, 121), 10, False)

      if coords:
        logging.debug('Нашли поставленную галочку на "Любой номер"')

        logging.debug('Спим ' + str(sleep) + 'с. перед перед снятием галочки с "Любой номер"')
        time.sleep(sleep)
        click(757, 113)
        time.sleep(0.1) # Обязательно!

        logging.debug('Спим ' + str(sleep) + 'с. перед проверкой, что мы действительно сняли галочку с "Любой номер"')
        time.sleep(sleep)
        coords = find_match(None, ['images/Tecdoc/Check Box - Unchecked.png'], (749, 104, 767, 121), 10, False)
        if coords:

          comparing_area = (209, 203, 1249, 877)
          logging.debug('Сохраняем предыдущий экран будь то результаты поиска или что-то другое...')
          previous_image = ImageGrab.grab(comparing_area)
          #previous_image.save('image_1.png')

          logging.debug('Убедились, что галочка "Любой номер снята", нажатием на кнопку поиска запчастей (Увеличительное стекло)')
          click(209, 43)

          logging.debug('Спим ' + str(sleep) + 'с. перед вводом каталожного номера')
          logging.debug('Вводим каталожный номер.')
          wsh.SendKeys(catalog_number)
          time.sleep(0.2)
          logging.debug('Нажимаем Enter.')
          wsh.SendKeys("{ENTER}")

          while True:
            logging.debug('Снимаем опять скриншот с результата поиска')
            current_image = ImageGrab.grab(comparing_area)
            diff = ImageChops.difference(previous_image, current_image)
            time.sleep(0.1)
            if (diff.getbbox() != None):
              logging.debug('Сравниваемые изображения разные, выходим из цикла')
              #current_image.save('image_2.png')
              #diff.save('diff.png')
              break

          #for i in range(1):
          if True:
            logging.debug('Ищем наличие, либо отсутсвтие информации по запчасти')

            logging.debug('Ищем окно, сообщающее, что каталожный номер не найден')
            coords = find_match(None, ['images/Tecdoc/Not Found.png'], (564, 466, 732, 584), 100, False)
            if coords:
              logging.debug('Нашли окно окно, сообщающее, что каталожный номер не найден')
              while True:
                logging.debug('Отправили в него ESC')
                wsh.SendKeys("{ESC}")
                time.sleep(0.1)
                logging.debug('Проверяем, чтобы окно скрылось')
                coords = find_match(None, ['images/Tecdoc/Not Found.png'], (564, 466, 732, 584), 100, False)
                if not coords:
                  logging.debug("Окно закрылось")
                  logging.debug("Отправляем пустые данные")
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': None
                  }))
                  return
                else:
                  logging.debug("Окно не закрылось")

            logging.debug('Ищем увеличительное стекло, означающее, что каталожный номер найден')
            coords = find_match(None, ['images/Tecdoc/Magnifier.png'], (224, 239, 243, 258), 100, False)
            if coords:
              logging.debug('Нашли увеличительное стекло')
              break_outer = False
              sleep = 0.1

              while True:

                logging.debug('Спим ' + str(sleep))
                time.sleep(sleep)
                logging.debug('Кликаем на выпадающем списке для просмотра всех найденных производителей')
                click(1252, 916)
                logging.debug('Кликнули, спим ' + str(sleep))
                time.sleep(sleep)
                im = ImageGrab.grab((875, 905, 876, 906))
                im = im.convert("RGBA")
                pixdata = im.load()

                logging.debug('Проверяем наличие нужного пикселя, т.е. что список действительно выпал')
                if(pixdata[0, 0] == (0, 0, 0, 255)):
                  logging.debug("Список отобразился, выходим из цикла, щелканья и нахождения выпадающего списка")
                  break

                logging.debug('Выход из цикла не произошел, прибавляем время, повторяем бесконечную итерацию по поиску выпавшего списка')
                sleep += 0.3

              if (tecdoc_manufacturer_alias.has_key(manufacturer)):
                tecdoc_manufacturer = tecdoc_manufacturer_alias[manufacturer]
              else:
                tecdoc_manufacturer = manufacturer

              logging.debug("Печатаем производителя в поле")
              #for char in tecdoc_manufacturer:
              #  wsh.SendKeys(char)
              wsh.SendKeys(tecdoc_manufacturer)
              # TODO не успевает! надо делать на проверках?!
              logging.debug("Спим")
              time.sleep(0.1)
              logging.debug("Нажимаем Enter")
              wsh.SendKeys("{Enter}")
              logging.debug("Спим")
              time.sleep(0.1)
              logging.debug("Копируем выделение")
              wsh.SendKeys("^c", 0)
              logging.debug("Спим")
              time.sleep(0.1)
              win32clipboard.OpenClipboard()
              #win32clipboard.EmptyClipboard()
              clipboard_data = win32clipboard.GetClipboardData()
              #win32clipboard.SetClipboardText(text)
              win32clipboard.CloseClipboard()
              logging.debug("Щелкаем в сторонке")
              click(868, 916)
              if(tecdoc_manufacturer != clipboard_data):
                logging.debug("Искомый и ни один из найденных производителей не совпали")
                # TODO тут тоже сделать возврат пустышки
                #print ''
                #print catalog_number
                #print tecdoc_manufacturer
                #print ''
                #pdb.set_trace()

                rs.publish('queen', json.dumps({
                  'caps': 'Tecdoc',
                  'manufacturer': data['manufacturer'],
                  'command': 'specifically_number_info',
                  'catalog_number': data['catalog_number'],
                  'data': None
                }))

              else:
                logging.debug("Искомый и доступный среди найденных производителей совпали")
                logging.debug("Делаем двойной клик на оранжевой полоске детали")
                click(391, 212)
                time.sleep(0.2)
                click(391, 212)

                # Порно
                
                tab_area = (192, 173, 1277, 225)

                time.sleep(2)                               
                
                rs.publish('queen', json.dumps({
                  'caps': 'Tecdoc',
                  'manufacturer': data['manufacturer'],
                  'command': 'specifically_number_info',
                  'catalog_number': data['catalog_number'],
                  'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                }))
                
                time.sleep(0.5)                  
                  
                check_or_start_text_catch()
                prepare_textcatch()
                time.sleep(1)
                click(600, 600)
                time.sleep(1)
                win32clipboard.OpenClipboard()
                time.sleep(1)                
                #win32clipboard.EmptyClipboard()
                clipboard_data = win32clipboard.GetClipboardData()
                time.sleep(1)                
                #win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()                
                time.sleep(1)                
                
                #pdb.set_trace()                
                
                time.sleep(0.5)                                  
                
                rs.publish('queen', json.dumps({
                  'caps': 'Tecdoc',
                  'manufacturer': data['manufacturer'],
                  'command': 'specifically_number_info_text',
                  'catalog_number': data['catalog_number'],
                  'data': cgi.escape(unicode(clipboard_data.decode('cp1251')))
                }))                
                
                time.sleep(0.5)                  
                  
                wmgr = WindowMgr()
                wmgr.find_window_wildcard(".*TECDOC(.*)")

                logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
                time.sleep(sleep)
                wmgr.set_foreground(True, True, True)                
                
                time.sleep(0.5)                  


                try:
                  coords = find_match(None, ['images/Tecdoc/Contact Address Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                  
                  time.sleep(0.5)                  
                  
                except:
                  pass

                try:
                  coords = find_match(None, ['images/Tecdoc/Construct Numbers Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))

                  time.sleep(0.5)                  
                  
                  check_or_start_text_catch()
                  prepare_textcatch()
                  time.sleep(1)
                  click(600, 600)
                  time.sleep(1)
                  win32clipboard.OpenClipboard()
                  time.sleep(1)                
                  #win32clipboard.EmptyClipboard()
                  clipboard_data = win32clipboard.GetClipboardData()
                  time.sleep(1)                
                  #win32clipboard.SetClipboardText(text)
                  win32clipboard.CloseClipboard()                
                  time.sleep(1)                
                  
                  #pdb.set_trace()                
                  
                  time.sleep(0.5)                  
                  
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info_text',
                    'catalog_number': data['catalog_number'],
                    'data': cgi.escape(unicode(clipboard_data.decode('cp1251')))
                  }))                
                  
                  time.sleep(0.5)                  
                  
                  wmgr = WindowMgr()
                  wmgr.find_window_wildcard(".*TECDOC(.*)")

                  logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
                  time.sleep(sleep)
                  wmgr.set_foreground(True, True, True)   
                  
                  time.sleep(0.5)                                    
                  
                except:
                  pass
                  

                try:
                  time.sleep(0.5)                                  
                  coords = find_match(None, ['images/Tecdoc/Use in Autos Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                  
                  time.sleep(0.5)                                    
                  
                  check_or_start_text_catch()
                  prepare_textcatch()
                  time.sleep(1)
                  click(600, 600)
                  time.sleep(1)
                  win32clipboard.OpenClipboard()
                  time.sleep(1)                
                  #win32clipboard.EmptyClipboard()
                  clipboard_data = win32clipboard.GetClipboardData()
                  time.sleep(1)                
                  #win32clipboard.SetClipboardText(text)
                  win32clipboard.CloseClipboard()                
                  time.sleep(1)                
                  
                  #pdb.set_trace()                
                  
                  time.sleep(0.5)                  
                  
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info_text',
                    'catalog_number': data['catalog_number'],
                    'data': cgi.escape(unicode(clipboard_data.decode('cp1251')))
                  }))                
                  
                  time.sleep(0.5)                  
                  
                  wmgr = WindowMgr()
                  wmgr.find_window_wildcard(".*TECDOC(.*)")

                  logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
                  time.sleep(sleep)
                  wmgr.set_foreground(True, True, True)                    
                  
                  time.sleep(0.5)                                    
                  
                except:
                  pass
                  
                  time.sleep(0.5)                  
                  
                try:
                  coords = find_match(None, ['images/Tecdoc/Photo Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                except:
                  pass
                  
                  time.sleep(0.5)                  
                  
                try:
                  coords = find_match(None, ['images/Tecdoc/Pitcure Tab.png'], (192, 173, 1277, 225), 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                except:
                  pass
                  
                  time.sleep(0.5)                  
                  
                try:
                  coords = find_match(None, ['images/Tecdoc/Use in Engines Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                  
                  time.sleep(0.5)                                    
                  
                  check_or_start_text_catch()
                  prepare_textcatch()
                  time.sleep(1)
                  click(600, 600)
                  time.sleep(1)
                  win32clipboard.OpenClipboard()
                  time.sleep(1)                
                  #win32clipboard.EmptyClipboard()
                  clipboard_data = win32clipboard.GetClipboardData()
                  time.sleep(1)                
                  #win32clipboard.SetClipboardText(text)
                  win32clipboard.CloseClipboard()                
                  time.sleep(1)                
                  
                  #pdb.set_trace()                
                  time.sleep(0.5)                  
                  
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info_text',
                    'catalog_number': data['catalog_number'],
                    'data': cgi.escape(unicode(clipboard_data.decode('cp1251')))
                  }))  

                  time.sleep(0.5)                  
                  
                  wmgr = WindowMgr()
                  wmgr.find_window_wildcard(".*TECDOC(.*)")

                  logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
                  time.sleep(sleep)
                  wmgr.set_foreground(True, True, True)                    
                  
                  time.sleep(0.5)
                  
                except:
                  pass

                try:
                  coords = find_match(None, ['images/Tecdoc/Techincal Image Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                except:
                  pass

                try:
                  coords = find_match(None, ['images/Tecdoc/Picture Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                except:
                  pass

                try:
                  coords = find_match(None, ['images/Tecdoc/Specification Tab.png'], tab_area, 500, False)
                  click(coords[0]+tab_area[0], coords[1]+tab_area[1])
                  time.sleep(2)
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info',
                    'catalog_number': data['catalog_number'],
                    'data': put_screenshot_to_webdis(data['catalog_number'], data['manufacturer'])
                  }))
                  
                  time.sleep(0.5)
                  
                  check_or_start_text_catch()
                  prepare_textcatch()
                  time.sleep(1)
                  click(600, 600)
                  time.sleep(1)
                  win32clipboard.OpenClipboard()
                  time.sleep(1)                
                  #win32clipboard.EmptyClipboard()
                  clipboard_data = win32clipboard.GetClipboardData()
                  time.sleep(1)                
                  #win32clipboard.SetClipboardText(text)
                  win32clipboard.CloseClipboard()                
                  time.sleep(1)                
                  
                  #pdb.set_trace()                
                  
                  rs.publish('queen', json.dumps({
                    'caps': 'Tecdoc',
                    'manufacturer': data['manufacturer'],
                    'command': 'specifically_number_info_text',
                    'catalog_number': data['catalog_number'],
                    'data': cgi.escape(unicode(clipboard_data.decode('cp1251')))
                  }))                
                  
                  wmgr = WindowMgr()
                  wmgr.find_window_wildcard(".*TECDOC(.*)")

                  logging.debug('Спим ' + str(sleep) + 'с. перед тем как сделать активным TECDOC')
                  time.sleep(sleep)
                  wmgr.set_foreground(True, True, True)                    
                  
                  time.sleep(0.5)
                  
                except:
                  pass

                #time.sleep(1)
                #
                #logging.debug("Отправляем пока что пустышку")
                #
                #rs.publish('queen', json.dumps({
                #  'caps': 'Tecdoc',
                #  'manufacturer': data['manufacturer'],
                #  'command': 'specifically_number_info',
                #  'catalog_number': data['catalog_number'],
                #  'data': collector
                #}))

              logging.debug("Возврат из метода")
              return
            else:
              logging.debug("Иконка увеличительного стекла, означающее, что каталожный номер найден, не найдена")

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
      exc_type, exc_object, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print (exc, exc_type, fname, exc_tb.tb_lineno)
      sleep = sleep + 0.3

# точка выполнения программы
if local_stub:
  logging.debug('Начало')
  # цикл работы пока в одной задаваемом регионе
  # позже можно сделать перебор регионов
  local_stub_areas = ['Europe', 'General', 'USA, Canada', 'Japan']
  data = {
    'manufacturer': 'manufacturer',
    'area': local_stub_areas[0],
    'catalog_number': '0446505221'
  }

  check_or_start_toyota_epc()
  choose_region(data['area'])
  search_applicability_in_current_area(data['catalog_number'], data)

  #pdb.set_trace()
else:
  while True:
    try:
        logging.debug('Начало')
        key = ''

        logging.debug('Подключаемся к Редис')
        #pdb.set_trace()
        rs = redis.StrictRedis(config['Redis'], socket_timeout=config['Redis socket_timeout'])
        logging.debug('Подключаемся к Джаггернаут')
        jug = Juggernaut(rs)
        logging.debug('Создаем паб/саб объект')
        ps = rs.pubsub()
        logging.debug('Выбираем нужные канал')
        ps.subscribe('bee')

        #rc.publish('foo', 'hello world')

        logging.debug('Заходим в цикл прослушивания канала')
        #pdb.set_trace()
        for item in ps.listen():
          logging.debug('Что-то пришло в канале')

          data = json.loads(item['data'])
          print data

          if data['caps'] == "Tecdoc":
            logging.debug('Проверяем, есть ли на этой машине Tecdoc.')
            if config['Tecdoc']['present']:
              logging.debug('Судя по настройке в конфиге - есть')
              logging.debug('раз')
              if data['command'] == 'specifically_number_info':
                logging.debug('два')
                key = "%s:%s:%s:%s" % (data['command'], data['catalog_number'], data['caps'], data['manufacturer'])
                logging.debug('три')
                logging.debug('Ключ lock:' + key.encode('utf-8', 'replace'))
                if(rs.setnx('lock:' + key, 1)):
                  logging.debug('четыре')
                  rs.expire('lock:' + key, config['Redis lock_key_ttl'])
                  logging.debug('пять')
                  search_in_tecdoc(data['catalog_number'], data['manufacturer'], data)
                  logging.debug('шесть')
          elif data['caps'] == "Toyota EPC":
            logging.debug('семь')
            logging.debug('Проверяем, есть ли на этой машине Toyota EPC.')
            if config['Toyota EPC']['present']:
              logging.debug('восемь')
              logging.debug('Судя по настройке в конфиге - есть')
              if data['command'] == 'get_precisely_info_by_car_catalog':
                  logging.debug('девять')
                  #print 'Тут надо получать более точную инфорацию по каталожному номеру'
                  pass
              elif data['command'] == 'part_number_application_to_models':
                  logging.debug('десять')
                  key = "%s:%s:%s:%s:%s" % (data['command'], data['catalog_number'], data['caps'], data['manufacturer'], data['area'])
                  logging.debug('одиннадцать')
                  logging.debug('Ключ lock:' + str(key))
                  if(rs.setnx('lock:' + key, 1)):
                    logging.debug('двенадцать')
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

          # Если ветвится запрос по одной детали (например регионы Тойоты, то запишется после первой обработки ветви)
          # Перенес сюда из Queen
          rs.set('t:' + data['catalog_number'] + ":" + data['manufacturer'], str(int(time.time() * 1000)));

          logging.debug("Итерация внутри пс.листен завершена")

    except Exception, exc:
      exc_type, exc_object, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print (exc, exc_type, fname, exc_tb.tb_lineno)
      print time.time()
      #time.sleep(1)
