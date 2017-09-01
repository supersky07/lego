# -*- coding: UTF-8 -*-
# Filename: index.py

from flask import Flask
from flask import render_template
from flask import request
import sys
sys.path.append("./module/")
import hopes
import channels

app = Flask(__name__)

@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/user/<user_id>')
def show_user_info(user_id):
    return render_template('index.html', name=user_id)

@app.route('/api/get/hope/<user_id>')
def get_hope_by_user_id(user_id):
    return hopes.get_hopes(user_id)

@app.route('/api/add/hope/<user_id>')
def add_hope_by_user_id(user_id):
    hope_name = request.args.get("hope_name")
    temp_channels = request.args.get("channels").split(',')

    return hopes.add_hope(user_id, hope_name, temp_channels)

@app.route('/api/add/channel/<hope_id>')
def add_channel_by_hope_id(hope_id):
    temp_channel = request.args.get("channel")
    return channels.add_channel(hope_id, temp_channel)

@app.route('/api/get/price')
def get_price():
    temp_channels = request.args.get("channels").split(',')
    return channels.get_channels(temp_channels)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# request.method request.args.get('key', '') request.cookies.get('username')