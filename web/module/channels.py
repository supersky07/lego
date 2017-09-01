# Filename: channels.py
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from urllib import unquote, quote
from flask import jsonify
import json
import time
import hashlib

name_mapper = {
    "8601a75674d05e67a09d0832e8d2b5bf": "亚马逊",
    "7793e978c70d7f3cecb79edf66585a52": "京东"
}

def add_channel(hope_id, channel):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    channels = db.channel
    hopes = db.hope

    channel = channel.encode("UTF-8")
    url_hash = hashlib.md5()
    url_hash.update(channel)
    url_hash = url_hash.hexdigest()

    # 检查这个url_hash是否存在
    is_exist = channels.find_one({ "channel_id": url_hash })

    if is_exist:
        res_obj = {
            "code": 100005,
            "msg": '链接已存在',
            "data": {}
        }
    else:
        result = channels.insert({
            "url": channel,
            "channel_id": url_hash
        })

        if result:
            hopes.update({"hope_id": hope_id}, {
                "$addToSet": {
                    "channels": url_hash
                }
            })

            res_obj = {
                "code": 100000,
                "msg": '',
                "data": {}
            }
        else:
            res_obj = {
                "code": 100005,
                "msg": '插入数据失败',
                "data": {}
            }

    client.close()

    return jsonify(res_obj)    

def get_channels(channels):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    prices = db.price

    res_arr = {}
    legend_arr = []
    label_arr = []
    i = 1
    for c in channels:
        result = prices.find({ "channel_id": 'e9e26a4b5ffef73b' })

        res_arr[c] = {
            "name": name_mapper[c],
            "type": "line",
            "data": []
        }
        legend_arr.append(name_mapper[c])

        for o in result:
            temp = float(o[u'price'])
            temp = temp / i
            res_arr[c]["data"].append(temp)
            if i == 1:
                label_arr.append(o[u'time'] * 1000)
        
        i = i + 1

    if len(res_arr) == 0:
        res_obj = {
            "code": 100005,
            "msg": '没有数据',
            "data": {}
        }
    else:
        temp = []
        for u in res_arr:
            temp.append(res_arr[u])
        res_obj = {
            "code": 100000,
            "msg": '',
            "data": {
                "title": "",
                "series": temp,
                "legend_arr": legend_arr,
                "labels": label_arr
            }
        }

    return jsonify(res_obj)
