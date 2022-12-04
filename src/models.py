from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



db = SQLAlchemy()
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

class Favorit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey('user.id'))
    tipo = db.Column(db.String(1), nullable=False, default="A")
    id_character = db.Column(db.Integer, ForeignKey('character.id'), nullable=True)
    id_planet = db.Column(db.Integer, ForeignKey('planet.id'), nullable=True)
    user = db.relationship(User)
    character = db.relationship(Character)
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Favorit %r>' % self.id


    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_character": self.id_character,
            "id_planet": self.id_planet,
            "tipo": self.tipo
        }
