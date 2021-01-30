from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from database import db

class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    def __repr__(self):
        return 'type {}'.format(self.type)

class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'District {}'.format(self.district)

class Road(db.Model):
    __tablename__ = 'road'
    id = db.Column(db.Integer, primary_key=True)
    road = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'Road {}'.format(self.road)

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String, unique=True)
    def __repr__(self):
        return 'type {}'.format(self.section)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    place_id = db.Column(db.String)
    rating = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String)

    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    type = db.relationship('Type', backref=db.backref('posts', lazy=True))

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    district = db.relationship('District', backref=db.backref('posts', lazy=True))

    road_id = db.Column(db.Integer, db.ForeignKey('road.id'), nullable=False)
    road = db.relationship('Road', backref=db.backref('posts', lazy=True))

    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<restaurant {}>'.format(self.name)
