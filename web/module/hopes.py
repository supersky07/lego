# Filename: hopes.py
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from urllib import unquote, quote
from flask import jsonify
import json
import time
import hashlib

def get_hopes(user_id):
    arr = []

    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    hopes = db.hope
    result = hopes.find({ "user_id": user_id })
    client.close()

    for u in result:
        temp = {
            "hope_name": u[u'hope_name'],
            "hope_id": u[u'hope_id'],
            "channels": u[u'channels']
        }

        arr.append(temp)

    if len(arr) == 0:
        res_obj = {
            "code": 100005,
            "msg": '没有数据',
            "data": {}
        }
    else:
        res_obj = {
            "code": 100000,
            "msg": '',
            "data": arr
        }

    return jsonify(res_obj)

def add_hope(user_id, hope_name, channel_data):
    # 先把channels添加到channels表，再把hope_name存到hope表
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.lego
    db.collection_names(include_system_collections=False)
    channels = db.channel
    hopes = db.hope
    users = db.user

    channel_id_res = []
    
    # 先往channel表中塞
    for c in channel_data:
        c = c.encode("UTF-8")
        url_hash = hashlib.md5()
        url_hash.update(c)
        url_hash = url_hash.hexdigest()

        is_exist = channels.find_one({ "channel_id": url_hash })

        if is_exist:
            channel_id_res.append(is_exist['channel_id'])
        else:
            result = channels.insert({
                "url": c,
                "channel_id": url_hash
            })

            channel_id_res.append(url_hash)
            
    # 再塞到hope表
    hope_id_hash =  hashlib.md5()
    hope_id_hash.update(str(time.time()).encode('UTF-8'))
    hope_id_hash = hope_id_hash.hexdigest()

    hopes.insert({
        "hope_name": hope_name,
        "channels": channel_id_res,
        "hope_id": hope_id_hash
    })

    # 再更新user表
    users.update({"uid": user_id}, {
        "$addToSet": {
            "hopes": hope_id_hash
        }
    })

    client.close()

    return hope_id_hash
