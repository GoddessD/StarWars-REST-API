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
from models import db, User, Characters, Planets, Vehicles



app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


characters = [
    {
        'id': 1,
        'name': 'Luke Skywalker',
        'planet_from': 'Tatooine',
        'birth_year': '19 BBY'
    },

    {
        'id': 2,
        'name': 'Darth Vader',
        'planet_from': 'Tatooine',
        'birth_year': '41 BBY'
    }
]

planets = [
    {
        'planet_id': 1,
        'name': 'Tatooine',
        'diameter': '10465',
        'population': '200000',
        'climate': 'arid',
    },

    {
        'id': 2,
        'name': 'Naboo',
        'diameter': '10465',
        'population': '4500000000',
        'climate': 'temperate',
    }
]

vehicles = [
    {
        'vehicle_id': '001',
        'name': 'Sand Crawler',
        'model': 'Digger Crawler',
        'crew': '46',
        'vehicle_class': 'wheeled'
    },

    {
        'vehicle_id': '002',
        'name': 'T-16 skyhopper',
        'model': 'T-16 skyhopper',
        'crew': '1',
        'vehicle_class': 'repulsorcraft',
    }
]

favorites = [
    {
        'date_added': '12/01/2022',
        'user_id': '2',
        'favorite_characters': 'Luke Skywalker',
        'favorite_planets': 'Naboo',
        'favorite_vehicles': 'car'
    }


]


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# sitemap: all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_all_users():
    users=User.query.all()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": users.serialize()

    }

    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    json_text = jsonify(characters)
    return json_text, 200


@app.route('/planets', methods=['GET'])
def get_planets():
    json_text = jsonify(planets)
    return json_text, 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    json_text = jsonify(vehicles)
    return json_text, 200


@app.route('/favorites', methods=['GET'])
def get_favorites():
    json_text = jsonify(Favorites)
    return json_text, 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_single_characters(id):
    # single_character = characters[id]
    single_character = Characters.query.get(id)
    # return jsonify(x.to_dict() for x in all_characters), 200
    return jsonify()


@app.route('/characters2', methods=['GET'])
def get_characters2():
    all_characters = Characters.query.all()
    return json_text, 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    single_planet = planets[id]
    return jsonify(x.to_dict() for x in all_planets), 200


@app.route('/vehicles/<int:id>', methods=['GET'])
def get_single_vehicle(id):
    single_vehicle = vehicles[id]
    return jsonify(x.to_dict() for x in all_vehicles), 200

# adding characters to a user's favorites:


@app.route('/users<int:id>/favorites/', methods=['GET'])
def get_all_favorites(id):
    user = User.query.get(id)
    user.to_dict()
    user_favorites = {
        'favorite_characters': user.favorite_characters,
        'favorite_planets': user.favorite_planets,
        'favorite_vehicles': user.favorite_vehicles
    }
    return jsonify(user_favorites), 200


@app.route('/users/favorites/character/<int:id>', methods=['POST', 'DELETE'])
def add_to_favorite_characters(id, name):
    body = request.get_json()
    if request.method == 'POST':
        user = User.query.get(id)
        character = Characters.query.get(name)
        user.favorite_characters.append(character)
        db.session.commit()
        return 'Favorite character has been added', 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        character = Characters.query.get(name)
        user.favorite_characters.remove(character)
        db.session.commit()
        return 'Character has been deleted from favorites', 200
    return 'POST or DELETE request was invalid', 484


@app.route('/users/favorites/planet/<int:id>', methods=['POST', 'DELETE'])
def add_to_favorite_planets(id, name):
    body = request.get_json()
    if request.method == 'POST':
        user = User.query.get(id)
        planet = Planets.query.get(name)
        user.favorite_planets.append(planet)
        db.session.commit()
        return 'Favorite planet has been added', 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        planet = Planets.query.get(name)
        user.favorite_planets.remove(planet)
        db.session.commit()
        return 'Planet has been deleted from favorites', 200
    return 'POST or DELETE request was invalid', 484


@app.route('/users/favorites/vehicle/<int:id>', methods=['POST', 'DELETE'])
def add_to_favorite_vehicles(id, name): #passing through the id of the user
    body = request.get_json()
    if request.method == 'POST':
        user = User.query.get(id)
        vehicle = Vehicles.query.get(name)
        user.favorite_characters.append(vehicle)
        db.session.commit()
        return 'Favorite vehicle has been added', 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        vehicle = Vehicles.query.get(name)
        user.favorite_vehicles.remove(vehicle)
        db.session.commit()
        return 'Vehicle has been deleted from favorites', 200
    return 'POST or DELETE request was invalid', 484


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
