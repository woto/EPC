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
import win32api, win32con
import win32com.client as comclt
import os

def move(x, y):  
  win32api.SetCursorPos((x,y))

  
def click(x, y):  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


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
def my_test(catalog_number, manufacturer):
  lock = FileLock("./application")
  with lock:
    wmgr = WindowMgr()

    # Проверяем запущено ли вообще приложение
    wmgr.find_window_wildcard("(.*)TECDOC(.*)")
    if len(wmgr._handle) == 0:
      sys.exit("TECDOC doesn't running.")
    wmgr.set_foreground()

    print '1'
    while True:
      # Ищем кнопку поиска и щелкаем по ней
      coords = find_match(None, ['images_tecdoc/Search Button.png'], None, 100, False)
      print 'cliced'
      if coords:
        click(coords[0], coords[1])
        move(0, 0)
        time.sleep(0.2)
        wsh.SendKeys(catalog_number)
        time.sleep(0.2)
        wsh.SendKeys("{ENTER}")
        time.sleep(1)
        while True:
          coords = find_match(None, ['images_tecdoc/Not Found.png', 'images_tecdoc/Found Any.png'], None, 100, False)
          if coords:
            return post_process_allow_origin(jsonify(time=time.time()))
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
