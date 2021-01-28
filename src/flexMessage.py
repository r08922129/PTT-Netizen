#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from linebot.models import FlexSendMessage
flex_message = FlexSendMessage(
    alt_text='hello',
    contents={
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://img.ltn.com.tw/Upload/news/600/2019/09/16/php7CYMfK.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "http://linecorp.com/"
                }
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                      "type": "postback",
                      "label": "PTT 熱門",
                      "data":"hot",
                      "displayText": "https://linecorp.com"
                    }
                  },
                  {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                      "type": "uri",
                      "label": "A paper a day",
                      "uri": "https://linecorp.com"
                    }
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "通行一下",
                      "uri": "http://linecorp.com/"
                    }
                  }
                ],
                "flex": 0
              }
            }
)

