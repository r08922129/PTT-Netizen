# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort, render_template, jsonify
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent,
    LocationMessage, 
)
from src.QABot import QABot
from src.pttHot import updateHotList, hot_list
from src.reply import *
import threading
import time
import random
import json
import googlemaps
import database
from models import Type, District, Road, Section, Restaurant, db
import commands

ROOT = os.path.join(os.path.dirname(__file__))
# setup config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# setup database
database.init_app(app)
# set commands
commands.init_app(app)
# build object for google map
gmaps = googlemaps.Client(key='')

# build Question Answering Bot
qabot = QABot(os.path.join(ROOT, 'corpus'))

# Get doori urls
with open(os.path.join(ROOT, 'links/doori')) as f:
    doori_links = [line.strip() for line in f.readlines()]
# Get papers in ACL
with open(os.path.join(ROOT, 'links/acl.json')) as f:
    papers = json.load(f)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def main_page():
    items = Road.query.all()
    return render_template('index.html', items=items)

@app.route("/road")
def add_road():
    road = Road(road="忠孝")
    # add to the database session
    database.db.session.add(road)
        
    # commit to persist into the database
    database.db.session.commit()
    
    return jsonify({"sucess": road.road})

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == "menu":
        line_bot_api.reply_message(
            event.reply_token,
            menu
        )
    elif event.message.text == "talk":
        qabot.talking = True
        print("Talking mode")
        print(threading.get_ident())
    elif event.message.text == "shut up":
        qabot.talking = False
        print("Silence mode")
        print(threading.get_ident())
    elif qabot.talking:
        msg = qabot.reply(event.message.text)
        print(msg)
        print(threading.get_ident())
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    else:
        print("QA BOT MODE", qabot.talking)
        print(threading.get_ident())

@handler.add(PostbackEvent)
def handle_postbacl_message(event):
    if event.postback.data == "hot":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(hot_list))
        )
    elif event.postback.data == "eat":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="選擇種類",
                quick_reply = asking_food
            )
        )
    elif event.postback.data == "paper":
        paper = random.choice(list(papers.keys()))
        flex_message = get_paper_reply(paper, papers[paper])
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )
    elif event.postback.data == "doori":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(doori_links))
        )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # use google location api to find restaurant
    # restaurants = gmaps.places('餐廳', event.message.address, type='restaurant')

    print("location:", event.message.address, event.message.latitude, event.message.longitude)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # Set crawler to get hot list from ptt
    t = threading.Thread(target = updateHotList)
    t.start()
    app.run(threaded=True, debug=options.debug, port=options.port)
