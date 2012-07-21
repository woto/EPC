﻿#coding=UTF-8

import StringIO, urllib2, pdb
import pyscreenshot as ImageGrab
import win32api, win32con
from itertools import izip, tee
import cv
import pyscreenshot as ImageGrab
import os, re, logging, time
from window_mgr import WindowMgr
from config import *

from poster.encode import multipart_encode
from poster.encode import MultipartParam
from poster.streaminghttp import register_openers



logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.DEBUG, 
                    filename='../logs/application.log')

def prepare_textcatch():
  sleep = 0.1
  while True:
    break_outer_loop = False
    time.sleep(sleep)
    coords = find_match(False, ['images/TextCatch/Sight.png'], None, 100, False)
    time.sleep(sleep)
    if coords:
      time.sleep(sleep)
      click(coords[0], coords[1])
      #while True:
      #  time.sleep(sleep)
      #  coords = find_match(False, ['images/TextCatch/choose_window.png'], None, 100, False)
      #  if coords:
      #    break_outer_loop = True
      #    break
      #  sleep += 0.1
      time.sleep(0.5)
      break
      #print break_outer_loop
      #if break_outer_loop:
      #  break
    sleep += 0.1
    
def check_or_start_text_catch():
  logging.debug('check_or_start_text_catch')
  wmgr = WindowMgr()
  logging.debug('Проверяем запущен ли вообще TextCatch') 
  wmgr.find_window_wildcard("TextCatch(.*)")
  if len(wmgr._handle) == 0:  
    logging.debug('Нет, запускаем')
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", config['TextCatch']['path']).group(0))
    os.startfile(config['TextCatch']['path'])
    os.chdir(origWD)
  wmgr.set_foreground(False, True, True, 0)
  logging.debug("Вышли из метода проверки запущенности TextCatch. Далее считается, что TextCatch запущен")

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
                    
def check_or_start_febest():
  logging.debug('check_or_start_febest')
  wmgr = WindowMgr()
  logging.debug('Проверяем запущено ли вообще Febest') 
  wmgr.find_window_wildcard("(.*)Febest")
  if len(wmgr._handle) == 0:  
    logging.debug('Нет, запускаем')
    origWD = os.getcwd()
    os.chdir(re.search("(.*)\/", config['Febest']['path']).group(0))
    os.startfile(config['Febest']['path'])
    os.chdir(origWD)
    logging.debug('Запустили Febest, сменили рабочую директорию обратно') 
    while True:
      coords = find_match(False, ['images/Febest/OK.png'], (697, 588, 720, 608), 10, False)
      logging.debug('Ищем кнопку ОК на первом экране') 
      break_upper_2 = False
      if coords:
        logging.debug('Нашли')
        break_upper = False
        while True:
          logging.debug('Нажимаем на кнопку на первом экране')
          time.sleep(0.3)
          click(708, 598)
          for i in range(20):
            coords = find_match(False, ['images/Febest/OK.png'], (697, 588, 720, 608), 10, False)
            
            logging.debug('Ищем кнопку ОК на втором экране: ' + str(i) + " раз") 
            if coords:
              logging.debug('Нашли') 
              time.sleep(0.3)
              click(801, 598)
              break_upper = True
              break
            else:
              logging.debug('Не нашли, спим') 

          logging.debug("Количество попыток найти кнопку ОК на втором экране превысило допустимое кол-во, произойдет следующая итерация")              
              
          if break_upper:
            break_upper_2 = True
            break
              
      if break_upper_2:
        break
          
      else:
        logging.debug('Не нашли, спим') 
      
  logging.debug("Вышли из метода проверки запущенности Febest. Далее считается, что Febest запущен")

def find_match(file_name, template_array, roi, minimal, debug):

  if not file_name:
    file_name = 'img.png'
    if roi:
      im = ImageGrab.grab(roi)
    else:
      im = ImageGrab.grab()
    im.save(file_name)


  img = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)
  cv.SetData(img, im.tostring(), im.size[0]*3)
  cv.CvtColor(img, img, cv.CV_RGB2BGR)      
  
  for id, template in enumerate(template_array):
    tpl = cv.LoadImage(template, cv.CV_LOAD_IMAGE_COLOR)
  
    res = cv.CreateImage((img.width - tpl.width + 1, img.height - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
    cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)
    (minval, maxval, minloc, maxloc) = cv.MinMaxLoc(res)

    if debug:
      print "minval:" + str(minval)
      print "maxval:" + str(maxval)
      print '"' + template + '": ' + str(minloc)
      print ""

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
      return [minloc[0], minloc[1]]

def move(x, y):  
  win32api.SetCursorPos((x,y))

def drag_drop((x1, y1), (x2, y2)):
  win32api.SetCursorPos((x1,y1))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1, y1, 0, 0)
  win32api.SetCursorPos((x2,y2))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2, y2, 0, 0)
  
def click(x, y):  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def pairs(lst):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first  

def pairwise(iterable):
  "s -> (s0,s1), (s1,s2), (s2, s3), ..."
  a, b = tee(iterable)
  next(b, None)
  return izip(a, b)
  
#def handleRemoveReadonly(func, path, exc):
#  excvalue = exc[1]
#  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
#      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
#      func(path)
#  else:
#      raise

def pil2gray(img_pil):
  img_rgb = cv.CreateImageHeader(img_pil.size, cv.IPL_DEPTH_8U, 3)
  cv.SetData(img_rgb, img_pil.tostring(), img_pil.size[0]*3)
  img_gray = cv.CreateImage(img_pil.size, cv.IPL_DEPTH_8U, 1)
  cv.CvtColor(img_rgb, img_gray, cv.CV_RGB2GRAY)
  return img_gray

def put_screenshot_to_webdis(catalog_number, manufacturer):
  im = ImageGrab.grab()
  
  im = ImageGrab.grab()
  fil=StringIO.StringIO()
  im.save(fil,"png")
  
  # Register the streaming http handlers with urllib2
  register_openers()

  # Start the multipart/form-data encoding of the file "DSC0001.jpg"
  # "image1" is the name of the parameter, which is normally set
  # via the "name" parameter of the HTML <input> tag.

  # headers contains the necessary Content-Type and Content-Length
  # datagen is a generator object that yields the encoded parameters
  
  #mp1 = MultipartParam("Filename", name + ".png")
  
  mp1 = MultipartParam("parts_image[catalog_number]", catalog_number)
  mp2 = MultipartParam("parts_image[manufacturer]", manufacturer)
  mp3 = MultipartParam("parts_image[part_image]", filename=catalog_number + ":" + manufacturer + ".png", filetype="application/octet-stream", fileobj=fil)

  datagen, headers =  multipart_encode([mp1, mp2, mp3])

  # Create the Request object
  request = urllib2.Request("http://" + config['Parts Images Address'] + "/parts_images.json", datagen, headers)

  # Actually do the request, and get the response
  return urllib2.urlopen(request).read()