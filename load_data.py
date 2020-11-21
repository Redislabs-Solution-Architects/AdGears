#!/usr/bin/env python3 

from redisbloom.client import Client as RedisBloom

import csv
import redis
from os import environ

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
rb = RedisBloom(
    host=redis_server,
    port=redis_port,
    password=redis_password
    )




with open('./users.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            rdb.hset(
                "user:%s" %(row[0].replace(" ", '')),
                mapping = {
                    'Name': row[0],
                    'AgeDemo': row[1],
                    'IncomeDemo': row[2],
                    'Sex': row[3]
                })
        line_count += 1

with open('./campaigns.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            rdb.zadd(
                "campaign:%s" %(row[0].replace(" ", '')),
                {row[2]: row[1]}
            )
            rb.bfCreate(row[2], 0.01, 1000)
        line_count += 1

