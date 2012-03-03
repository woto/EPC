import json
from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.datastructures import Headers


def make_json_app(import_name, **kwargs):
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app


app = make_json_app(__name__)

@app.route('/')
def hello_world():
  pyDict = {'one':1,'two':2}
  response = jsonify(pyDict)
  return response

if __name__ == '__main__':
  app.debug = True
  app.run()