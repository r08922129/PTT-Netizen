#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import os
import time


# In[66]:

def update_hot_list():
    while True:
        hot_list.clear()
        hot_base = "https://disp.cc/m/"
        html = requests.get(hot_base)
        soup = BeautifulSoup(html.text, "html.parser")
        nodes = soup.findAll('div', {'class' : 'ht_title'})

        for node in nodes:
            url = node.find('a').get('href')
            # to get the original url
            html = requests.get(os.path.join(hot_base, url))
            soup = BeautifulSoup(html.text, "html.parser")
            for node in soup.findAll('span', {'class' : 'record'}):
                if '文章網址' in node.text:
                    hot_list.append(node.find('a').get('href'))
                    break
        time.sleep(3600)

