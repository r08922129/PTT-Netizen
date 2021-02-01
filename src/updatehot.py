import redis
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from bs4 import BeautifulSoup
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=180)
def test():
    r = redis.from_url(os.environ.get("REDIS_URL"))
    hot_list = []
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
    # update hot list
    if hot_list:
        for i in range(r.llen("hot list")):
            r.lpop("hot list")
        for url in hot_list:
            r.lpush("hot list", url)

sched.start()
