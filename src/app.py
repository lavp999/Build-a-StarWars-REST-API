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
from models import db, User, Character


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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def getPeople():
    data = Character.query.all()

    return jsonify(data), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def getPerson(people_id):
    response_body = {
        "msg": "Metodo GET de person " + str(people_id)
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def getPlanets():
    response_body = {
        "msg": "Metodo GET de planets "
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    response_body = {
        "msg": "Metodo GET de planet " + str(planet_id)
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def getUsers(planet_id):
    response_body = {
        "msg": "Metodo GET de User"
    }

    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def getFavorites():
    response_body = {
        "msg": "Metodo GET de Favorites"
    }

    return jsonify(response_body), 200


@app.route('/users/favorites/planet/<int:planet_id>', methods=['POST'])
def getFavoritePlanet(planet_id):
    response_body = {
        "msg": "Metodo POST de Planets Favorites" + str(planet_id)
    }

    return jsonify(response_body), 200


@app.route('/users/favorites/people/<int:people_id>', methods=['POST'])
def getFavoritePeople(people_id):
    response_body = {
        "msg": "Metodo POST de People Favorites" + str(people_id)
    }

    return jsonify(response_body), 200


@app.route('/users/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delFavoritePlanet(planet_id):
    response_body = {
        "msg": "Metodo DELETE de Planets Favorites" + str(planet_id)
    }

    return jsonify(response_body), 200

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
