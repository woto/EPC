import json
from lockfile import FileLock
import time, random
from functools import partial
from flask import Flask, jsonify, request
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.datastructures import Headers


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

@app.route('/info/<default:detail>')
def my_test(detail):
  lock = FileLock("./application.lock")
  with lock:
    print lock.path, 'is locked.'
    time.sleep(random.randrange(0, 10))
    return post_process_allow_origin(jsonify(itworks='yeah!'))

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
