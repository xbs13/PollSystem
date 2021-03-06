import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
import flask_admin as admin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)
admin = admin.Admin(app, name="Poll System")

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('poll startup')

from app import views, models, admin_views
