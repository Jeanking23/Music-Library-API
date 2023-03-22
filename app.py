from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Music(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    artist = db.Column(db.String(255), nullable = False)
    album = db.Column(db.String(255), nullable = False)
    release_date = db.Column(db.Date)
    genre = db.Column (db.String(255), nullable = False)


# Schemas
class MusicSchema(ma.Schema):
    # id = fields.Integer(primary_key = True)
    # title = fields.string(primary_key = True)
    # artist = fields.String(required = True)
    # album = fields.String(required = True)
    # release_date = fields.Date()
    # genre = field.String(require = True)
    class Meta:
        fields = ("id", "title", "artist", "album","release_date", "genre" )

music_schema = MusicSchema()
musics_schema = MusicSchema(many = True)
# Resources
class MusicListResource(Resource):
     def get(self):
         all_musics = Music.query.all()
         return musics_schema.dump(all_musics)
# Routes
api.add_resource(MusicListResource, '/api/musics')