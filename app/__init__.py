import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instance relative config makes flask look for configs in the instance folder in the root of the project
app = Flask(__name__, instance_relative_config=True)

# Assume environment to be dev if not specified
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')


CONFIG_FILE = 'config_dev.json'

if app.config['ENV'] == 'production':
    CONFIG_FILE = 'config_prod.json'

app.config.from_json(CONFIG_FILE)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{server}/{database}'.format(
    username=app.config['DB_USERNAME'],  # FROM CONFIG
    password=app.config['DB_PASSWORD'],  # FROM CONFIG
    server=app.config['DB_SERVER'],  # FROM CONFIG
    database=app.config['DB_DATABASE'],  # FROM CONFIG
)

db = SQLAlchemy(app)


from .mod_auth import Employee


db.create_all()
