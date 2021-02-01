# PTT-Netizen
## Features
1. retrun an article from PTT[熱門文章](https://disp.cc/m/) in random.
2. send user's location and return the information of a near restaurant in random.
3. return a paper from ACL2020 in random
4. 計畫通行. It's a cover singer I like, hope you too :)

## QR-Code
This chatbot is deployed on Heroku.
Due to the limitation on free web dyno, the server will sleep if it receive no web traffic in 30 miniutes period.
You may have to wait it to warm up for a while.

![image](https://github.com/r08922129/PTT-Netizen/blob/main/qrcode.png?raw=true)
## Setting
If you want to deploy this chatbot by yourself, 6 environment variables must be set.
```
export LINE_CHANNEL_SECRET="Your Line channel secret"
export LINE_CHANNEL_ACCESS_TOKEN="Your Line channel access token"
```
You can get them at the console home of your line bot channel.
Please refer to the official [tutorial](https://developers.line.biz/en/docs/messaging-api/getting-started/#using-console).

```
export APP_SETTINGS="config.DevelopmentConfig"
```
Choose the config declared in `config.py`
```
export DATABASE_URL="url to your database"
```
eg. `export DATABASE_URL="postgresql:///chatbot"`
```
export GOOGLE_API_KEY="your google api key"
```
You have to apply a [billing account](https://console.developers.google.com/apis) to access google api.
There are $200USD per month for free. Be careful to use the searching restaurant feature.

```
export REDIS_URL="redis://:"
```
To update the hot articles in PTT periodically, `clock: python /app/src/updatehot.py` was set in `Procfile`. For more [detail](https://devcenter.heroku.com/articles/clock-processes-python).

Heroku will run `/app/src/updatehot.py` at the interval you set in this file in another dyno.
Because the application and the clocker will run in different dynos seperately, neither share variable nor mmap can be used to store the list of hot articles. Clocker should update the list into a database and then the application can grab the list from it. 
A simple way is attaching [Heroku-Redis](https://devcenter.heroku.com/articles/heroku-redis) to this chatbot application. Then heroku will set `REDIS_URL` automatically.

# Citatio
文本來自於 [Gossiping-Chinese-Corpus](https://github.com/zake7749/Gossiping-Chinese-Corpus)

@misc{
    kai-chou yang_2019,
    title={PTT-Gossiping-Corpus},
    url={https://www.kaggle.com/dsv/676336},
    DOI={10.34740/DVS/676336},
    publisher={Kaggle},
    author={Kai-Chou Yang},
    year={2019}
}


