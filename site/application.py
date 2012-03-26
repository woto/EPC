#coding=UTF-8


                    
                    
                    
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



  
@app.route('/json/toyota_substitution/<catalog_number>/')
def toyota_substitution(catalog_number):
  logging.debug('toyota_substitution')
  
  wmgr = WindowMgr()
  wmgr.minimize_all_windows()
  check_or_start_toyota_epc()
  
  return post_process_allow_origin(jsonify(time=str(catalog_number)))

  


@app.route('/json/vin/<vin_code>/')
def vin(vin_code):
  logging.debug('vin')
  
  check_or_start_toyota_epc()
  #goto_main_menu_toyota_epc()
  
  print "Searching " + str(vin)

  areas = in_each_region(search_vin_in_current_area, vin_code)
  
  return post_process_allow_origin(jsonify(time=str(areas))) 
  
  
  
  
@app.route('/json/info/<catalog_number>/', defaults={'manufacturer': None})
@app.route('/json/info/<catalog_number>/<manufacturer>')
def info(catalog_number, manufacturer):
  logging.debug('info')
  
  # На случай с FRI.TECH. когда Rails почему-то делает не .../catalog_number/manufacturer, a .../catalog_number?manufacturer=manufacturer
  if (manufacturer == None):
    manufacturer = request.args.get('manufacturer', '')  
  
  logging.debug('Проверяем наличие закешированной картинки') 
  if os.path.exists("./static/" + catalog_number + ".png"):
    logging.debug('Нашли и показали') 
    return post_process_allow_origin(jsonify(time=str(catalog_number))) 
    
  wmgr = WindowMgr()
  wmgr.minimize_all_windows()    

  if manufacturer == "TOYOTA":
  
    raise('Moved')
        
  else:
    raise('Moved')
  logging.debug('Безусловный возврат результата.') 
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
  app.run()
