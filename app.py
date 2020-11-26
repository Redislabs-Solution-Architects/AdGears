from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from redistimeseries.client import Client as RedisTimeseries


# From our local file
from load_data import load_data

from os import environ

import redis

import json
import re
import string
import time

app = Flask(__name__)
bootstrap = Bootstrap()

if environ.get('REDIS_SERVER') is not None:
   redis_server = environ.get('REDIS_SERVER')
else:
   redis_server = 'localhost'

if environ.get('REDIS_PORT') is not None:
   redis_port = int(environ.get('REDIS_PORT'))
else:
   redis_port = 6379

if environ.get('REDIS_PASSWORD') is not None:
   redis_password = environ.get('REDIS_PASSWORD')
else:
   redis_password = ''

rdb = redis.Redis(
    host=redis_server,
    port=redis_port,
    password=redis_password
    )

rts = RedisTimeseries(
    host=redis_server,
    port=redis_port,
    password=redis_password
    )



nav = Nav()
topbar = Navbar('',
    View('Home', 'index'),
    View('Get Ads', 'getads'),
    View('View Campaign', 'getcampaign'),
    View('Revenue', 'getrevenue'),
)
nav.register_element('top', topbar)

@app.route('/')
def index():
   if rdb.exists("TOTALREVENUE") < 1:
       load_data()
   return render_template('top.html')

@app.route('/ads')
def getads():
   username = request.args.get('user')
   userlist = rdb.lrange('USERLIST', 0, 1000)
   adcopy = ""
   if username:
     adc = rdb.execute_command('RG.TRIGGER', 'adserv', username)
     adcopy = re.match( r'\(\'(.*)\',', adc[0].decode('utf-8'))
     if adcopy.group(1):
        adcopy = adcopy.group(1)
   return render_template('ads.html', username=username, userlist=userlist, adcopy=adcopy)

@app.route('/campaign')
def getcampaign():
   campaign = {}
   counters = {}
   c = rdb.zrevrange('campaign:Female:100-200K:30-35', 0 , 1000, withscores=True)
   for j in c:
      campaign[j[0].decode('utf-8')] = j[1]
      counters[j[0].decode('utf-8')] = rdb.get("counter:%s" %(j[0].decode('utf-8').replace(" ", '')))
   return render_template('campaign.html', campaign=campaign, counters=counters )

@app.route('/revenue')
def getrevenue():
   labels = []
   datapoints = []
   ts = rts.range('TOTALREVENUE', 0, -1, bucket_size_msec=10000)
   for x in ts:
      labels.append(time.strftime('%H:%M:%S', time.localtime(x[0])))
      datapoints.append(x[1])
   print(labels)
   return render_template('revenue.html', datapoints=datapoints,labels=labels )


if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=5000, host="0.0.0.0")
