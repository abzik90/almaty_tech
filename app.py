from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ride_requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from api.location_controller import rides_bp
app.register_blueprint(rides_bp, url_prefix='/')