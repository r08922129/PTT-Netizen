import googlemaps
import os
import re
import threading
from models import *
import random
from database import db
import json
# build object for google map
gmaps = googlemaps.Client(key=os.environ['GOOGLE_API_KEY'])

def parse_address(address):
  pattern = re.compile(r"(?:([\u3400-\u9FFF]{2,5}?[市|縣])([\u3400-\u9FFF]{2,5}?[鄉|鎮|市|區])([\u3400-\u9FFF]{2,6}?[路|街])(\w*))")
  try:
    city = re.search(pattern, address).group(1)
  except:
    city = None
  try:
    district = re.search(pattern, address).group(2)
  except:
    district = None
  try:
    road = re.search(pattern, address).group(2)
  except:
    road = None
  try:
    addr = re.search(pattern, address).group(3)
  except:
    addr = None
  return city, district, road, addr

def store_food(restaurants, app):
    with app.app_context():
        for restaurant in restaurants['results']:

            city, district, road, addr = parse_address(restaurant['formatted_address'])

            # check the name is unique
            temp = City.query.filter_by(city=city).first()
            if temp:
                city = temp
            else:
                city = City(city=city)
                db.session.add(city)

            temp = District.query.filter_by(district=district).first()
            if temp:
                district = temp
            else:
                district = District(district=district)
                db.session.add(district)

            temp = Road.query.filter_by(road=road).first()
            if temp:
                road = temp
            else:
                road = Road(road=road)
                db.session.add(road)

            rest = Restaurant(
                name=restaurant['name'],
                place_id=restaurant['place_id'],
                rating=restaurant['rating'],
                latitude=restaurant['geometry']['location']['lat'],
                longitude=restaurant['geometry']['location']['lng'],
                address=addr,
                city=city,
                district=district,
                road=road,
            )
            db.session.add(rest)
            db.session.commit()

def find_food(query, latitude, longitude, app):
    restaurants = gmaps.places(query, (latitude, longitude),
                                type='restaurant', radius=1000,
                                language='zh-tw')
    t = threading.Thread(target = store_food, args=(restaurants, app))
    t.start()
    if len(restaurants['results']):
        idx = random.randint(0, len(restaurants['results']))
        restaurant = restaurants['results'][idx]
        return {
            'name' : restaurant['name'],
            'place' : restaurant['formatted_address'],
            'rating' : restaurant['rating'],
            'latitude' : restaurant['geometry']['location']['lat'],
            'longitude' : restaurant['geometry']['location']['lng'],
        }
    else:
        return None