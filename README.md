# PTT-Netizen
## Features
1. 返回隨機一篇目前PTT[熱門文章](https://disp.cc/m/)
2. 傳送目前位置, 隨機返回附近餐廳
3. 從ACL2020隨機返回一篇論文
## QR-Code
![image](https://github.com/r08922129/PTT-Netizen/blob/main/qrcode.png?raw=true)
## Setting
If you want to use this chatbot, 5 environment variables must be set.
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


