"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorit
import json 
from json import JSONEncoder

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# ------------------------------------------------------------
# Handle/serialize errors like a JSON object
# ------------------------------------------------------------
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# ------------------------------------------------------------
# generate sitemap with all your endpoints
# ------------------------------------------------------------
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ------------------------------------------------------------
# Retorna todos los personajes de StarWars
# ------------------------------------------------------------
@app.route('/people', methods=['GET'])
def getPeople():
    people = Character.query.all()
    print (people)

    return jsonify(people), 200

# ------------------------------------------------------------
# Retorna la información de un sol personaje
# ------------------------------------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def getPerson(people_id):
    people = Character.query.filter_by(id=people_id).first()

    return jsonify(people), 200

# ------------------------------------------------------------
# Retorna la lista de todos los planetas
# ------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def getPlanets():
    planets = Planet.query.all()
    print (planets)
    return jsonify(planets), 200

# ------------------------------------------------------------
# Retorna los datos de un planeta
# ------------------------------------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()

    return jsonify(planet), 200

# ------------------------------------------------------------
# retorna la lista de todos los usuarios del blog
# ------------------------------------------------------------
@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    print (users)
    return jsonify(users), 200

# ------------------------------------------------------------
# retorna los personajes y usuarios favoritos de el usuario "conectado"
# ------------------------------------------------------------
@app.route('/users/favorites', methods=['GET'])
def getFavorites():
    favorites = Favorit.query.all()
    print (favorites)
    return jsonify(favorites), 200

# ------------------------------------------------------------
# Añade un planeta favorito en el usuario "conectado"
# ------------------------------------------------------------
@app.route('/users/favorites/planet/<int:planet_id>', methods=['POST'])
def getFavoritePlanet(planet_id):
    response_body = {
        "msg": "Metodo POST de Planets Favorites" + str(planet_id)
    }

    return jsonify(response_body), 200


# ------------------------------------------------------------
# Añade un personaje favorito en el usuario "conectado"
# ------------------------------------------------------------
@app.route('/users/favorites/people/<int:people_id>', methods=['POST'])
def getFavoritePeople(people_id):
    response_body = {
        "msg": "Metodo POST de People Favorites" + str(people_id)
    }

    return jsonify(response_body), 200


# ------------------------------------------------------------
# Elimina un planeta favorito del usuario "conectado"
# ------------------------------------------------------------
@app.route('/users/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delFavoritePlanet(planet_id):
    response_body = {
        "msg": "Metodo DELETE de Planets Favorites" + str(planet_id)
    }

    return jsonify(response_body), 200

# ------------------------------------------------------------
# Elimina un personaje favorito del usuario "conectado"
# ------------------------------------------------------------
@app.route('/users/favorites/people/<int:people_id>', methods=['DELETE'])
def delFavoritePeople(people_id):
    response_body = {
        "msg": "Metodo DELETE de People Favorites" + str(people_id)
    }

    return jsonify(response_body), 200














# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
