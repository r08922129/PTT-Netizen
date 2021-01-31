from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from database import db


class City(db.Model):
    # 縣市
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'District {}'.format(self.city)
class District(db.Model):
    # 鄉鎮市區
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'District {}'.format(self.district)

class Road(db.Model):
    # 路街
    __tablename__ = 'road'
    id = db.Column(db.Integer, primary_key=True)
    road = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'Road {}'.format(self.road)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    place_id = db.Column(db.String)
    rating = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref=db.backref('posts', lazy=True))

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    district = db.relationship('District', backref=db.backref('posts', lazy=True))

    road_id = db.Column(db.Integer, db.ForeignKey('road.id'), nullable=False)
    road = db.relationship('Road', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<restaurant {}>'.format(self.name)
