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
from flask_migrate import Migrate
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent,
    LocationMessage, LocationSendMessage
)
from src.QABot import QABot
from src.ptthot import update_hot_list, hot_list
from src.reply import *
import src.findfood as findfood
import threading
import time
import random
import json
import googlemaps
import database
import commands
from models import *
import mmap

ROOT = os.path.join(os.path.dirname(__file__))
# setup config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
# setup database
database.init_app(app)
# set commands
commands.init_app(app)
# build Question Answering Bot
qabot = QABot(os.path.join(ROOT, 'corpus'))
# build mmap to access chatbot status
with open("bot_status", "wb") as f:
    f.write(b"\0")
with open("bot_status", "r+b") as f:
    BOT_STATUS = mmap.mmap(f.fileno(), 0)

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
        BOT_STATUS[0] = 1
        BOT_STATUS.flush()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="安安你好")
        )
    elif event.message.text == "shut up":
        BOT_STATUS[0] = 0
        BOT_STATUS.flush()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉")
        )
    elif int.from_bytes(BOT_STATUS, byteorder='big'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=qabot.reply(event.message.text))
        )

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
                text="現在的位置??",
                quick_reply = asking_food
            )
        )
    elif event.postback.data == "paper":
        paper = random.choice(list(papers.keys()))
        line_bot_api.reply_message(
            event.reply_token,
            get_paper_reply(paper, papers[paper]),
        )
    elif event.postback.data == "doori":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(doori_links))
        )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # use google location api to find restaurant
    restaurant = findfood.find_food('餐廳', event.message.latitude, event.message.longitude, app)
    line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title=restaurant['name'], address=restaurant['place'],
                latitude=restaurant['latitude'], longitude=restaurant['longitude']
          )
        )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # Set crawler to get hot list from ptt
    t = threading.Thread(target = update_hot_list)
    t.start()
    app.run(threaded=True, debug=options.debug, port=options.port)
