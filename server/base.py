import os
import yaml
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__, static_folder=os.path.abspath("static\\dist"))

# setup YAML
with open(os.path.join(app.root_path, '..', 'settings.yaml')) as f:
    settings = yaml.load(f, yaml.SafeLoader)

# fix configs
app.config['SQLALCHEMY_DATABASE_URI'] = settings['SQLALCHEMY_DATABASE_URI']
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = settings['SECRET_KEY']

# setup Database
db = SQLAlchemy(app)

# setup API
from namespaces.auditories import api as auditories_ns
from namespaces.teachers import api as teachers_ns
api = Api(app, prefix="/api")
api.add_namespace(auditories_ns)
api.add_namespace(teachers_ns)

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response