from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)


# mysql://username:password@hostname/database

# HOST = '34.93.23.26'
# USERNAME = 'flask'
# PASSWORD = '12345678'
# DATABASE = 'flask'

# Free mysql hosting
HOST = 'sql12.freemysqlhosting.net'
USERNAME = 'sql12356834'
PASSWORD = 'WjTyIMjauF'
DATABASE = 'sql12356834'

db_uri = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
heroku_uri = 'postgres://rmgzzblhxhdflz:d187090005767b826f9e7631586da84c5d2c2d6815c1f876fa435b09b04eaeeb@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/dd0a5a59ngoa4t'

ENV = 'prod'

if ENV == 'dev':
    uri = db_uri
else:
    uri = heroku_uri

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
