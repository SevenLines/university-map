import os

import yaml
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder=os.path.abspath("static\\dist"))

# setup API
api = Api(app, prefix="/api")

# setup Database
db = SQLAlchemy(app)

from server.namespaces.auditories import api as ns1
api.add_namespace(ns1)

# setup YAML
with open(os.path.join(app.root_path, '..', 'settings.yaml')) as f:
    settings = yaml.load(f, yaml.SafeLoader)

# fix configs
app.config['SQLALCHEMY_DATABASE_URI'] = settings['SQLALCHEMY_DATABASE_URI']
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = settings['SECRET_KEY']
