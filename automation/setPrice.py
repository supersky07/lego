# -*- coding:utf-8 -*-  
# use sched to timing

import string
import sys
import requests
from lxml import etree
import random
import re
import pymongo
from pymongo import MongoClient
import time
import sched
from tools import getPriceBySelenium, getPriceByRequests

reload(sys)
sys.setdefaultencoding('utf-8')
schedule = sched.scheduler(time.time, time.sleep)

def getAllUrls():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    channels = db.channel

    urls = channels.find()

    res = []
    for u in urls:
        res.append(u['url'])
    
    return res

def getPriceAndSet(test_str, inc):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    price_table = db.price

    all_urls = getAllUrls()

    for u in all_urls:
        if u.find('jd') > -1:
            price = getPriceByRequests(u, 'jd')
        elif u.find('amazon.cn') > -1:
            price = getPriceByRequests(u, 'amazon')
        elif u.find('tmall') > -1:
            price = getPriceBySelenium(u, 'tmall')

        print price
        # new_data = {
        #     "price": price,
        #     "channel_id": "e9e26a4b5ffef73b",
        #     "time": time.time()
        # }

        # result = price_table.insert(new_data)
        # print result

    client.close()
    # schedule.enter(inc, 0, getPriceAndSet, (test_str, inc))

def main(test_str, inc=60):  
    schedule.enter(0, 0, getPriceAndSet, (test_str, inc))  
    schedule.run()

#main('test', 60)

getPriceAndSet('1', 60)