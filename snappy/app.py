from flask import Flask
import json


# Flask setup and config loading
app = Flask(__name__, instance_relative_config=True)
app.config.from_file("config.json", load=json.load)
