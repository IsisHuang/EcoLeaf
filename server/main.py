# import Pyramid
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response

import psycopg2
import serial
import time

from pyramid.paster import get_app, setup_logging
ini_path = 'production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')

from google.appengine.ext import vendor
vendor.add('lib')

# set up the serial line
ser = serial.Serial('COM3', 9600)
time.sleep(2)

# connect to database
conn = psycopg2.connect(
database='DATABASE',
user='USER',
host='HOST',
port=8000
)

""" Helper Functions """

def send_biometric():
  data =[]                      
  for i in range(50):
    byte = ser.readline()       
    string_n = byte.decode() 
    string = string_n.rstrip() 
    flt = float(string)       
    print(flt)
    data.append(flt)          
    time.sleep(0.1)          

  for line in data:
    conn.set_session(autocommit=True)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO biometric (heatindex) VALUES (%s)", line)
    print(line)
  ser.close()

def create_plot(data):
  import matplotlib.pyplot as plt
  import pandas as pd
  plt.plot(data)
  plt.xlabel('Time (seconds)')
  plt.ylabel('Heat Index')
  plt.title('Reading of Heat Index')

  series = pd.Series([1, 2, 3])
  fig, ax = plt.subplots()
  series.plot.bar()
  fig.savefig('my_plot.png')

""" Routes """

def ecoleaf_ui_route(req):
  return render_to_response('template/ecoleaf_ui.html', [], request=req)

def get_biometric_route(req):
  import json
  send_biometric()
  conn.set_session(autocommit=True)
  cursor = conn.cursor()
  cursor.execute("SELECT heatindex FROM biometric ORDER BY id DESC")
  data = cursor.fetchone()
  if data is None:
    return {'Response (server):':'State information unavailable'}
  else:
    heatindex=json.dumps(data)
    create_plot(heatindex)
    return Response(heatindex)

""" Main Entrypoint """

if __name__ == '__main__':
  with Configurator() as config:
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_route('ecoleaf_ui', '/')
    config.add_view(ecoleaf_ui_route, route_name='ecoleaf_ui')

    config.add_route('get_biometric', '/get_biometric')
    config.add_view(get_biometric_route, route_name='get_biometric', renderer='json')
    
    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()

  server = make_server('0.0.0.0', 1234, app)
  print('Web server started on: http://0.0.0.0:8000 OR http://localhost:8000')
  server.serve_forever()
