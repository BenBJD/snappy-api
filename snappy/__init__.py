# imports
from flask import Flask

# Flask setup and config loading
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

from . import routes
