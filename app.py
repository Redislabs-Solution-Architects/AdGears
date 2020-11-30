from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from redistimeseries.client import Client as RedisTimeseries
from redisbloom.client import Client as RedisBloom


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

rb = RedisBloom(
    host=redis_server,
    port=redis_port,
    password=redis_password
    )


nav = Nav()
topbar = Navbar('',
    View('Home', 'index'),
    View('Get Ads', 'getads'),
    View('View Campaigns', 'getcampaign'),
    View('Revenue', 'getrevenue'),
    View('Ad Stats', 'getadstats'),
    View('New Campaign', 'addcampaign'),
    View('New Intent', 'addintent'),
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
   return render_template('revenue.html', datapoints=datapoints,labels=labels )

@app.route('/getadstats')
def getadstats():
   ads = rdb.smembers('AdStats')
   return render_template('getadstats.html', ads=ads)


@app.route('/displayadstats')
def displayadstats():
   ad = request.args.get('ad')
   labels = []
   datapoints = []
   ts = rts.range("ADVIEW:%s" %(ad), 0, -1, bucket_size_msec=10000)
   for x in ts:
      labels.append(time.strftime('%H:%M:%S', time.localtime(x[0])))
      datapoints.append(x[1])
   return render_template('adstats.html', datapoints=datapoints,labels=labels,title="Impressions for %s" %(ad) )

@app.route('/addcampaign')
def addcampaign():
   return render_template('addcampaign.html')

@app.route('/insertcampaign', methods = ['POST'])
def insertcampaign():
   f = request.form.to_dict()
   rdb.zadd(
     "campaign:%s:%s:%s" %(f['sex'], f['income'], f['age']),
     {f['copy']: f['score']}
   )
   rb.bfCreate(f['copy'], 0.01, 1000)
   rb.set("counter:%s" %(f['copy'].replace(" ", '')), f['limit'])
   rts.create("ADVIEW:%s" %(f['copy'].replace(" ", '')))
   rb.sadd("AdStats",f['copy'])
   return redirect("/campaign", code=302)

@app.route('/addintent')
def addintent():
   userlist = rdb.lrange('USERLIST', 0, 1000)
   return render_template('addintent.html', userlist=userlist)

@app.route('/insertintent', methods = ['POST'])
def insertintent():
   f = request.form.to_dict()
   rdb.set("user:%s:intent" %(f['user'].replace(" ", '')), f['campaign'], ex=f['ttl'])
   print(f)
   return redirect("/ads?user=%s" %(f['user']), code=302)

if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=5000, host="0.0.0.0")
