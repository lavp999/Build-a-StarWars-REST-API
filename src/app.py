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
from util_bbdd import delPlanetFav, delcharacterFav, delAmbosFav, existePlanetaFavorito, existeCharacterFavorito

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
    data = []

    # data = [char.serialize() for char in people]
    for char in people:
        data.append(char.serialize())

    return data, 200

# ------------------------------------------------------------
# Retorna la información de un sol personaje
# ------------------------------------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def getPerson(people_id):
    character = Character.query.filter_by(id=people_id).first()

    if character:
        return jsonify(character.serialize()), 200
    
    return jsonify({"mensaje": "Producto no encontrado"}), 400

# ------------------------------------------------------------
# Retorna la lista de todos los planetas
# ------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def getPlanets():
    planets = Planet.query.all()
    data = []

    # data = [char.serialize() for char in people]
    for planet in planets:
        data.append(planet.serialize())

    return data, 200

# ------------------------------------------------------------
# Retorna los datos de un planeta
# ------------------------------------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()

    if planet:
        return jsonify(planet.serialize()), 200
    
    return jsonify({"mensaje": "Planeta no encontrado"}), 400
# ------------------------------------------------------------
# retorna la lista de todos los usuarios del blog
# ------------------------------------------------------------
@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    data = []

    for user in users:
        data.append(user.serialize())

    return jsonify(data), 200

# ------------------------------------------------------------
# retorna los personajes y usuarios favoritos de el usuario
# ------------------------------------------------------------
@app.route('/users/favorites', methods=['GET'])
def getFavorites():
    favorits = Favorit.query.all()
    data = []

    for favorit in favorits:
        data.append(favorit.serialize())

    return jsonify(data), 200

# ------------------------------------------------------------
# Añade un personaje
# ------------------------------------------------------------
@app.route('/people', methods=['POST'])
def addPeople():
    data = request.json

    character = Character(nombre=data['nombre'])
    db.session.add(character)
    db.session.commit()
    return jsonify({"mensaje": "Registro creado correctamente"}), 200

# ------------------------------------------------------------
# Añade un planeta
# ------------------------------------------------------------
@app.route('/planet', methods=['POST'])
def addPlanet():
    data = request.json

    planet = Planet(nombre=data['nombre'])
    db.session.add(planet)
    db.session.commit()
    return jsonify({"mensaje": "Registro creado correctamente"}), 200

# ------------------------------------------------------------
# Modifica un planeta
# ------------------------------------------------------------
@app.route('/planet', methods=['PUT'])
def modPlanet():
    data = request.json
    planet = Planet.query.filter_by(id=data['id']).first()

    if planet:
        planet.nombre = data['nombre']
        db.session.commit()
        return jsonify({"mensaje": "Planeta actualizado"}), 200
    else:
        return jsonify({"mensaje": "Planeta no encontrado"}), 400

# ------------------------------------------------------------
# Modifica un Character
# ------------------------------------------------------------
@app.route('/people', methods=['PUT'])
def modPeople():
    data = request.json
    character = Character.query.filter_by(id=data['id']).first()

    if character:
        character.nombre = data['nombre']
        db.session.commit()
        return jsonify({"mensaje": "Character actualizado"}), 200
    else:
        return jsonify({"mensaje": "Character no encontrado"}), 400

# ------------------------------------------------------------
# Añade un planeta favorito en el usuario
# ------------------------------------------------------------
@app.route('/users/favorites/planet', methods=['POST'])
def addFavoritePlanet():
    data = request.json

    if (existePlanetaFavorito(data['id_user'], data['id_planet'])):
        return jsonify({"msg": "No se ha podido crear como favorito el User/Planeta" + str(data['id_user'])+"/"+str(data['id_planet']) +" porque ya existia"}), 400
    else:
        favorit = Favorit(id_user=data['id_user'], tipo="P", id_planet=data['id_planet'])
        db.session.add(favorit)
        db.session.commit()
        return jsonify({"mensaje": "Registro creado correctamente"}), 200

# ------------------------------------------------------------
# Añade un personaje favorito en el usuario
# ------------------------------------------------------------
@app.route('/users/favorites/people', methods=['POST'])
def addFavoritePeople():
    data = request.json

    if (existeCharacterFavorito(data['id_user'], data['id_character'])):
        return jsonify({"msg": "No se ha podido crear como favorito el User/Character" + str(data['id_user'])+"/"+str(data['id_character']) +" porque ya existia"}), 400
    else:
        favorit = Favorit(id_user=data['id_user'], tipo="C", id_character=data['id_character'])
        db.session.add(favorit)
        db.session.commit()
        return jsonify({"mensaje": "Registro creado correctamente"}), 200

# ------------------------------------------------------------
# Elimina un planeta favorito del usuario
# ------------------------------------------------------------
@app.route('/users/favorites/planet', methods=['DELETE'])
def delFavoriteplanet():
    data = request.json

    return jsonify(delPlanetFav(data['id_user'], data['id_planet'])), 200

# ------------------------------------------------------------
# Elimina un personaje favorito del usuario
# ------------------------------------------------------------
@app.route('/users/favorites/people', methods=['DELETE'])
def delFavoritePeople():
    data = request.json
    result = delcharacterFav(data['id_user'], data['id_character'])

    return jsonify(result), 200
    
# ------------------------------------------------------------
# Elimina un personaje/planeta favorito del usuario
# ------------------------------------------------------------
@app.route('/users/favorites/people/planet', methods=['DELETE'])
def delFavoriteAmbos():
    data = request.json

    return jsonify(delAmbosFav(data['id_user'], data['id_planet'], data['id_character'])), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
