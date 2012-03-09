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



import win32com.client as comclt
import os
from functions import *

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

@app.route('/info/<catalog_number>/<manufacturer>')
def info(catalog_number, manufacturer):
  lock = FileLock("./application")
  with lock:
    wmgr = WindowMgr()

    # Проверяем запущено ли вообще приложение
    wmgr.find_window_wildcard("(.*)TECDOC(.*)")
    if len(wmgr._handle) == 0:
      #sys.exit("TECDOC doesn't running.")
      origWD = os.getcwd()
      os.chdir("C:/TECDOC_CD/1_2012/pb/")
      os.startfile("C:/TECDOC_CD/1_2012/pb/tof.exe")
      os.chdir(origWD)
    else:
      wmgr.set_foreground()
    
    while True:
      # Ищем кнопку поиска и щелкаем по ней
      coords = find_match(None, ['images_tecdoc/Search Button.png'], None, 100, False)
      time.sleep(0.2)
      if coords:
        click(coords[0], coords[1])
        move(0, 0)
        time.sleep(0.2)
        wsh.SendKeys(catalog_number)
        time.sleep(0.2)
        wsh.SendKeys("{ENTER}")
        time.sleep(1)
        while True:
          coords = find_match(None, ['images_tecdoc/Not Found.png'], None, 100, False)
          if coords:
            wsh.SendKeys("{ESC}")
            return post_process_allow_origin(jsonify(time="Ничего не нашли"))
          coords = find_match(None, ['images_tecdoc/Found Any.png'], None, 100, False)
          if coords:
            im = ImageGrab.grab((200, 200, 1000, 1000))
            #im.save("tmp.png")
            print im.size[0]*2
            print im.size[1]*2
            im.resize((im.size[0]*2, im.size[1]*2)).save("tmp.png")
            img = Image.open("tmp.png")
            img = img.convert("RGBA")
            pixdata = img.load()

            # Clean the background noise, if color != white, then set to black.
            # change with your color
            for y in xrange(img.size[1]):
              for x in xrange(img.size[0]):
                if (pixdata[x, y] == (255, 255, 255, 255)) or (pixdata[x, y] == (0, 0, 0, 0)):
                  pixdata[x, y] = (1, 1, 1, 255)

            for y in xrange(img.size[1]):
              for x in xrange(img.size[0]):
                if pixdata[x, y] != (1, 1, 1, 255):
                  pixdata[x, y] = (255, 255, 255, 255)
                  

            img.save("tmp.png")
            print time.time()
            #subprocess.call(["C:/Program Files/Tesseract-OCR/tesseract.exe", "C:/EPC/site/wsgi/tmp.png", "C:/EPC/site/wsgi/1", "-l", "rus"], 0, None, None, None, None, None, False, True, None, None, False, None, 0)
            subprocess.call(["C:/Program Files/Tesseract-OCR/tesseract.exe", "C:/EPC/site/wsgi/tmp.png", "C:/EPC/site/wsgi/1", "-l", "rus"])
            print time.time()
            time.sleep(1)
            infile = open('1.txt', 'r')
            filestr = infile.read()
            infile.close
            return post_process_allow_origin(jsonify(time=str(catalog_number)+filestr))          
          
      time.sleep(0.3)
      break
    
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
