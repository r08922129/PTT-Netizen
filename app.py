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
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent
)
from src.QABot import QABot
from src.pttHot import updateHotList, hot_list
from src.menu import menu
import threading
import time
import random
import json
# build Question Answering Bot
qabot = QABot("/app/corpus")

# Set crawler to get hot list from ptt
t = threading.Thread(target = updateHotList)
t.start()
# Get doori urls
with open('/app/links/doori') as f:
    doori_links = [line.strip() for line in f.readlines()]
# Get papers in ACL
with open('/app/links/acl.json') as f:
    papers = json.load(f)
app = Flask(__name__)

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
        qabot.talking = True
        print("Talking mode")
    elif event.message.text == "shut up":
        qabot.talking = False
        print("Silence mode")
    elif qabot.talking:
        msg = qabot.reply(event.message.text)
        print(msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )

@handler.add(PostbackEvent)
def handle_text_message(event):
    if event.postback.data == "hot":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(hot_list))
        )
    elif event.postback.data == "paper":
        paper = random.choice(list(papers.keys()))
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": paper,
                        "size": "md",
                        "style": "italic",
                        "wrap": True,
                        "weight": "bold",
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": papers[paper]
                        }
                    }
                    ],
                    "spacing": "none",
                    "margin": "xs"
                }
            }
        )
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )
    elif event.postback.data == "doori":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(doori_links))
        )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(threaded=True, debug=options.debug, port=options.port)
