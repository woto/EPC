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
