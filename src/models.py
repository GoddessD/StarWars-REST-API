from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_characters = db.Table(
    "favorite_characters",
    db.Column("user_id",db.Integer, db.ForeignKey("user.id"),primary_key=True),
    db.Column("character_id", db.Integer, db.ForeignKey("characters.id") ,primary_key=True),
)

favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id",db.Integer, db.ForeignKey("user.id"),primary_key=True),
    db.Column("planet_id", db.Integer, db.ForeignKey("planets.planet_id") ,primary_key=True),
)

favorite_vehicles = db.Table(
    "favorite_vehicles",
    db.Column("user_id",db.Integer, db.ForeignKey("user.id"),primary_key=True),
    db.Column("vehicle_id", db.Integer, db.ForeignKey("vehicles.vehicle_id") ,primary_key=True),
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_characters = db.relationship('Characters',secondary=favorite_characters,lazy="subquery")
    favorite_planets = db.relationship('Planets',secondary=favorite_planets,lazy="subquery")
    favorite_vehicles = db.relationship('Vehicles',secondary=favorite_vehicles,lazy="subquery")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": list(map(lambda x: x.name, self.favorite_characters)),
            "favorite_planets": list(map(lambda x: x.name, self.favorite_planets)),
            "favorite_vehicles": list(map(lambda x: x.name, self.favorite_vehicles)),
           
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(120) , nullable=False) 
    planet_from = db.Column(db.Integer, db.ForeignKey('planets.planet_id'), nullable=True)
    birth_year = db.Column(db.Integer)


    def __repr__(self):
        return '<Character %r>' % self.name


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'planet_from': self.planet_from,
            'birth_year': self.birth_year 
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120) , unique=True , nullable=False)
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            'planet_id': self.planet_id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population,
            'climate': self.climate,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    vehicle_id = db.Column(db.Integer,primary_key=True, nullable=False)
    name = db.Column(db.String(120) , unique=True , nullable=False)
    model = db.Column(db.String(120))
    crew = db.Column(db.String(120))
    vehicle_class = db.Column(db.String(120))

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            'name': self.name,
            'vehicle_id': self.vehicle_id,
            'model': self.model,
            'crew': self.crew,
            'vehicle_class': self.vehicle_class
        }

